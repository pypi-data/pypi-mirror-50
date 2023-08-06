# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.node.docker import DockerNode


class StreamNode(DockerNode):
    def formatNodeInfo(self, nodeInfo):
        nodeInfo["params"] = [
            {"name": name, **param}
            for name, param in nodeInfo.get("params", {}).items()
        ]
        return super(StreamNode, self).formatNodeInfo(nodeInfo)
