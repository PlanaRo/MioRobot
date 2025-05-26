from abc import ABC

from Models.Event.EventType import EventType


class BaseEvent(ABC):
    """
    消息数据基类
    """

    # 机器人QQ号
    Robot: int
    # 事件类型
    Post_Type: EventType
    # 消息事件戳
    Time: int
