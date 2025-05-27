import base64
from functools import singledispatchmethod
import aiohttp
from Models.Context.GroupMessageContext import GroupMessageContext
from Core.Plugin import Plugin
from Models.MessageChain.Message import Image
from Models.MessageChain.MessageChain import MessageChain
from Plugins.super_img.super import do_super_resolution


class SuperImagePlugin(Plugin):
    # 需要超分的qq用户缓存
    cache: dict

    def init(self):
        self.cache = {}

    @singledispatchmethod
    async def run(self, context: GroupMessageContext):

        QQ = str(context.Event.QQ)

        if context.Event.Message[0] == "图片超分":
            await context.Command.Reply("发送超分图片，然后再发送图片就可以超分图片啦")

        if context.Event.Message[0] == "超分图片":

            if context.Event.Images:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=context.Event.Images[0]) as resp:
                        imgData = await resp.read()

                if imgData:
                    imgData = await do_super_resolution(imgData)
                    if isinstance(imgData, str):
                        await context.Command.Reply("超分失败，图片太大")
                    else:

                        imgData = base64.b64encode(imgData.getvalue()).decode()

                        messageChain = MessageChain().add(Image(f"base64://{imgData}"))

                        await context.Command.Reply(messageChain)
                else:
                    await context.Command.Reply("图片url存在问题，请稍后重试")
            else:
                self.cache[QQ] = True
                await context.Command.Reply("阁下请携带图片")

        if self.cache.get(QQ, False):
            self.cache.pop(QQ)
            if context.Event.Images:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=context.Event.Images[0]) as resp:
                        imgData = await resp.read()

                if imgData:
                    imgData = await do_super_resolution(imgData)
                    if isinstance(imgData, str):
                        await context.Command.Reply("超分失败，图片太大")
                    else:
                        imgData = base64.b64encode(imgData.getvalue()).decode()

                        messageChain = MessageChain().add(Image(f"base64://{imgData}"))

                        await context.Command.Reply(messageChain)
                else:
                    await context.Command.Reply("图片url存在问题，请稍后重试")

    def dispose(self) -> None:
        self.cache.clear()
