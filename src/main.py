from BsdlParser import BsdlParser
import argparse
import json

def main():
    parser = argparse.ArgumentParser(
        prog='BSDL Parser', # 程序名
    )
    parser.add_argument("filename", help="BSDL file to parse", type=str)
    parser.add_argument("--output", help="Output file", type=str, default="output.json")
    parser.add_argument("--seperate", help="Separate output", type=bool, default=True)
    args = parser.parse_args()

    with open(args.filename) as f:
        text = f.read()
        parser = BsdlParser.bsdlParser()
        ast = parser.parse(text)
        if args.output.endswith(".json"):
            with open(args.output, "w") as f:
                dictValue = BsdlParser.ast_to_dict(ast, args.seperate)
                json.dump(dictValue, f, indent=2)
        


if __name__ == "__main__":
    main()
