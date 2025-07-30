import os
from pathlib import Path
import subprocess
import signal
from . import playlist_manager as playlist
from . import channel_manager as cm
from utils.config_reader import load_config

# Start a single channel: spawn ffmpeg in background, record its PID

conf = load_config()
CHAN_ROOT = Path(conf["Paths"]["CHAN_ROOT"])
HLS_ROOT = Path(conf["Paths"]["HLS_ROOT"])
SEGMENT_TIME = conf["HLS"]["SEGMENT_TIME"]
LIST_SIZE = conf["HLS"]["LIST_SIZE"]


def launch_ffmpeg(cfg: dict, concat_path: Path) -> subprocess.Popen:
    cid = cfg["id"]
    stream_dir = HLS_ROOT/cid
    chan_dir = CHAN_ROOT/cid
    os.makedirs(stream_dir, exist_ok=True)
    os.makedirs(chan_dir, exist_ok=True)

    # Build ffmpeg command
    cmd = [
        "ffmpeg",
        # Input rate control must come before input
        "-re",
        # Allow file protocol for concat
        # "-protocol_whitelist", "file,pipe,concat",
        # Reset timestamps and handle discontinuities
        # "-max_interleave_delta", "0",
        # "-dts_delta_threshold", "100",
        # "-max_delay", "5000000",
        # concat demuxer with necessary options
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_path),
        # Handle broken timestamps and errors
        "-fflags", "+genpts", #+igndts+discardcorrupt",
        # "-err_detect", "ignore_err",
        "-avoid_negative_ts", "make_zero",
        "-reset_timestamps", "1",
        # copy streams but handle timestamps carefully
        "-c:v", "copy", "-c:a", "copy",
        # "-start_at_zero",
        # "-copyts",
        # "-vsync", "1",
        # HLS settings
        "-f", "hls",
        "-hls_time", str(SEGMENT_TIME),
        "-hls_list_size", str(LIST_SIZE),
        "-hls_flags", "delete_segments",  # +independent_segments+discont_start",
        str(stream_dir/"index.m3u8")
    ]

    # Open log files
    stdout_log = chan_dir/"ffmpeg.out.log"
    stderr_log = chan_dir/"ffmpeg.err.log"

    # Launch ffmpeg in its own process group
    proc = subprocess.Popen(
        cmd,
        stdout=open(stdout_log, "a"),
        stderr=open(stderr_log, "a"),
        preexec_fn=os.setsid
    )

    # Store PID for later control
    pid_file = CHAN_ROOT/cid/"channel.pid"
    with open(pid_file, "w") as f:
        f.write(str(proc.pid))

    print(f"Started channel '{cid}' (pid={proc.pid})")
    return proc


def start_channel(cfg):
    cid = cfg["id"]

    # Check if already running
    if cm.channel_is_running(cfg):
        print(f"Channel '{cid}' is already running.")
        return

    # Build playlist path
    playlist_path = playlist.build_playlist(
        cid, cfg["media_dir"], cfg["recursive"])

    # Launch ffmpeg process
    try:
        p = launch_ffmpeg(cfg, playlist_path)
        return p.pid
    except Exception as e:
        print(f"Failed to start channel '{cid}': {str(e)}")
        return None


def stop_channel(cfg):
    cid = cfg["id"]
    pid_file = CHAN_ROOT/cid/"channel.pid"
    if not os.path.exists(pid_file):
        print(f"Channel '{cid}' is not running (no pid file).")
        return
    with open(pid_file) as f:
        pid = int(f.read())
    try:
        os.killpg(pid, signal.SIGTERM)
        print(f"Stopped channel '{cid}' (pid={pid})")
    except ProcessLookupError:
        print(f"Process {pid} for channel '{cid}' not found.")
    os.remove(pid_file)


def restart_channel(cfg):
    stop_channel(cfg)
    start_channel(cfg)
