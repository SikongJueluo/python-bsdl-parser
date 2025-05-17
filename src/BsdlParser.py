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


import os
from functools import singledispatch
from typing import Any

from lark import Lark, Token, Tree

# This is the path to the EBNF file that defines the BSDL grammar.
EBNF_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bsdl.lark")


@singledispatch
def node_to_dict(token: Token, isSeperate=True) -> dict[str,Any]:
    if isSeperate:
        return dict(
            type=token.type,
            value=str(token.value),
        )
    else:
        return {token.type: str(token.value)}

@node_to_dict.register
def _(type: str, value, isSeperate: bool = True):
    if isinstance(value, list):
        if isSeperate:
            return dict(
                type=type,
                children=value,
            )
        else:
            unWrappedDict = {}
            for item in value:
                if isinstance(item, dict) and len(item) == 1:
                    unWrappedDict[list(item.keys())[0]] = list( item.values() )[0]
                else:
                    break
            if len(unWrappedDict) == len(value):
                return unWrappedDict
            else:
                return {type: value}
    else:
        if isSeperate:
            return dict(
                type=type,
                value=str(value),
            )
        else:
            return {type: str(value)}


class BsdlParser:
    @staticmethod
    def bsdlParser() -> Lark:
        with open(EBNF_FILE_PATH, "r", encoding="utf-8") as file:
            ebnfContent = file.read()
        return Lark(ebnfContent)

    @staticmethod
    def ast_process(node:Tree, _depth = 0):
        if _depth == 0 and isinstance(node, Tree) and len(node.children) == 1:
            # 处理根节点
            node = node.children[0]


    @staticmethod
    def ast_to_dict(node, isSeperate=False, _depth=0):
        if _depth == 0 and isinstance(node, Tree) and len(node.children) == 1:
            # 处理根节点
            node = node.children[0]

        _depth += 1
        if node is None:
            return
        elif isinstance(node, Token):
            return node_to_dict(node, isSeperate)
        elif isinstance(node, Tree):
            if len(node.children) == 1:
                child = node.children[0]
                # 处理同名字符串
                if (
                    isinstance(child, Token)
                    and child.type.lower() == str(child.value).lower()
                ):
                    return node_to_dict(node.data, child.value, isSeperate)
            else:
                # 处理正则表达式名称
                isAllRegexp = True
                regexDict = {}
                for child in node.children:
                    if not isinstance(child, Token) or not (
                        child.type[:7] == "__ANON_"
                    ):
                        isAllRegexp = False
                        break
                    regexDict[child.type] = child.value
                if isAllRegexp:
                    return node_to_dict(node.data, regexDict, isSeperate)

                # 处理其余情况
                children = []
                for child in node.children:
                    childNode = BsdlParser.ast_to_dict(child, isSeperate, _depth)
                    if childNode is not None:
                        children.append(childNode)
                return node_to_dict(node.data, children, isSeperate)

    @staticmethod
    def find_type(node, type_name):
        if isinstance(node, Token):
            if node.type == type_name:
                return node
            return None

        elif isinstance(node, Tree):
            if node.data == type_name:
                return node
            for child in node.children:
                result = BsdlParser.find_type(child, type_name)
                if result is not None:
                    return result
        return None
