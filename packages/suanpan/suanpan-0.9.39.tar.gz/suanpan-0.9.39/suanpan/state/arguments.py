# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan import path
from suanpan.arguments import Arg
from suanpan.log import logger
from suanpan.state.storage import StorageIndexSaver, ScreenshotIndexSaver
from suanpan.storage import storage


class StateArg(Arg):
    pass


class StorageLoaderArg(StateArg):
    STATE_CLASS = StorageIndexSaver
    STATE_PATTERN = "storage_{index}"

    def __init__(self, *args, **kwargs):
        super(StorageLoaderArg, self).__init__(*args, **kwargs)
        self.loader = None
        self.folderName = None
        self.folderPath = None

    def load(self, args):
        self.folderName = super(StorageLoaderArg, self).load(args)
        if self.folderName:
            self.folderPath = storage.getPathInTempStore(self.folderName)
            self.loader = self.STATE_CLASS(
                name=self.folderName, pattern=self.STATE_PATTERN
            )
        if self.folderPath:
            path.mkdirs(self.folderPath)
        self.value = self.loader
        return self.value

    def clean(self, context):
        raise NotImplementedError(
            "{} can't be set as output argument.".format(self.name)
        )


class StorageSaverArg(StateArg):
    STATE_CLASS = StorageIndexSaver
    STATE_PATTERN = "storage_{index}"

    def __init__(self, *args, **kwargs):
        super(StorageSaverArg, self).__init__(*args, **kwargs)
        self.saver = None
        self.folderName = None
        self.folderPath = None

    def load(self, args):
        self.folderName = super(StorageSaverArg, self).load(args)
        if self.folderName:
            self.folderPath = storage.getPathInTempStore(self.folderName)
            self.saver = self.STATE_CLASS(
                name=self.folderName, pattern=self.STATE_PATTERN
            )
        if self.folderPath:
            path.mkdirs(self.folderPath)
        self.value = self.saver
        return self.value

    def format(self, context):
        raise NotImplementedError(
            "{} can be set as output argument only.".format(self.name)
        )

    def clean(self, context):
        if self.folderPath:
            path.empty(self.folderPath)
        return self.folderPath

    def save(self, context, result):
        logger.info("Saving: ({}) Nothing to do!".format(self.name))


class Screenshot(StorageSaverArg):
    STATE_CLASS = ScreenshotIndexSaver
    STATE_PATTERN = "screenshot_{index}.png"
