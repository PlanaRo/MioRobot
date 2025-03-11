import os
from importlib import import_module, reload
from typing import Any
import Plugin as BasePlugin
from Utils.Logs import Log
from DataType.MessageData import MessageData
import traceback
import sys
import time
import websockets


class PluginLoader:
    """
    插件加载器
    """

    # 单例模式
    _instance = None
    # 插件路径
    _pluginPathList = None
    # 插件实例字典
    pluginInstanceList = {}

    # 加载的插件数量
    pluginNumber = 0

    # 性能警告阈值,单位为秒
    performanceWarningThreshold = 1
    # 全部插件初始化加载时间
    pluginLoadTime = 0

    # 单插件调用耗时记录
    pluginCallTime = {}

    def __new__(cls, *args: Any, **kwargs: Any):
        if not cls._instance:
            cls._instance = super(PluginLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):  # 防止__init__方法的重复调用
            self._pluginPathList = os.listdir("Plugin")
            self._initialized = True

    def loading(self) -> None:
        """
        加载插件
        """
        # 统计加载插件的时间
        startTime = time.time()

        # for pluginName in self._pluginPathList:
        #     try:
        #         # 导入模块
        #         pluginModel: Plugin = reload(import_module(f"Plugin.{pluginName}"))
        #         # 获取优先级
        #         priority = pluginModel.Plugin.setting["priority"]

        #         # 将插件实例添加到字典中
        #         self.plugin_list[plugin_model] = priority

        #         # 记录回调函数名
        #         self.plugin_name_list.append(callback_name)

        #         # 记录加载的插件数量
        #         self.plugin_num += 1

        #     except Exception as e:
        #         exc_type, exc_value, exc_traceback = sys.exc_info()
        #         tb = traceback.extract_tb(exc_traceback)

        #         Log.plugin_error(
        #             plugin_name,
        #             f"加载插件 {plugin_name} 失败。\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}",
        #         )

        # # 将插件按照优先级排序
        # self.plugin_list = dict(
        #     sorted(self.plugin_list.items(), key=lambda item: item[1], reverse=True)
        # )
        # Log.info(f"成功加载了{self.plugin_num}个插件")

        # self.plugin_load_time = time.time() - start_time
        # Log.info(f"加载插件耗时: {self.plugin_load_time}秒")
        subclasses = BasePlugin.Plugin.subclasses
        for subclass in subclasses:
            try:
                pluginInstance = subclass()
                pluginInstance.init()
                self.pluginInstanceList[pluginInstance] = (
                    pluginInstance.setting.priority
                )

            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)
                Log.plugin_error(
                    subclass.__name__,
                    f"加载插件 {subclass.__name__} 失败。\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}",
                )

    def reload(self) -> None:
        """
        重新加载插件
        """
        # 删除旧插件
        # 插件路径
        self._plugin_path_list = os.listdir("Plugin")

        # 插件回调函数对象字典
        self.plugin_list = {}
        # 插件回调函数名列表,用于检查重复
        self.plugin_name_list = []
        # 全部插件调用耗时记录
        self.plugin_call_time = {}
        # 加载的插件数量
        self.plugin_num = 0

        Log.info("正在重新加载插件")

        # 重新加载插件
        self.loading()

        Log.info("重载成功")

    async def callBack(
        self,
        messageData: MessageData,
    ) -> None:
        """
        调用插件
        """

        Post_Type = messageData.Post_Type

        # 统计插件调用的时间
        start_time = time.time()
        # 遍历插件回调函数对象字典
        for plugin_model in self.plugin_list.keys():

            try:
                # 获取插件名
                plugin_name: str = plugin_model.plugin.name
                # 获取回调函数名
                callback_name = plugin_model.plugin.setting["callback_name"]
                # 获取开发者设置
                developer_setting = plugin_model.plugin.developer_setting
                # 判断是否在插件的监听事件中
                if Post_Type in plugin_model.plugin.setting["event"]:

                    # 记录插件运行时间
                    if plugin_model.plugin.developer_setting["count_runtime"]:
                        start_time = time.time()

                    # 调用插件
                    callback = eval(f"plugin_model.{callback_name}")
                    code = await callback(
                        websocket, data, self.trigger_list[callback_name]
                    )

                    # 记录插件运行时间
                    if developer_setting["count_runtime"]:
                        # 统计插件运行时间
                        runtime = time.time() - start_time
                        # 将插件运行时间添加到字典中
                        self.plugin_call_time[plugin_name] = runtime
                        if (
                            runtime > developer_setting["runtime_threshold"]
                            and not developer_setting["allow_high_time_cost"]
                        ):
                            Log.warning(
                                f"插件({plugin_name})运行耗时: {runtime}秒,性能较低，请检查插件!"
                            )

                    # 判断检查，是否有插件返回了非0的状态码
                    # 0为触发，1为未触发，-1为插件错误
                    if code == 0:
                        # 触发并中断后续插件的调用
                        Log.info(f"插件({plugin_name})触发成功")
                        break
                    elif code == -1:
                        # 插件错误
                        Log.plugin_error(
                            plugin_name,
                            f"插件({plugin_name})触发失败,插件内部错误",
                        )
                        break

            except Exception as e:
                _exc_type, _exc_value, exc_traceback = sys.exc_info()
                tb = traceback.extract_tb(exc_traceback)

                Log.plugin_error(
                    plugin_name,
                    f"调用插件 {plugin_name} 失败。\n文件路径: {tb[-1].filename} \n行号：{tb[-1].lineno} \n错误源码:{traceback.format_exc()}\n错误信息为: {e}",
                )

        # 统计插件调用的时间
        self.plugin_call_time = time.time() - start_time
        if self.plugin_call_time > self.performance_warning_threshold:
            Log.warning(
                f"插件调用耗时: {self.plugin_call_time}秒,性能较低，请检查插件!"
            )


# 单例初始化
PluginLoaderControl = PluginLoader()
