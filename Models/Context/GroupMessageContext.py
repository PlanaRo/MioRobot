# from Models.MessageContext.MessageContext import MessageContext
from typing import Union
from Models.Api.MessageApi import MessageApi
from Models.Event.GroupMessageEvent import GroupMessageEvent
from Models.Context.MessageContext import MessageContext, Commands
from Utils.Trigger import MessageTrigger


class GroupCommands(Commands[GroupMessageEvent]):
    Trigger: MessageTrigger
    messageData: GroupMessageEvent

    def __init__(self, event: GroupMessageEvent) -> None:
        self.Trigger = MessageTrigger()
        self.messageData = event

    async def SendGroupMessage(self, message: Union[str, list, list[dict]]):
        """
        发送群消息
        """
        self.Trigger.update()
        await MessageApi.sendGroupMessage(self.messageData, message)

    async def SendPrivateMessage(self, message):
        """
        发送私聊消息
        未实现
        """
        pass
        # await MessageApi.sendPrivateMessage(self.messageData, message)

    async def Reply(self, message):
        """
        快捷回复
        """
        if self.messageData.Group:
            await self.SendGroupMessage(message)

        else:
            await self.SendPrivateMessage(message)


class GroupMessageContext(MessageContext[GroupMessageEvent]):
    Event: GroupMessageEvent
    Command: Commands[GroupMessageEvent]

    def __init__(self, event: GroupMessageEvent):
        self.Command = GroupCommands(event)  # 显式初始化 Command 属性
        self.Event = event
