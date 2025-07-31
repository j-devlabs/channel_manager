import sys
from pathlib import Path
from utils import logger as logger
from utils.config_reader import load_config
from handlers.playback_manager import launch_ffmpeg_media_dir_loop


if __name__ == "__main__":
    media_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    recursive = bool(sys.argv[3]) if len(sys.argv) > 3 else False
    if not media_dir or not out_dir:
        logger.log(
            "Usage: python run_channel.py <media_dir> <output_dir> <recursive>")
        sys.exit(1)

    conf = load_config()
    SEGMENT_TIME = conf["HLS"]["SEGMENT_TIME"]
    LIST_SIZE = conf["HLS"]["LIST_SIZE"]
    try:
        launch_ffmpeg_media_dir_loop(Path(media_dir), Path(
            out_dir), recursive, int(SEGMENT_TIME), int(LIST_SIZE))
    except Exception as e:
        logger.log(f"Error launching ffmpeg: {e}")
        sys.exit(1)
