#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
from handlers import registry_manager as rm
from handlers import playback_manager as pm
from handlers import channel_manager as cm


def main():
    parser = argparse.ArgumentParser(
        prog="channel-manager",
        description="Manage HLS channels via ffmpeg")
    sub = parser.add_subparsers(dest='command', required=True)

    # Add command
    p_add = sub.add_parser('add', help='Add a new channel')
    p_add.add_argument('id', help='Channel ID')
    p_add.add_argument('name', help='Display name for the channel')
    p_add.add_argument('path', help='Path to media directory or playlist file')

    # List command
    sub.add_parser('list', help='List all configured channels')

    # Start command
    p_start = sub.add_parser('start', help='Start a channel')
    p_start.add_argument('id', help='Channel ID to start')

    # Stop command
    p_stop = sub.add_parser('stop', help='Stop a channel')
    p_stop.add_argument('id', help='Channel ID to stop')

    # Restart command
    p_restart = sub.add_parser('restart', help='Restart a channel')
    p_restart.add_argument('id', help='Channel ID to restart')

    # Status command
    p_status = sub.add_parser('status', help='Show status of channels')
    p_status.add_argument('id', nargs='?', help='Channel ID (omit for all)')

    # Run command
    p_run = sub.add_parser('run', help='Start one or more channels')
    p_run.add_argument('ids', nargs='*', help='Channel IDs (omit for all)')

    args = parser.parse_args()
    registry = rm.load_registry()

    if args.command == 'add':
        cm.add_channel(args.id, args.name, args.path)

    elif args.command == 'list':
        for cfg in registry:
            print(cfg["id"])

    elif args.command == 'start':
        cfg = next((cfg for cfg in registry if cfg["id"] == args.id), None)
        if not cfg:
            print(f"Unknown channel: {args.id}")
            sys.exit(1)
        pm.start_channel(cfg)

    elif args.command == 'stop':
        cfg = next((cfg for cfg in registry if cfg["id"] == args.id), None)
        if not cfg:
            print(f"Unknown channel: {args.id}")
            sys.exit(1)
        pm.stop_channel(cfg)

    elif args.command == 'restart':
        cfg = next((cfg for cfg in registry if cfg["id"] == args.id), None)
        if not cfg:
            print(f"Unknown channel: {args.id}")
            sys.exit(1)
        pm.restart_channel(cfg)

    elif args.command == 'status':
        if args.id:
            cfg = next((cfg for cfg in registry if cfg["id"] == args.id), None)
            if not cfg:
                print(f"Unknown channel: {args.id}")
                sys.exit(1)
            cm.status_channel(cfg)
        else:
            for cfg in registry:
                cm.status_channel(cfg)

    elif args.command == 'run':
        targets = args.ids or [cfg["id"] for cfg in registry]
        for target_id in targets:
            cfg = next(
                (cfg for cfg in registry if cfg["id"] == target_id), None)
            if not cfg:
                print(f"Unknown channel: {target_id}")
                continue
            pm.start_channel(cfg)


if __name__ == '__main__':
    main()
