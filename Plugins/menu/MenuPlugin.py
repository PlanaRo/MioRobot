from Plugin import Plugin
from Plugins.menu.Menu import Menu
from DataType.CQcode import CQcode
import re
from Models.Context.GroupMessageContext import GroupMessageContext
from functools import singledispatchmethod


class Plugin(Plugin):
    def init(self):
        pass

    @singledispatchmethod
    async def run(self, context: GroupMessageContext):

        if context.Event.Message[0] == "菜单":
            menu_data = Menu(display_number=10)
            await context.Command.Reply(menu_data.show_menu())

            if menu_data.page_number > 1:
                await context.Command.Reply(
                    CQcode.at(context.Event.QQ)
                    + ' 这是第1页菜单,总共{}页,发送"第2页"可以查看其他菜单哦'.format(
                        menu_data.page_number
                    ),
                )

        elif num := re.match(r"第(\d+)页", context.Event.Message[0]):
            menu_data = Menu(display_number=10)
            data = menu_data.show_menu(page_num=int(num.group(1)))
            await context.Command.Reply(
                data if data else CQcode.at(context.Event.QQ) + " 没有更多了",
            )

    def dispose(self) -> None:
        pass
