# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.screenshot.base import ScreenshotIndexSaver
from suanpan.state.arguments import StorageSaverArg


class Screenshot(StorageSaverArg):
    STATE_CLASS = ScreenshotIndexSaver
    STATE_PATTERN = "{index}.png"
