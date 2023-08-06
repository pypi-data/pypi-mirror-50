# coding=utf-8
from __future__ import absolute_import, print_function

import os

from suanpan.proxy import Proxy

TYPE = os.environ.get("SP_SCREENSHOT_TYPE", "index")
PATTERN = os.environ.get("SP_SCREENSHOT_PATTERN")
STORAGE_KEY = os.environ.get("SP_SCREENSHOT_STORAGE_KEY")


class Screenshot(Proxy):
    MAPPING = {
        "index": "suanpan.state.storage.ScreenshotIndexSaver",
        "time": "suanpan.state.storage.ScreenshotTimeSaver",
    }
    DEFAULT_PATTERN_MAPPING = {"index": "{index}.png", "time": "{time}.png"}

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("type", TYPE)
        kwargs.setdefault("name", STORAGE_KEY)
        kwargs.setdefault(
            "pattern", PATTERN or self.DEFAULT_PATTERN_MAPPING.get(kwargs["type"])
        )
        super(Screenshot, self).__init__()
        self.setBackend(*args, **kwargs)


screenshot = Screenshot()
