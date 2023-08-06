# coding=utf-8
from __future__ import absolute_import, print_function

import base64
import copy
import os
import re
from collections import namedtuple

from suanpan.log import logger
from suanpan.objects import HasName
from suanpan.utils import json

Param = namedtuple("Param", ["uuid", "name", "type"])
Port = namedtuple("Port", ["uuid", "name", "type", "subtype"])


class BaseNode(HasName):
    NODE_INFO_KEY = "SP_NODE_INFO"
    DEFAULT_NODE_INFO = {"info": {}, "inputs": {}, "outputs": {}, "params": {}}

    def __init__(self):
        super(BaseNode, self).__init__()
        self._node = self.load()

    def __getattr__(self, key):
        if re.match(r"in\d+", key):
            collection = "inputs"
        elif re.match(r"out\d+", key):
            collection = "outputs"
        else:
            collection = "params"
        if key not in self._node[collection]:
            raise Exception("{} {} not contains {}".format(self.name, collection, key))
        return self._node[collection][key]

    @property
    def info(self):
        return self._node["info"]

    @property
    def inputs(self):
        return self._node["inputs"].values()

    @property
    def ins(self):
        return self._node["inputs"].values()

    @property
    def outputs(self):
        return self._node["outputs"].values()

    @property
    def outs(self):
        return self._node["outputs"].values()

    @property
    def params(self):
        return self._node["params"].values()

    def loadFromEnv(self):
        nodeInfoBase64 = os.environ.get(self.NODE_INFO_KEY, "")
        logger.debug("{}(Base64)='{}'".format(self.NODE_INFO_KEY, nodeInfoBase64))
        nodeInfoString = base64.b64decode(nodeInfoBase64).decode()
        nodeInfo = json.loads(nodeInfoString)
        return nodeInfo

    def formatNodeInfo(self, nodeInfo):
        raise NotImplementedError("Method not implemented!")

    def defaultNodeInfo(self):
        return copy.deepcopy(self.DEFAULT_NODE_INFO)

    def _updateInfo(self, *infos):
        result = self.defaultNodeInfo()
        keys = result.keys()
        for info in infos:
            for key in keys:
                result[key].update(info[key])
        return result

    def load(self):
        return self._updateInfo(self.formatNodeInfo(self.loadFromEnv()))
