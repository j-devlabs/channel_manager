import configparser
import sys
import argparse
from pathlib import Path
import services.registry_manager as rm
import services.playback_manager as pm

# # region ─── CONFIGURATION ───────────────────────────────────────
# TIME_ZONE = "America/Puerto_Rico"  # UTC−4
# CONFIG_ROOT = Path("/opt/xhubsrc/config")
# CONCAT_ROOT = Path("/opt/vlc/channels")
# HLS_ROOT = Path("/opt/vlc/streams")

# REGISTRY_FILE = CONFIG_ROOT / "channels.json"
# MASTER_PLAYLIST = HLS_ROOT / "master.m3u"
# XMLTV_FILE = HLS_ROOT / "guide.xml"

# HOST_URL = "http://localhub.local:8090/live"
# VIDEO_EXTS = {".mp4", ".mkv", ".avi", ".mov", ".flv", ".ts", ".webm"}
# SEGMENT_TIME = 10   # seconds per segment
# LIST_SIZE = 6    # number of segments in the live .m3u8
# # endregion


def load_config():
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent.parent / "config.ini")
    return config

def main():
    parser = argparse.ArgumentParser(
        description="Manage HLS channels via ffmpeg")
    sub = parser.add_subparsers(dest='command', required=True)

    sub.add_parser('list', help='List all configured channels')

    p_start = sub.add_parser('start', help='Start a channel')
    p_start.add_argument('id', help='Channel ID to start')

    p_stop = sub.add_parser('stop', help='Stop a channel')
    p_stop.add_argument('id', help='Channel ID to stop')

    p_restart = sub.add_parser('restart', help='Restart a channel')
    p_restart.add_argument('id', help='Channel ID to restart')

    p_status = sub.add_parser('status', help='Show status of channels')
    p_status.add_argument('id', nargs='?', help='Channel ID (omit for all)')

    p_run = sub.add_parser('run', help='Start one or more channels')
    p_run.add_argument('ids', nargs='*', help='Channel IDs (omit for all)')

    args = parser.parse_args()
    registry = rm.load_registry()

    if args.command == 'list':
        for cid in registry:
            print(cid)

    elif args.command == 'start':
        cfg = registry.get(args.id)
        if not cfg:
            print(f"Unknown channel: {args.id}")
            sys.exit(1)
        pm.start_channel(cfg)

    elif args.command == 'stop':
        cfg = registry.get(args.id)
        if not cfg:
            print(f"Unknown channel: {args.id}")
            sys.exit(1)
        pm.stop_channel(cfg)

    elif args.command == 'restart':
        cfg = registry.get(args.id)
        if not cfg:
            print(f"Unknown channel: {args.id}")
            sys.exit(1)
        pm.restart_channel(cfg)

    elif args.command == 'status':
        if args.id:
            cfg = registry.get(args.id)
            if not cfg:
                print(f"Unknown channel: {args.id}")
                sys.exit(1)
            pm.status_channel(cfg)
        else:
            for cfg in registry.values():
                pm.status_channel(cfg)

    elif args.command == 'run':
        targets = args.ids or list(registry.keys())
        for cid in targets:
            cfg = registry.get(cid)
            if not cfg:
                print(f"Unknown channel: {cid}")
                continue
            pm.start_channel(cfg)


if __name__ == '__main__':
    main()
