import os
from pathlib import Path
from . import registry_manager as rm
from utils.config_reader import load_config


def add_channel(chan_id: str, display_name: str, media_path: str):
    reg = rm.load_registry()
    if any(cfg["id"] == chan_id for cfg in reg):
        print(f"🔔 Channel '{chan_id}' already exists.")
        return False

    p = Path(media_path)
    if not p.exists():
        print(f"❌ Path does not exist: {media_path}")
        return False

    config = load_config()
    video_exts = [ext.strip() for ext in config.get(
        'Video', 'VIDEO_EXTS', fallback='.mp4,.mkv,.avi').split(',')]

    entry = {
        "id": chan_id,
        "name": display_name,
        "recursive": False
    }

    if p.is_file():
        if p.suffix not in video_exts and p.suffix != '.m3u8':
            print(
                f"❌ Invalid file type: {p.suffix}. Must be a video file {video_exts} or playlist (.m3u8)")
            return False
        entry["media_file"] = str(p.resolve())
        print(
            f"✅ Added channel '{chan_id}' → '{display_name}' with media file: {media_path}")
    else:  # is directory
        entry["media_dir"] = str(p.resolve())
        print(
            f"✅ Added channel '{chan_id}' → '{display_name}' with media directory: {media_path}")

    reg.append(entry)  # Add the new entry to the registry
    rm.save_registry(reg)
    return True


def delete_channel(self, channel_id):
    """
    Delete an existing channel.

    Args:
        channel_id (int): The ID of the channel to delete.

    Returns:
        bool: True if the channel was deleted successfully, False otherwise.
    """
    pass


def get_channel(self, channel_id):
    """
    Retrieve details of a specific channel.

    Args:
        channel_id (int): The ID of the channel to retrieve.

    Returns:
        dict: A dictionary containing channel details, or None if not found.
    """
    pass


def list_channels(self):
    """
    List all available channels.

    Returns:
        list: A list of dictionaries containing channel details.
    """
    pass


def channel_is_running(cfg):
    cid = cfg["id"]
    conf = load_config()
    HLS_ROOT = conf["Paths"]["HLS_ROOT"]
    pid_file = os.path.join(HLS_ROOT, cid, f"{cid}.pid")

    if os.path.exists(pid_file):
        with open(pid_file) as f:
            try:
                pid = int(f.read().strip())
                # Check if process exists in /proc
                if os.path.exists(f"/proc/{pid}"):
                    print(f"Channel '{cid}' is running (pid={pid})")
                    return True
            except ValueError:
                pass

        # If we get here, the process is not running
        os.remove(pid_file)

    print(f"Channel '{cid}' is stopped")
    return False
