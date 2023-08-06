# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.storage import storage
from suanpan.state.base import Saver, IndexSaver, TimeSaver
from suanpan.utils import image


class StorageSaver(Saver):
    PATTERN = None

    def __init__(self, name, **kwargs):
        super(StorageSaver, self).__init__(storageName=name, **kwargs)

    @property
    def currentPattern(self):
        _pattern = self.current.pattern or self.PATTERN
        if not _pattern:
            raise Exception("Pattern is not set!")
        return _pattern.format(**self.current)

    def update(self):
        self.current.localPath = storage.getPathInTempStore(self.current.storageName)
        storageName = storage.storagePathJoin(self.current.storageName, self.currentPattern)
        localPath = storage.localPathJoin(self.current.localPath, self.currentPattern)
        return storage.upload(storageName, localPath)


class StorageIndexSaver(StorageSaver, IndexSaver):
    pass


class StorageTimeSaver(StorageSaver, TimeSaver):
    pass


class ScreenshotSaver(StorageSaver):
    def update(self, data):
        self.current.localPath = storage.getPathInTempStore(self.current.storageName)
        storageName = storage.storagePathJoin(self.current.storageName, self.currentPattern)
        localPath = storage.localPathJoin(self.current.localPath, self.currentPattern)
        image.save(localPath, data, self.current.get("flag"))
        return storage.upload(storageName, localPath)


class ScreenshotIndexSaver(ScreenshotSaver, IndexSaver):
    PATTERN = "screenshot_{index}.png"


class ScreenshotTimeSaver(ScreenshotSaver, TimeSaver):
    PATTERN = "screenshot_{time}.png"
