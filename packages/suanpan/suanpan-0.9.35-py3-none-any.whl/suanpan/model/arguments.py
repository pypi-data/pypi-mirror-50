# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.components import Result
from suanpan.storage.arguments import Folder


class CommonModel(Folder):
    def __init__(self, key, type, **kwargs):
        self.modelType = type
        self.model = self.modelType()
        super(CommonModel, self).__init__(key, **kwargs)

    def load(self, args):
        super(CommonModel, self).load(args)
        if self.folderPath:
            self.value = self.model
        return self.value

    def format(self, context):
        super(CommonModel, self).format(context)
        if self.folderPath:
            self.model.load(self.folderPath)
            self.value = self.model
        return self.value

    def clean(self, context):
        super(CommonModel, self).clean(context)
        if self.folderPath:
            self.value = self.model
        return self.value

    def save(self, context, result):
        model = result.value
        model.save(self.folderPath)
        return super(CommonModel, self).save(
            context, Result.froms(value=self.folderPath)
        )


class HotReloadModel(CommonModel):
    def __init__(self, key, type, version="latest", **kwargs):
        super(HotReloadModel, self).__init__(key, type, **kwargs)
        self.version = version

    def format(self, context):
        if self.folderName:
            self.model.loadFrom(self.folderName, version=self.version)
            self.value = self.model
        return self.value

    def save(self, context, result):
        raise NotImplementedError("Not support save!")
