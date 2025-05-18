from BsdlParser import BsdlParser
import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        prog="BSDL Parser",  # 程序名
    )
    parser.add_argument("filename", help="BSDL file to parse", type=str)
    parser.add_argument("--output", help="Output file", type=str, default="output.json")
    parser.add_argument("--format", help="Output format", type=str, default="json")
    parser.add_argument("--type", help="Type to parse", type=str, default=None)
    parser.add_argument(
        "--method",
        help="Get special type",
        type=str,
        default=None,
    )
    parser.add_argument("--seperate", help="Separate output", type=bool, default=False)
    args = parser.parse_args()

    if args.format == "json":
        if args.method == "GetLogicPortDesp":
            bsdl_parser = BsdlParser(args.filename)
            result = bsdl_parser.GetLogicPortDesp()
            with open(args.output, "w", encoding="utf-8") as output_file:
                json.dump(result, output_file, indent=2)
        elif args.method == "GetBoundaryScanRegDesp":
            bsdl_parser = BsdlParser(args.filename)
            result = bsdl_parser.GetBoundaryScanRegDesp()
            with open(args.output, "w", encoding="utf-8") as output_file:
                json.dump(result, output_file, indent=2)
        else:
            bsdl_parser = BsdlParser(args.filename)
            bsdl_parser.ToJson(args.output, args.type, args.seperate)
    elif args.format == "str":
        if args.method == "GetLogicPortDesp":
            bsdl_parser = BsdlParser(args.filename)
            result = bsdl_parser.GetLogicPortDesp()
            print(json.dumps(result, indent=2))
        elif args.method == "GetBoundaryScanRegDesp":
            bsdl_parser = BsdlParser(args.filename)
            result = bsdl_parser.GetBoundaryScanRegDesp()
            print(json.dumps(result, indent=2))
        else:
            bsdl_parser = BsdlParser(args.filename)
            print(bsdl_parser.ToDict(args.type, args.seperate))


if __name__ == "__main__":
    main()
