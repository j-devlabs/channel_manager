from pathlib import Path
import random
from utils.config_reader import load_config

conf = load_config()
CHAN_ROOT = Path(conf["Paths"]["CHAN_ROOT"])
MASTER_PLAYLIST = Path(conf["Paths"]["MASTER_PLAYLIST"])
HOST_URL = conf["Server"]["HOST_URL"]
VIDEO_EXTS = [ext.strip()
                for ext in conf["Video"]["VIDEO_EXTS"].split(",")]

def build_playlist(cid: str, media_dir: str, recursive: bool) -> Path:
    """
    Build a shuffled FFmpeg concat file (list.txt) for a channel.
    Escapes spaces and single quotes in paths.
    """
    out = CHAN_ROOT/cid/"playlist.txt"
    root = Path(media_dir)
    iterator = root.rglob("*") if recursive else root.glob("*")

    files = [
        p for p in iterator
        if p.is_file() and not p.stem.startswith("._") and p.suffix.lower() in VIDEO_EXTS
    ]
    random.shuffle(files)

    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        for p in files:
            raw = str(p.resolve())
            escaped = raw.replace("\\", "\\\\") \
                         .replace(" ", "\\ ") \
                         .replace("'", "\\'")
            f.write(f"file {escaped}\n")
    return out

def get_media_files(media_dir: Path, recursive: bool) -> list[Path]:
    """
    Build a shuffled FFmpeg concat file (list.txt) for a channel.
    Escapes spaces and single quotes in paths.
    """
    root = Path(media_dir)
    iterator = root.rglob("*") if recursive else root.glob("*")

    files = [
        p for p in iterator
        if p.is_file() and not p.stem.startswith("._") and p.suffix.lower() in VIDEO_EXTS
    ]
    random.shuffle(files)
    return files

def add_to_master(cid: str, chan_name: str) -> None:
    """
    Add a channel stream to the master playlist.
    """
    with open(MASTER_PLAYLIST, "a") as f:
        f.write(f"#EXTINF:-1, tvg-id=\"{cid}\" tvg-name=\"{chan_name}\",{chan_name}\n")
        f.write(f"{HOST_URL}/{cid}/index.m3u8\n")