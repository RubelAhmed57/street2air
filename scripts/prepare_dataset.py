#!/usr/bin/env python3
"""Small helper to inspect and prepare example dataset files."""
import argparse
from pathlib import Path


def list_files(root: Path):
    for p in sorted(root.rglob('*')):
        print(p.relative_to(root))


def main():
    parser = argparse.ArgumentParser(description='Prepare/list Street2Air dataset examples')
    parser.add_argument('--root', default='.', help='Dataset root')
    parser.add_argument('--list', action='store_true', help='List all files')
    args = parser.parse_args()

    root = Path(args.root)
    if args.list:
        list_files(root)


if __name__ == '__main__':
    main()
