"""Module entry point"""
import argparse
from steampurch import __doc__, __version__
from steampurch import htmlhistory, export


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input", help="Steam account purchase history HTML file", required=True)
    parser.add_argument("-j", "--json-output", default=None, help="Output JSON file")
    parser.add_argument("-c", "--csv-output", default=None, help="Output CSV file")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args()

    print("Steam purchase history parsing start.")
    data = htmlhistory.read_html_file(args.input)
    #for d in data:
    #    print(d)
    if args.json_output:
        export.write_json_file(args.json_output, data)
    if args.csv_output:
        export.write_csv_file(args.csv_output, data)
    print("Steam purchase history parsing end.")
