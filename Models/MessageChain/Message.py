from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# 添加类型检查时的导入（不会影响运行时）,防止循环导入
if TYPE_CHECKING:
    from Models.MessageChain.MessageChain import MessageChain


class Message(ABC):
    """
    消息基类
    """

    type: str

    def __str__(self):
        return str(self.to_dict())

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class Text(Message):
    """
    文本消息
    """

    type: str = "text"
    content: str

    def __init__(self, content: str):
        self.content = content

    def to_dict(self) -> dict:
        return {"type": self.type, "data": {"text": self.content}}


class Image(Message):
    """
    图片消息

    Parameters:
        file: 图片文件/base64编码的图片文件/网址
    """

    type: str = "image"
    file: str

    def __init__(self, file: str):
        self.file = file

    def to_dict(self) -> dict:
        return {"type": self.type, "data": {"file": self.file}}


class Video(Message):
    """
    视频消息

    Parameters:
        file: 视频文件/base64编码的视频文件
    """

    type: str = "video"
    file: str

    def __init__(self, file: str):
        self.file = file

    def to_dict(self) -> dict:
        return {"type": self.type, "data": {"url": self.file}}


class Reply(Message):
    """
    回复消息

    Parameters:
        message_id: 消息ID
    """

    type: str = "reply"
    message_id: int

    def __init__(self, message_id: int):
        self.message_id = message_id

    def to_dict(self) -> dict:
        return {"type": self.type, "data": {"id": self.message_id}}


class At(Message):
    """
    At消息
    """

    type: str = "at"
    qq: int

    def __init__(self, qq: int):
        self.qq = qq

    def to_dict(self) -> dict:
        return {"type": self.type, "data": {"qq": self.qq}}


class Face(Message):
    """
    表情消息
    """

    type: str = "face"
    face_id: int

    def __init__(self, face_id: int):
        self.face_id = face_id

    def to_dict(self) -> dict:
        return {"type": self.type, "data": {"id": self.face_id}}


class Record(Message):
    """
    语音消息

    Parameters:
        file: 语音文件/base64编码的语音文件
    """

    type: str = "record"
    file: str

    def __init__(self, file: str):
        self.file = file

    def to_dict(self) -> dict:
        return {"type": self.type, "data": {"file": self.file}}


class Dice(Message):
    """
    骰子消息
    Parameters:
        value(int): 骰子值1-6
    """

    type: str = "dice"
    value: int

    def __init__(self, value: int):
        self.value = value
        if self.value < 1 or self.value > 6:
            raise ValueError("骰子消息的值必须在1-6之间")

    def to_dict(self) -> dict:
        return {"type": self.type, "data": {"value": self.value}}


class Rps(Message):
    """
    猜拳消息
    """

    type: str = "rps"

    def __init__(self):
        pass

    def to_dict(self) -> dict:
        return {"type": self.type, "data": {}}


class QQMusic(Message):
    """
    QQ音乐消息
    Parameters:
        id: 歌曲id
    """

    type: str = "music"
    data: dict

    def __init__(self, music_id: int):
        self.data = {
            "id": music_id,
            "type": "qq",
        }

    def to_dict(self) -> dict:
        return {"type": self.type, "data": self.data}


class WYMusic(Message):
    """
    网易云音乐消息
    Parameters:
        id: 歌曲id
    """

    type: str = "music"
    data: dict

    def __init__(self, music_id: int):
        self.data = {
            "id": music_id,
            "type": "163",
        }

    def to_dict(self) -> dict:
        return {"type": self.type, "data": self.data}


class CustomMusic(Message):
    """
    自定义音乐分享消息

    Parameters:
        url: 音乐跳转链接
        title: 音乐标题
        audio: 音乐音频
        image: 音乐图片
    """

    type: str = "music"
    data: dict

    def __init__(
        self,
        url: str,
        title: str,
        audio: str,
        image: str,
    ):
        self.data = {
            "type": "custom",
            "url": url,
            "title": title,
            "audio": audio,
            "image": image,
        }

    def to_dict(self) -> dict:
        return {"type": self.type, "data": self.data}


class JsonMessage(Message):
    """
    Json消息
    """

    data: dict

    def __init__(self, data: dict):
        self.data = data

    def to_dict(self) -> dict:
        return {"type": "json", "data": self.data}


class ForwardMessage(Message):
    """
    转发消息
    """

    content: "MessageChain"

    def __init__(self, content: "MessageChain"):
        self.content = content

    def to_dict(self) -> dict:
        return {"type": "forward", "data": self.content.to_dict()}
