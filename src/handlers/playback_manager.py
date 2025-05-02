
import os
from pathlib import Path
import subprocess
import signal
from utils.config_reader import load_config

# Start a single channel: spawn ffmpeg in background, record its PID


def launch_ffmpeg(cfg, concat_path):
    cid = cfg["id"]
    conf = load_config()
    HLS_ROOT = Path(conf["Paths"]["HLS_ROOT"])
    SEGMENT_TIME = conf["HLS"]["SEGMENT_TIME"]
    LIST_SIZE = conf["HLS"]["LIST_SIZE"]
    LOG_ROOT = Path(conf["Paths"]["LOG_ROOT"])
    out_dir = HLS_ROOT/cid
    log_dir = LOG_ROOT/cid
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    # Build ffmpeg command
    cmd = [
        "ffmpeg",
        "-re",
        # regenerate PTS & ignore broken DTS
        "-fflags", "+genpts+igndts",
        # loop the entire playlist forever
        "-stream_loop", "-1",
        # concat demuxer
        "-f", "concat", "-safe", "0", "-i", str(concat_path),
        # copy streams but force any negative ts → 0
        "-c:v", "copy", "-c:a", "copy",
        "-avoid_negative_ts", "make_zero",
        # HLS settings
        "-f", "hls",
        "-hls_time", str(SEGMENT_TIME),
        "-hls_list_size", str(LIST_SIZE),
        "-hls_flags", "delete_segments",
        str(out_dir/"index.m3u8")
    ]

    # Open log files
    stdout_log = cfg.get(
        "log_stdout", os.path.join(log_dir, f"{cid}.out.log"))
    stderr_log = cfg.get(
        "log_stderr", os.path.join(log_dir, f"{cid}.err.log"))

    # Launch ffmpeg in its own process group
    p = subprocess.Popen(
        cmd,
        stdout=open(stdout_log, "a"),
        stderr=open(stderr_log, "a"),
        preexec_fn=os.setsid
    )

    # Store PID for later control
    pid_file = os.path.join(out_dir, f"{cid}.pid")
    with open(pid_file, "w") as f:
        f.write(str(p.pid))

    print(f"Started channel '{cid}' (pid={p.pid})")
    return p.pid


def start_channel(cfg):

    pass


def stop_channel(cfg):
    cid = cfg["id"]
    conf = load_config()
    HLS_ROOT = conf["paths"]["hls_root"]
    pid_file = os.path.join(HLS_ROOT, cid, f"{cid}.pid")
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


def status_channel(cfg):
    cid = cfg["id"]
    conf = load_config()
    HLS_ROOT = conf["paths"]["hls_root"]
    pid_file = os.path.join(HLS_ROOT, cid, f"{cid}.pid")
    if os.path.exists(pid_file):
        with open(pid_file) as f:
            pid = f.read().strip()
        print(f"Channel '{cid}' is running (pid={pid})")
    else:
        print(f"Channel '{cid}' is stopped")
