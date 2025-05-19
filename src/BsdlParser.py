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
import json

from lark import Lark, Token, Tree

# This is the path to the EBNF file that defines the BSDL grammar.
EBNF_FILE_PATH = os.path.join(os.path.dirname(__file__), "bsdl.lark")


def NodeToDict(type: str, value, isSeperate: bool = True):
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
                    unWrappedDict[list(item.keys())[0]] = list(item.values())[0]
                else:
                    break
            if len(unWrappedDict) == len(value):
                return unWrappedDict
            else:
                return {type: value}
    elif isinstance(value, dict):
        if isSeperate:
            return dict(
                type=type,
                children=value,
            )
        else:
            if len(value) == 1 and type == list(value.keys())[0]:
                return value
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
    def __init__(self, filepath: str = None):
        self.parser = BsdlParser.Parser()
        if filepath is not None:
            self.filepath = filepath

    def ToDict(self, typeName: str = None, isSeperate: bool = False):
        if self.filepath is None:
            raise ValueError("File path is not set.")

        with open(self.filepath, "r", encoding="utf-8") as file:
            text = file.read()
            self.ast = self.parser.parse(text)
            if typeName is None:
                return BsdlParser.AstToDict(self.ast, isSeperate)
            else:
                return BsdlParser.AstToDict(
                    BsdlParser.FindType(self.ast, typeName), isSeperate
                )

    def ToJson(self, outputPath: str, typeName: str = None, isSeperate: bool = False):
        if self.filepath is None:
            raise ValueError("File path is not set.")

        with open(self.filepath, "r", encoding="utf-8") as file:
            text = file.read()
            self.ast = self.parser.parse(text)
            if typeName is None:
                dictValue = BsdlParser.AstToDict(self.ast, isSeperate)
            else:
                dictValue = BsdlParser.AstToDict(
                    BsdlParser.FindType(self.ast, typeName), isSeperate
                )
            with open(outputPath, "w", encoding="utf-8") as outputFile:
                json.dump(dictValue, outputFile, indent=2)

    def GetLogicPortDesp(self) -> dict:
        if self.filepath is None:
            raise ValueError("File path is not set.")

        with open(self.filepath, "r", encoding="utf-8") as file:
            text = file.read()
            self.ast = self.parser.parse(text)
            portDesp = BsdlParser.AstToDict(
                BsdlParser.FindType(self.ast, "logical_port_description"), False
            )["logical_port_description"]

            if portDesp is None:
                raise ValueError("No logical_port_description found in the BSDL file.")

            # 处理逻辑端口描述
            result = {}
            for item in portDesp:
                result[item["pin_spec"]["port_name"]] = {
                    "port_type": item["pin_spec"]["pin_type"],
                    "port_dimension": item["pin_spec"]["port_dimension"],
                }
            return {"port_number": len(result), "ports": result}

    def GetPinMap(self, mapName: str = None) -> dict:
        if self.filepath is None:
            raise ValueError("File path is not set.")

        with open(self.filepath, "r", encoding="utf-8") as file:
            text = file.read()
            self.ast = self.parser.parse(text)
            pinMappingList = BsdlParser.AstToDict(
                BsdlParser.FindType(self.ast, "pin_mapping_list"),
                False,
            )
            if pinMappingList is None:
                raise ValueError("No pin_mapping_list found in the BSDL file.")

            if mapName is None:
                if isinstance(pinMappingList, list):
                    pinMapping = pinMappingList[0]
                elif isinstance(pinMappingList, dict):
                    pinMapping = pinMappingList["pin_mapping"]
                else:
                    raise ValueError("No pin_mapping found in the pin_mapping_list.")
            else:
                if isinstance(pinMappingList, list):
                    pinMapping = None
                    for item in pinMappingList:
                        if item.get("pin_mapping_name") == mapName:
                            pinMapping = item
                            break

                    if pinMapping is None:
                        raise ValueError(
                            f"No pin_mapping_list found in the BSDL file with name {mapName}."
                        )
                else:
                    raise ValueError(f"No value could find {mapName}.")

            # 处理引脚映射
            result = {}
            for item in pinMapping["map_string"]:
                itemValue = item["port"].get("pin_id")
                if itemValue is None:
                    itemValue = item["port"].get("pin_list")
                if itemValue is None:
                    raise ValueError("No pin_id or pin_list found in the pin_mapping.")
                result[item["port"]["port_name"]] = itemValue

            return {"pin_map_name": pinMapping["pin_mapping_name"], "pin_map": result}

    def GetBoundaryScanRegDesp(self, usePinMap: bool = True) -> dict:
        if self.filepath is None:
            raise ValueError("File path is not set.")

        with open(self.filepath, "r", encoding="utf-8") as file:
            text = file.read()
            self.ast = self.parser.parse(text)
            boundaryScanRegDesp = BsdlParser.AstToDict(
                BsdlParser.FindType(self.ast, "boundary_scan_register_description"),
                False,
            ).get("boundary_scan_register_description")

            if boundaryScanRegDesp is None:
                raise ValueError(
                    "No boundary_scan_register_description found in the BSDL file."
                )

            if usePinMap:
                pinMap = self.GetPinMap().get("pin_map")
                if pinMap is None:
                    raise ValueError("No pin_map found in the BSDL file.")

            regsDict = {}
            for item in boundaryScanRegDesp["boundary_register_stmt"]:
                if isinstance(item, dict) and item.get("component_name") is None:
                    if usePinMap and item["cell_entry"].get("port_id") is not None:
                        item["cell_entry"]["port_id"] = pinMap.get(
                            item["cell_entry"]["port_id"]
                        )
                        if item["cell_entry"]["port_id"] is None:
                            raise ValueError(
                                f"No pin_id found in the pin_mapping for {item['cell_entry']['port_id']}."
                            )
                    regsDict[item["cell_entry"]["cell_number"]] = item["cell_entry"]
            return {
                "register_length": len(regsDict),
                "registers": list(
                    sorted(
                        regsDict.values(),
                        key=lambda x: int(x["cell_number"]),
                    )
                ),
            }

    @staticmethod
    def Parser() -> Lark:
        with open(EBNF_FILE_PATH, "r", encoding="utf-8") as file:
            ebnfContent = file.read()
        return Lark(ebnfContent)

    @staticmethod
    def AstToDict(node, isSeperate=False, _depth=0):
        if _depth == 0 and isinstance(node, Tree) and len(node.children) == 1:
            # 处理根节点
            node = node.children[0]

        _depth += 1
        if node is None:
            return
        elif isinstance(node, Token):
            # 处理正则表达式名称
            if node.type[:7] == "__ANON_":
                return str(node.value)
            # 处理字符串
            elif node.type == "ESCAPED_STRING":
                return node.value
            # 处理同名字符串
            elif node.type.lower() == str(node.value).lower():
                return str(node.value)
            return NodeToDict(node.type, node.value, isSeperate)
        elif isinstance(node, Tree):
            childrenDict = {}
            childrenList = []
            isList = False
            for child in node.children:
                childNode = BsdlParser.AstToDict(child, isSeperate, _depth)
                # 处理Null节点
                if childNode is None:
                    continue
                elif isinstance(childNode, str):
                    isList = True

                if not isList:
                    if (
                        isinstance(child, Token)
                        and childrenDict.get(child.type) is None
                    ):
                        childrenDict.update(childNode)
                    elif (
                        isinstance(child, Tree) and childrenDict.get(child.data) is None
                    ):
                        childrenDict.update(childNode)
                    else:
                        isList = True

                if isList:
                    if isinstance(child, Token):
                        childrenList.append(childNode)
                    else:
                        childrenList.append(
                            NodeToDict(child.data, childNode, isSeperate)
                        )

            if isList:
                if len(childrenDict) != 0:
                    for key, value in childrenDict.items():
                        childrenList.append(NodeToDict(key, value, isSeperate))
                # 处理单数情况
                if len(childrenList) == 1:
                    return NodeToDict(node.data, childrenList[0], isSeperate)
                else:
                    return NodeToDict(node.data, childrenList, isSeperate)
            else:
                return NodeToDict(node.data, childrenDict, isSeperate)

    @staticmethod
    def FindType(node, type_name):
        if isinstance(node, Token):
            if node.type == type_name:
                return node
            return None

        elif isinstance(node, Tree):
            if node.data == type_name:
                return node
            for child in node.children:
                result = BsdlParser.FindType(child, type_name)
                if result is not None:
                    return result
        return None
