from Models.MessageChain.MessageChain import MessageChain
from Models.Api.BaseApi import RequestApi, ApiAdapter


class MessageApi:
    """LLOneBot 消息相关API"""

    @staticmethod
    async def sendPrivateMsg(user_id: int, message: MessageChain):
        """
        发送私聊文本消息
        Parameters:
            user_id (int): 用户QQ号
            message (MessageChain): 消息内容
        """
        param = {"user_id": user_id, "message": message.to_dict()}
        args = RequestApi("send_private_msg", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def sendGroupMsg(group_id: int, message: MessageChain):
        """
        发送群聊文本消息
        Parameters:
            group_id (int): 群号
            message (MessageChain): 消息内容
        """
        param = {"group_id": group_id, "message": message.to_dict()}
        args = RequestApi("send_group_msg", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def forwardFriendSingleMsg(user_id: int, message_id: int):
        """
        转发单条好友消息
        Parameters:
            user_id (int): 用户QQ号
            message_id (int): 消息ID
        """
        param = {"user_id": user_id, "message_id": message_id}
        args = RequestApi("forward_friend_single_msg", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def forwardGroupSingleMsg(group_id: int, message_id: int):
        """
        转发单条群消息
        Parameters:
            group_id (int): 群号
            message_id (int): 消息ID
        """
        param = {"group_id": group_id, "message_id": message_id}
        args = RequestApi("forward_group_single_msg", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getMsg(message_id: int):
        """
        获取消息详情
        Parameters:
            message_id (int): 消息ID
        """
        param = {"message_id": message_id}
        args = RequestApi("get_msg", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def deleteMsg(message_id: int):
        """
        撤回消息
        Parameters:
            message_id (int): 消息ID
        """
        param = {"message_id": message_id}
        args = RequestApi("delete_msg", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getFileInfo(file_id: str):
        """
        获取消息文件详情
        Parameters:
            file_id (str): 文件ID,上报的文件消息中有
        """
        param = {"file_id": file_id}
        args = RequestApi("get_file", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getImageInfo(file: str):
        """
        获取消息图片详情
        Parameters:
            file (str): 图片id,上报的文件消息中有
        """
        param = {"file": file}
        args = RequestApi("get_image", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getRecordInfo(file: str, out_format: str = "mp3"):
        """
        获取消息语音详情
        Parameters:
            file (str): 语音文件名
            out_format (str): 输出格式，默认mp3
        """
        param = {"file": file, "out_format": out_format}
        args = RequestApi("get_record", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setMsgEmojiLike(message_id: int, emoji_id: str):
        """
        表情回应消息（只支持群聊消息）
        Parameters:
            message_id (int): 消息ID
            emoji_id (str): 表情ID

        参考https://bot.q.qq.com/wiki/develop/api-v2/openapi/emoji/model.html#EmojiType
        """
        param = {"message_id": message_id, "emoji_id": emoji_id}
        args = RequestApi("set_msg_emoji_like", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def unsetMsgEmojiLike(message_id: int, emoji_id: str):
        """
        取消消息表情回应（只支持群聊消息）
        Parameters:
            message_id (int): 消息ID
            emoji_id (str): 表情ID
        """
        param = {"message_id": message_id, "emoji_id": emoji_id}
        args = RequestApi("unset_msg_emoji_like", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getFriendMsgHistory(user_id: int):
        """
        获取好友历史消息记录
        Parameters:
            user_id (int): 用户QQ号
            message_seq (int): 消息序号（可选）
            count (int): 获取消息数量，默认20条
        """
        param = {"user_id": user_id}
        args = RequestApi("get_friend_msg_history", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getGroupMsgHistory(
        group_id: int, message_seq: int | None = None, count: int = 20
    ):
        """
        获取群历史消息
        Parameters:
            group_id (int): 群号
            message_seq (int): 消息序号（可选）
            count (int): 获取消息数量，默认20条
        """
        param = {"group_id": group_id, "count": count}
        if message_seq is not None:
            param["message_seq"] = message_seq
        args = RequestApi("get_group_msg_history", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getForwardMsg(message_id: int):
        """
        获取转发消息详情
        Parameters:
            message_id (int): 转发消息ID
        """
        param = {"message_id": message_id}
        args = RequestApi("get_forward_msg", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def markMsgAsRead(message_id: int):
        """
        标记消息已读
        Parameters:
            message_id (int): 消息ID
        """
        param = {"message_id": message_id}
        args = RequestApi("mark_msg_as_read", param)
        return await ApiAdapter.sendActionApi(args, 10)
