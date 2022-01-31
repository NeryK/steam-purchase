"""Module entry point"""
import os
import argparse
import pathlib
from steampurch import __doc__, __version__
from steampurch import htmlhistory


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input", help="Steam account purchase history HTML file", required=True)
    parser.add_argument("-o", "--output", default=None, help="Output JSON file", required=False)
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args()

    print("Steam purchase history parsing start.")
    data = htmlhistory.read_html_file(args.input)
    #for d in data:
    #    print(d)
    if args.output:
        htmlhistory.write_json_file(args.output, data)
    print("Steam purchase history parsing end.")
