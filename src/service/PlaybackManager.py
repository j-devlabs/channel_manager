
import os
import subprocess
import signal

from main import HLS_ROOT
# Start a single channel: spawn ffmpeg in background, record its PID


class PlaybackManager:

    @staticmethod
    def start_channel(cfg):
        cid = cfg["id"]
        out_dir = os.path.join(HLS_ROOT, cid)
        os.makedirs(out_dir, exist_ok=True)

        # Build ffmpeg command
        cmd = [
            "ffmpeg",
            *cfg.get("input_args", []),
            "-hls_segment_type", "mpegts",
            "-hls_time", str(cfg.get("hls_time", 10)),
            os.path.join(out_dir, "index.m3u8")
        ]

        # Open log files
        stdout_log = cfg.get(
            "log_stdout", os.path.join(out_dir, f"{cid}.out.log"))
        stderr_log = cfg.get(
            "log_stderr", os.path.join(out_dir, f"{cid}.err.log"))

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

    @staticmethod
    def stop_channel(cfg):
        cid = cfg["id"]
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

    @staticmethod
    def restart_channel(cfg):
        PlaybackManager.stop_channel(cfg)
        PlaybackManager.start_channel(cfg)

    @staticmethod
    def status_channel(cfg):
        cid = cfg["id"]
        pid_file = os.path.join(HLS_ROOT, cid, f"{cid}.pid")
        if os.path.exists(pid_file):
            with open(pid_file) as f:
                pid = f.read().strip()
            print(f"Channel '{cid}' is running (pid={pid})")
        else:
            print(f"Channel '{cid}' is stopped")
