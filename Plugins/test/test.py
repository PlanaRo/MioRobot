from functools import singledispatchmethod
from Models.Context.GroupMessageContext import GroupMessageContext
from Plugin import Plugin


class MyPlugin(Plugin):
    def init(self):
        pass

    @singledispatchmethod
    async def run(self, context: GroupMessageContext):

        if context.Event.Message[0] == "测试":
            await context.Command.Reply("测试成功")

    def dispose(self) -> None:
        pass
