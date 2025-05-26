from Models.Event.BaseEvent import BaseEvent
from Models.Event.EventType import EventType


class PrivateMessageEvent(BaseEvent):
    """
    私聊消息事件
    """

    # 事件戳
    Time: int
    # 事件类型
    Post_Type: EventType
    # 消息类型
    Message_Type: str
    # 消息子类型，为normal
    Sub_Type: str
    # QQ号
    QQ: int
    # robot的QQ号
    Robot: int
    # 昵称
    Nickname: str
    # 私聊消息
    Message: list
    # 消息ID
    Message_ID: int | None
    # 原始消息，即带CQ码的消息
    RowMessage: str
    # 便捷消息读取
    # 消息图片
    Images: list[str]

    def __init__(self, data: dict):
        sender = data.get("sender", {})
        # 初始化基础属性
        self.Post_Type = EventType.FriendMessage
        self.Message_Type = data.get("message_type", "")
        self.Time = data.get("time", "")
        self.Sub_Type = data.get("sub_type", "")
        self.QQ = data.get("user_id", 0)
        self.Robot = data.get("self_id", 0)
        self.Nickname = sender.get("nickname")
        self.RowMessage = data.get("raw_message", "")
        self.Message_ID = data.get("message_id", None)

        # 初始化便捷消息读取列表
        self.Message = []
        self.Images = []

        # 解析原始消息数据
        self.MessageData = data.get("message", [])
        self.__parse_message_data()

    def __parse_message_data(self):
        """解析消息数据"""
        for item in self.MessageData:
            msg_type = item.get("type")
            msg_data = item.get("data", {})

            if msg_type == "text":
                self.Message.append(msg_data.get("text", ""))
            elif msg_type == "image":
                url = msg_data.get("url", "").replace(
                    "https://multimedia.nt.qq.com.cn/", "https://gchat.qpic.cn/"
                )
                self.Images.append(url)
        # 如果没有文字消息，添加空字符串占位
        if not self.Message:
            self.Message.append("")
