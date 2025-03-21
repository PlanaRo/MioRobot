import os
from typing import Any, Type
from Models.Event.BaseEvent import BaseEvent
from Models.Event.GroupMessageEvent import GroupMessageEvent
from Models.Context.MessageContext import MessageContext
from Plugin import Plugin, PluginSetting
from Utils.LoadModel import findSubclasses
from Utils.Logs import Log
import traceback
import sys
import time
from GroupControl import GroupControl


class PluginLoader:
    """
    插件加载器
    """

    # 单例模式
    _instance = None
    # 插件实例字典
    pluginInstanceList: dict[Plugin, int] = {}

    # 加载的插件数量
    pluginNumber = 0

    # 性能警告阈值,单位为秒
    performanceWarningThreshold = 1
    # 全部插件初始化加载时间
    pluginLoadTime = 0

    # 单插件调用耗时记录
    pluginCallTime: dict[str, float] = {}

    def __new__(cls, *args: Any, **kwargs: Any):
        if not cls._instance:
            cls._instance = super(PluginLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):  # 防止__init__方法的重复调用
            self._initialized = True

    def getPlugins(self) -> dict[str, dict]:
        """
        获取插件设置数据
        """
        pluginsSettingData = {}

        for plugin in self.pluginInstanceList.keys():
            pluginsSettingData[plugin.name] = plugin.getPluginStatus()
        return pluginsSettingData

    def getPluginsName(self) -> list[str]:
        """
        获取插件名称列表
        @return: 插件名称列表
        """
        pluginsName = []
        for plugin in self.pluginInstanceList.keys():
            pluginsName.append(plugin.name)
        return pluginsName

    def updatePluginSetting(self, pluginName: str, setting: PluginSetting) -> bool:
        """
        更新插件设置
        @param pluginName: 插件名称
        @param setting: 插件设置
        @return: None
        """
        flag: bool = False

        for plugin in self.pluginInstanceList.keys():
            if plugin.name == pluginName:
                plugin.updateSetting(setting)
                flag = True
                break
        PluginLoaderControl.reload()
        return flag

    def loading(self, reload: bool = False) -> None:
        """
        加载插件
        @param reload: 是否重新加载
        @return: None
        """
        # 统计加载插件的时间
        startTime = time.time()
        # 扫描获取所有插件类
        subclasses: list[Type[Plugin]] = findSubclasses("Plugins", Plugin, reload)

        for subclass in subclasses:
            try:
                # 实例化插件
                pluginInstance = subclass()
                # 初始化插件
                pluginInstance.init()
                # 添加插件到字典中
                self.pluginInstanceList[pluginInstance] = (
                    pluginInstance.setting.priority
                )
                self.pluginNumber += 1

            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)
                Log.pluginError(
                    subclass.__name__,
                    f"加载插件 {subclass.__name__} 失败。\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}",
                )

        # 将插件按照优先级排序
        self.pluginInstanceList = dict(
            sorted(
                self.pluginInstanceList.items(), key=lambda item: item[1], reverse=True
            )
        )
        Log.info(f"成功加载了{self.pluginNumber}个插件")
        self.pluginLoadTime = time.time() - startTime
        Log.info(f"加载插件耗时: {self.pluginLoadTime}秒")

    def reload(self) -> None:
        """
        重新加载插件
        """
        # 插件实例字典
        self.pluginInstanceList = {}

        # 加载的插件数量
        self.pluginNumber = 0

        # 全部插件初始化加载时间
        self.pluginLoadTime = 0

        # 单插件调用耗时记录
        self.pluginCallTime = {}

        Log.info("正在重新加载插件")

        # 重新加载插件
        self.loading(reload=True)

        Log.info("重载成功")

    def clearMemory(self) -> None:
        """
        调用插件的dispose方法,清理内存
        """
        Log.info("正在清理内存")
        for plugin in self.pluginInstanceList.keys():
            plugin.dispose()

    async def callBack(
        self,
        messageContext: MessageContext[BaseEvent],
    ) -> None:
        """
        调用插件
        @param messageContext: 消息上下文
        """
        # 获取消息类型
        postType = messageContext.Event.Post_Type
        # 统计插件调用的时间
        startTime = time.time()
        # 遍历插件回调函数对象字典
        for plugin in self.pluginInstanceList.keys():

            try:
                if not plugin.setting.enable:
                    continue

                if isinstance(messageContext.Event, GroupMessageEvent):
                    # 判断群组是否启用
                    if not GroupControl.isEnable(messageContext.Event.Group):
                        continue

                    # 判断群组插件是否启用
                    if not GroupControl.isEnablePlugin(
                        messageContext.Event.Group, plugin.name
                    ):
                        continue

                # 判断是否在插件的监听事件中
                if postType in plugin.setting.event:
                    # 调用插件
                    await plugin.run(messageContext)
                    # 统计插件运行时间
                    runtime = time.time() - startTime
                    # 将插件运行时间添加到字典中
                    self.pluginCallTime[plugin.name] = runtime
                    # 判断插件是否触发,如果触发则取消后续插件的运行
                    if messageContext.Command.Trigger.isTriggered():
                        break

            except Exception as e:
                _exc_type, _exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)

                Log.pluginError(
                    plugin.name,
                    f"调用插件 {plugin.name} 失败。\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}",
                )


# 单例初始化
PluginLoaderControl = PluginLoader()
