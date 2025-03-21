from enum import Enum


class EventType(Enum):
    """
    事件类型
    """

    # 群聊消息
    GroupMessage = "GroupMessage"
    # 好友消息
    FriendMessage = "FriendMessage"
