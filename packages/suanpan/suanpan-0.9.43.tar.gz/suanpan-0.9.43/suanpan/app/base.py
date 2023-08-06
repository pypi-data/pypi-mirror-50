# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.objects import HasName
from suanpan.interfaces import HasInitHooks, HasCallHooks


class BaseApp(HasName, HasInitHooks, HasCallHooks):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented!")

    def start(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented!")

    @property
    def trigger(self):
        raise NotImplementedError("{} not support trigger".format(self.name))

    def input(self, argument):
        raise NotImplementedError("Method not implemented!")

    def output(self, argument):
        raise NotImplementedError("Method not implemented!")

    def param(self, argument):
        raise NotImplementedError("Method not implemented!")

    def column(self, argument):
        raise NotImplementedError("Method not implemented!")

    def beforeInit(self, hook):
        self.addBeforeInitHooks(hook)
        return hook

    def afterInit(self, hook):
        self.addAfterInitHooks(hook)
        return hook

    def beforeCall(self, hook):
        self.addBeforeCallHooks(hook)
        return hook

    def afterCall(self, hook):
        self.addAfterCallHooks(hook)
        return hook
