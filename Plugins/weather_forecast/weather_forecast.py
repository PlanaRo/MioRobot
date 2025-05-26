import base64
import re
from Models.Context.GroupMessageContext import GroupMessageContext
from Core.Plugin import Plugin
from Models.MessageChain.Message import Image
from Models.MessageChain.MessageChain import MessageChain
from Plugins.weather_forecast.weather import Weather
from functools import singledispatchmethod


class WeatherForecast(Plugin):

    @singledispatchmethod
    async def run(self, context: GroupMessageContext):

        data = re.search(r"^天气 (.*)", context.Event.Message[0])
        if data:
            weather = Weather(data.group(1))
            if weather.isTrueCity:
                # 获取天气信息
                image = weather.image()
                if image is None:
                    await context.Command.Reply("天气信息获取失败，请稍后再试！")
                else:
                    img_data = base64.b64encode(image).decode()
                    messageChain = MessageChain().add(Image(f"base64://{img_data}"))
                    await context.Command.Reply(messageChain)
            else:
                await context.Command.Reply(
                    "阁下输入的城市不存在，请换一个城市再试试！",
                )

    def dispose(self) -> None:
        pass
