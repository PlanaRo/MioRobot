from datetime import datetime
from Core.Plugin import Plugin
from functools import singledispatchmethod
from Models.Context.GroupMessageContext import GroupMessageContext


class HotReloadPlugin(Plugin):

    @singledispatchmethod
    async def run(self, context: GroupMessageContext):
        print(context.Event.Message)

        if context.Event.Message[0] == "高考倒计时":
            Today = datetime.now()
            year = Today.year
            # 高考开始日期
            gaokaoStartDate = datetime(year, 6, 7)

            # 计算剩余天数，注意需要将datetime对象转换为date对象进行计算
            RemainingDays = (gaokaoStartDate.date() - Today.date()).days

            if RemainingDays > 0:
                reply = f"距离高考还有{RemainingDays}天！"

                await context.Command.Reply(reply)
            elif RemainingDays > -3:
                await context.Command.Reply("阁下，高考加油!")
            else:
                year = Today.year + 1
                gaokaoStartDate = datetime(year, 6, 7)

                RemainingDays = (gaokaoStartDate.date() - Today.date()).days
                reply = f"距离高考还有{RemainingDays}天！"
                await context.Command.Reply(reply)

    def dispose(self) -> None:
        pass
