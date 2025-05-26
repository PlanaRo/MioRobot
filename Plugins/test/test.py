from functools import singledispatchmethod
from Models.Context.GroupMessageContext import GroupMessageContext
from Core.Plugin import Plugin
from Models.MessageChain.Message import Text
from Models.MessageChain.MessageChain import MessageChain


class MyPlugin(Plugin):

    @singledispatchmethod
    async def run(self, context: GroupMessageContext):

        if context.Event.Message[0] == "测试":
            messageChain = MessageChain().add(Text("测试成功"))
            await context.Command.Reply(messageChain)

    def dispose(self) -> None:
        pass
