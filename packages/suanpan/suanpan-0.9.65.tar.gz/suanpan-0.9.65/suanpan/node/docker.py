# coding=utf-8
from __future__ import absolute_import, print_function

from lostc import collection as lcc
from suanpan.node.base import BaseNode, Param, Port


class DockerNode(BaseNode):
    def formatNodeInfo(self, nodeInfo):
        ports = {p["uuid"]: p for p in nodeInfo.get("ports", [])}
        node = lcc.classify(
            nodeInfo.get("params", []),
            inputs=lambda p: p.get("defInPortUuid", "").startswith("in"),
            outputs=lambda p: p.get("defOutPortUuid", "").startswith("out"),
            params=lambda p: "defInPortUuid" not in p and "defOutPortUuid" not in p,
        )
        inputs = {
            i["name"]: Port(
                uuid=i["defInPortUuid"],
                name=i["name"],
                type=ports[i["defInPortUuid"]]["type"],
                subtype=ports[i["defInPortUuid"]]["subType"],
            )
            for i in node["inputs"]
        }
        outputs = {
            o["name"]: Port(
                uuid=o["defOutPortUuid"],
                name=o["name"],
                type=ports[o["defOutPortUuid"]]["type"],
                subtype=ports[o["defOutPortUuid"]]["subType"],
            )
            for o in node["outputs"]
        }
        params = {
            p["name"]: Param(uuid=p["controlInstUuid"], name=p["name"], type=p["type"])
            for p in node["params"]
        }
        return {"inputs": inputs, "outputs": outputs, "params": params}
