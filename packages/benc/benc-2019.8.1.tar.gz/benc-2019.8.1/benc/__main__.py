import argparse
import json
import sys

import benc


def action(data):
    if len(data) > 1 and data[0] in {"i", "l", "d"}:
        pass
        # decode(data)
    else:
        sys.stdout.buffer.write(benc.bencode(json.loads(data)))
        sys.stdout.buffer.write(b'\n')


def main() -> None:
    parser = argparse.ArgumentParser(prog='benc', description="benocde decoder and encoder")
    parser.add_argument('data', help="JSON object to bencode or bencode object to decode.")
    parser.add_argument('--version', action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.version:
        print("benc", benc.__version__)
    if args.data:
        sys.exit(action(args.data))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
