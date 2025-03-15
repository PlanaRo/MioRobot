from Plugin import Plugin
from PluginLoader import PluginLoaderControl
from functools import singledispatchmethod
from Models.Context.GroupMessageContext import GroupMessageContext


class HotReloadPlugin(Plugin):
    def init(self):
        pass

    @singledispatchmethod
    async def run(self, context: GroupMessageContext):

        if context.Event.Message[0] == "插件重载":
            PluginLoaderControl.reload()
            await context.Command.Reply("重载成功")

    def dispose(self) -> None:
        pass
