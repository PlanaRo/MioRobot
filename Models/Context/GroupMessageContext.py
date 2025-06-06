from Models.Api.MessageApi import MessageApi
from Models.Event.GroupMessageEvent import GroupMessageEvent
from Models.Context.MessageContext import MessageContext, Commands
from Models.MessageChain.Message import Text
from Models.MessageChain.MessageChain import MessageChain
from Utils.Trigger import MessageTrigger


class GroupCommands(Commands[GroupMessageEvent]):
    Trigger: MessageTrigger
    messageData: GroupMessageEvent

    def __init__(self, event: GroupMessageEvent) -> None:
        self.Trigger = MessageTrigger()
        self.messageData = event

    async def SendGroupMessage(self, group_id: int, message: MessageChain):
        """
        发送群聊文本消息
        Parameters:
            group_id (int): 群号
            message (MessageChain): 消息内容
        """
        self.Trigger.update()
        await MessageApi.sendGroupMsg(group_id, message)

    async def SendPrivateMessage(self, qq: int, message: MessageChain):
        """
        发送私聊文本消息
        Parameters:
            qq (int): QQ号
            message (MessageChain): 消息内容
        """
        self.Trigger.update()
        await MessageApi.sendPrivateMsg(qq, message)

    async def forwardFriendSingleMsg(self, user_id: int, message_id: int):
        """
        转发单条好友消息
        Parameters:
            user_id (int): 用户QQ号
            message_id (int): 消息ID
        """
        self.Trigger.update()
        return await MessageApi.forwardFriendSingleMsg(user_id, message_id)

    async def forwardGroupSingleMsg(self, group_id: int, message_id: int):
        """
        转发单条群消息
        Parameters:
            group_id (int): 群号
            message_id (int): 消息ID
        """
        self.Trigger.update()
        return await MessageApi.forwardGroupSingleMsg(group_id, message_id)

    async def getMsg(self, message_id: int):
        """
        获取消息详情
        Parameters:
            message_id (int): 消息ID
        """
        self.Trigger.update()
        return await MessageApi.getMsg(message_id)

    async def deleteMsg(self, message_id: int):
        """
        撤回消息
        Parameters:
            message_id (int): 消息ID
        """
        self.Trigger.update()
        return await MessageApi.deleteMsg(message_id)

    async def getFileInfo(self, file_id: str):
        """
        获取消息文件详情
        Parameters:
            file_id (str): 文件ID,上报的文件消息中有
        """
        self.Trigger.update()
        return await MessageApi.getFileInfo(file_id)

    async def getImageInfo(self, file: str):
        """
        获取消息图片详情
        Parameters:
            file (str): 图片id,上报的文件消息中有
        """
        self.Trigger.update()
        return await MessageApi.getImageInfo(file)

    async def getRecordInfo(self, file: str, out_format: str = "mp3"):
        """
        获取消息语音详情
        Parameters:
            file (str): 语音文件名
            out_format (str): 输出格式，默认mp3
        """
        self.Trigger.update()
        return await MessageApi.getRecordInfo(file, out_format)

    async def setMsgEmojiLike(self, message_id: int, emoji_id: str):
        """
        表情回应消息（只支持群聊消息）
        Parameters:
            message_id (int): 消息ID
            emoji_id (str): 表情ID

        参考https://bot.q.qq.com/wiki/develop/api-v2/openapi/emoji/model.html#EmojiType
        """
        self.Trigger.update()
        return await MessageApi.setMsgEmojiLike(message_id, emoji_id)

    async def unsetMsgEmojiLike(self, message_id: int, emoji_id: str):
        """
        取消消息表情回应（只支持群聊消息）
        Parameters:
            message_id (int): 消息ID
            emoji_id (str): 表情ID
        """
        self.Trigger.update()
        return await MessageApi.unsetMsgEmojiLike(message_id, emoji_id)

    async def getFriendMsgHistory(self, user_id: int):
        """
        获取好友历史消息记录
        Parameters:
            user_id (int): 用户QQ号
            message_seq (int): 消息序号（可选）
            count (int): 获取消息数量，默认20条
        """
        self.Trigger.update()
        return await MessageApi.getFriendMsgHistory(user_id)

    async def getGroupMsgHistory(
        self, group_id: int, message_seq: int | None = None, count: int = 20
    ):
        """
        获取群历史消息
        Parameters:
            group_id (int): 群号
            message_seq (int): 消息序号（可选）
            count (int): 获取消息数量，默认20条
        """
        self.Trigger.update()
        return await MessageApi.getGroupMsgHistory(group_id, message_seq, count)

    async def getForwardMsg(self, message_id: int):
        """
        获取转发消息详情
        Parameters:
            message_id (int): 转发消息ID
        """
        self.Trigger.update()
        return await MessageApi.getForwardMsg(message_id)

    async def markMsgAsRead(self, message_id: int):
        """
        标记消息已读
        Parameters:
            message_id (int): 消息ID
        """
        self.Trigger.update()
        return await MessageApi.markMsgAsRead(message_id)

    async def Reply(self, message: MessageChain | str):
        """
        快捷回复
        """
        if isinstance(message, str):
            message = MessageChain().add(Text(message))

        if self.messageData.Group:

            await self.SendGroupMessage(self.messageData.Group, message)

        else:
            await self.SendPrivateMessage(self.messageData.QQ, message)


class GroupMessageContext(MessageContext[GroupMessageEvent]):
    Event: GroupMessageEvent
    Command: Commands[GroupMessageEvent]

    def __init__(self, event: GroupMessageEvent):
        self.Command = GroupCommands(event)  # 显式初始化 Command 属性
        self.Event = event
