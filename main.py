import json
import sys
import os
import argparse
from playback import start_channel, stop_channel, restart_channel, status_channel

# Default HLS output root (same for all channels)
HLS_ROOT = os.environ.get("HLS_ROOT", "/var/www/hls")

# JSON registry file
REGISTRY_FILE = "channels.json"

# Load channel definitions


def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        print(f"Registry file {REGISTRY_FILE} not found.")
        sys.exit(1)
    with open(REGISTRY_FILE) as f:
        return json.load(f)


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
    registry = load_registry()

    if args.command == 'list':
        for cid in registry:
            print(cid)

    elif args.command == 'start':
        cfg = registry.get(args.id)
        if not cfg:
            print(f"Unknown channel: {args.id}")
            sys.exit(1)
        start_channel(cfg)

    elif args.command == 'stop':
        cfg = registry.get(args.id)
        if not cfg:
            print(f"Unknown channel: {args.id}")
            sys.exit(1)
        stop_channel(cfg)

    elif args.command == 'restart':
        cfg = registry.get(args.id)
        if not cfg:
            print(f"Unknown channel: {args.id}")
            sys.exit(1)
        restart_channel(cfg)

    elif args.command == 'status':
        if args.id:
            cfg = registry.get(args.id)
            if not cfg:
                print(f"Unknown channel: {args.id}")
                sys.exit(1)
            status_channel(cfg)
        else:
            for cfg in registry.values():
                status_channel(cfg)

    elif args.command == 'run':
        targets = args.ids or list(registry.keys())
        for cid in targets:
            cfg = registry.get(cid)
            if not cfg:
                print(f"Unknown channel: {cid}")
                continue
            start_channel(cfg)


if __name__ == '__main__':
    main()
