from pathlib import Path
import random
from utils.config_reader import load_config


def build_playlist(cid: str, media_dir: str, recursive: bool) -> Path:
    """
    Build a shuffled FFmpeg concat file (list.txt) for a channel.
    Escapes spaces and single quotes in paths.
    """
    conf = load_config()
    CHAN_ROOT = Path(conf["Paths"]["CHAN_ROOT"])
    VIDEO_EXTS = [ext.strip()
                  for ext in conf["Video"]["VIDEO_EXTS"].split(",")]

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
