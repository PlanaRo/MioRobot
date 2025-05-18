from abc import ABC, abstractmethod
import inspect
import json
import os
from dataclasses import dataclass
from Models.Event.BaseEvent import BaseEvent
from Models.Event.EventType import EventType
from Models.Context.MessageContext import MessageContext
from Utils.Logs import Log
from functools import singledispatchmethod
from typing import TypeVar, Generic


T = TypeVar("T", bound=BaseEvent)


@dataclass
class PluginSetting:
    # 插件优先级
    _priority: int
    # 是否启用
    _enable: bool
    # 监听事件列表
    _event: list[EventType]
    # 是否在菜单隐藏,为True时将不会在简易菜单中显示
    _hide: bool

    def __init__(
        self,
        priority: int,
        enable: bool,
        event: list[EventType],
        hide: bool,
    ) -> None:
        self._priority = priority
        self._enable = enable
        self._event = event
        self._hide = hide

    @property
    def priority(self) -> int:
        return self._priority

    @priority.setter
    def priority(self, priority: int) -> None:
        self._priority = priority

    @property
    def enable(self) -> bool:
        return self._enable

    @enable.setter
    def enable(self, enable: bool) -> None:
        self._enable = enable

    @property
    def event(self) -> list[EventType]:
        return self._event

    @event.setter
    def event(self, event: list[EventType]) -> None:
        self._event = event

    @property
    def hide(self) -> bool:
        return self._hide

    @hide.setter
    def hide(self, hide: bool) -> None:
        self._hide = hide

    @classmethod
    def loadFromJson(cls, jsonData: dict) -> "PluginSetting":
        """
        从JSON数据中加载插件设置
        """
        if "event" in jsonData.keys():
            jsonData["event"] = cls.loadEvent(jsonData["event"])
        return cls(**jsonData)

    @staticmethod
    def loadEvent(eventList: list[str]):
        return [EventType(event) for event in eventList]

    def toJson(self) -> dict:
        return {
            "priority": self.priority,
            "enable": self.enable,
            "event": [event.value for event in self.event],
            "hide": self.hide,
        }


@dataclass
class DeveloperSetting:
    # 是否启用debug模式
    _debug: bool = False
    # 是否记录插件运行时间
    _countRuntime: bool = False
    # 运行时间阈值，超过则输出警告
    _runtimeThreshold: float = 0.5

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, debug: bool) -> None:
        self._debug = debug

    @property
    def countRuntime(self) -> bool:
        return self._countRuntime

    @countRuntime.setter
    def countRuntime(self, countRuntime: bool) -> None:
        self._countRuntime = countRuntime

    @property
    def runtimeThreshold(self) -> float:
        return self._runtimeThreshold

    @runtimeThreshold.setter
    def runtimeThreshold(self, runtimeThreshold: float) -> None:
        self._runtimeThreshold = runtimeThreshold

    @classmethod
    def loadFromJson(cls, jsonData: dict) -> "DeveloperSetting":
        """
        从JSON数据中加载插件设置
        """
        return cls(**jsonData)

    def toJson(self) -> dict:
        return {
            "debug": self.debug,
            "countRuntime": self.countRuntime,
            "runtimeThreshold": self.runtimeThreshold,
        }


class Plugin(ABC):

    # 插件作者
    _author: str
    # 插件名称
    _name: str
    # 简易菜单展示名称
    _displayName: str
    # 插件描述
    _description: str
    # 插件版本
    _version: str
    # 插件设置
    _setting: PluginSetting
    # 开发者设置
    _developerSetting: DeveloperSetting

    def __init__(self):
        """
        初始化插件
        如果子类需要重写构造函数，请使用super().__init__()
        """
        self.loadConfig()
        self.init()

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, author: str) -> None:
        self._author = author

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def displayName(self) -> str:
        return self._displayName

    @displayName.setter
    def displayName(self, displayName: str) -> None:
        self._displayName = displayName

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, version: str) -> None:
        self._version = version

    @property
    def setting(self) -> PluginSetting:
        return self._setting

    @setting.setter
    def setting(self, setting: PluginSetting) -> None:
        self._setting = setting

    @property
    def developerSetting(self) -> DeveloperSetting:
        return self._developerSetting

    @developerSetting.setter
    def developerSetting(self, developerSetting: DeveloperSetting) -> None:
        self._developerSetting = developerSetting

    def init(self) -> None:
        """
        此方法用于插件初始化私有数据
        """
        pass

    @singledispatchmethod
    @abstractmethod
    async def run(
        self,
        context: MessageContext,
    ):
        """
        此方法用于插件运行
        请使用@singledispatchmethod进行任务分发
        """
        pass

    @abstractmethod
    def dispose(self) -> None:
        """
        此方法用于释放内存等资源
        对于需要临时存储数据的插件，请重写此方法，用于释放内存等资源
        """
        pass

    def loadConfig(self) -> bool:
        """
        获取配置文件中对应键的值
        """
        currentClass = self.__class__
        filePath = inspect.getfile(currentClass)
        jsonFilePath = os.path.join(os.path.dirname(filePath), "Cache\config.json")

        try:
            # 读取配置文件
            with open(jsonFilePath, "r", encoding="utf-8") as configFile:
                configData = json.load(configFile)
                self.author = configData.get("author", "未提供作者信息")
                self.name = configData.get("name", "未提供名称")
                self.displayName = configData.get("display_name", "未提供显示名称")
                self.description = configData.get("description", "未提供描述")
                self.version = configData.get("version", "未提供版本号")
                self.setting = PluginSetting.loadFromJson(configData.get("setting", {}))
                self.developerSetting = DeveloperSetting.loadFromJson(
                    configData.get("developer_setting", {})
                )
            return True  # 成功返回True
        except Exception as e:
            Log.error(f"错误信息{e}")
            return False  # 失败返回False

    def getPluginStatus(self):
        """
        获取插件基础信息和设置
        """
        return {
            "author": self.author,
            "name": self.name,
            "displayName": self.displayName,
            "description": self.description,
            "version": self.version,
            "setting": self.setting.toJson(),
            "developerSetting": self.developerSetting.toJson(),
        }

    def setStatus(self, status: bool):
        """
        设置插件开关状态
        """
        # 获取配置文件路径
        currentClass = self.__class__
        filePath = inspect.getfile(currentClass)
        jsonFilePath = os.path.join(os.path.dirname(filePath), "Cache\config.json")

        try:
            with open(jsonFilePath, "r+", encoding="utf-8") as configFile:
                configData = json.load(configFile)

                configData["setting"]["enable"] = status
                # 指针回到文件开头
                configFile.seek(0)
                # 清空文件
                configFile.truncate()

                configFile.write(configData)
            return True
        except Exception as e:
            Log.error(f"错误信息{e}")
            return False

    def updateSetting(self, setting: PluginSetting):
        """
        更新插件设置
        """
        # 获取配置文件路径
        currentClass = self.__class__
        filePath = inspect.getfile(currentClass)
        jsonFilePath = os.path.join(os.path.dirname(filePath), "Cache\config.json")

        try:
            with open(jsonFilePath, "r+", encoding="utf-8") as configFile:
                configData = json.load(configFile)
                configData["setting"] = setting.toJson()
                configFile.seek(0)
                configFile.truncate()
                configFile.write(configData)
        except Exception as e:
            Log.error(f"错误信息{e}")
            return False
