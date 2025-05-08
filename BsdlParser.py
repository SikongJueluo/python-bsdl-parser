#!/usr/bin/env python3
#
# python-bsdl-parser
#
# Copyright (c) 2016, Forest Crossman <cyrozap@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#


import sys

from lark import Lark, Token, Tree

EBNF_FILE_PATH = "./bsdl.lark"


class BSDL:
    @staticmethod
    def bsdlParser() -> Lark:
        with open(EBNF_FILE_PATH, "r", encoding="utf-8") as file:
            ebnfContent = file.read()
        return Lark(ebnfContent)

    @staticmethod
    def ast_to_yaml(node, indent=""):
        indent += "  "
        if node is None:
            return
        elif isinstance(node, Token):
            yield f"{indent}- type: {node.type}"
            yield f"{indent}  value: {repr(node.value)}"
        elif isinstance(node, Tree):
            yield f"{indent}- type: {node.data}"

            if len(node.children) == 1:
                child = node.children[0]
                # 处理同名字符串
                if isinstance(child, Token) and child.type.lower() == str(child.value).lower():
                    yield f"{indent}  value: {repr(child.value)}"
                    return

            if len(node.children) > 0:
                # 处理正则表达式名称
                isAllRegexp = True
                for child in node.children:
                    if not isinstance(child, Token) or not (child.type[:7] == "__ANON_"):
                        isAllRegexp = False
                        break
                if isAllRegexp:
                    for child in node.children:
                        yield f"{indent}  value: {repr(child.value)}"
                    return

                # 处理其余情况
                yield f"{indent}  children:"
                for child in node.children:
                    yield from BSDL.ast_to_yaml(child, indent)
        

def main(filename):
    with open(filename) as f:
        text = f.read()
        parser = BSDL.bsdlParser()
        ast = parser.parse(text)
        for line in BSDL.ast_to_yaml(ast):
            print(line)


if __name__ == "__main__":
    main(sys.argv[1])
