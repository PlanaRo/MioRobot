from functools import singledispatchmethod, singledispatch
from Models.Event.BaseEvent import BaseEvent
from Models.Event.GroupMessageEvent import GroupMessageEvent
from Models.Context.GroupMessageContext import GroupMessageContext


class MessageContextBuild:

    @singledispatch
    @staticmethod
    def build(data) -> None | GroupMessageContext:
        return None

    @build.register
    @staticmethod
    def _(data: GroupMessageEvent) -> GroupMessageContext:
        return GroupMessageContext(data)
