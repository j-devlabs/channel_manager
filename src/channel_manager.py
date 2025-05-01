from pathlib import Path
import registry_manager as rm


def add_channel(chan_id: str, display_name: str, media_path: str):
    reg = rm.load_registry()
    if any(cfg["id"] == chan_id for cfg in reg):
        print(f"🔔 Channel '{chan_id}' already exists.")
        return
    p = Path(media_path)
    if not p.is_dir():
        print(f"❌ Invalid media path: {media_path}")
        return

    reg.append({
        "id": chan_id,
        "name": display_name,
        "media_dir": str(p.resolve()),
        "recursive": False
    })
    rm.save_registry(reg)

    print(f"✅ Added channel '{chan_id}' → '{display_name}' @ {media_path}")
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
