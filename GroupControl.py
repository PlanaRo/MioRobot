from Models.Api.RobotInfo import RobotInfo
import websockets
import json
import asyncio
from Utils.WebsocketControl import WebsocketControl


class GroupControl:
    """
    群控制类
    """

    # 群列表,群号为键,群是否开启为值
    groupList = {}
    websocket: websockets.WebSocketClientProtocol = None

    @staticmethod
    def init():
        """
        初始化群控制类,即通过接口获取群数据,并更新群列表
        :param websocket: websocket连接
        """
        GroupControl.websocket = WebsocketControl.websocket

        loop = asyncio.get_event_loop()
        loop.create_task(GroupControl.getGroupData())

    @staticmethod
    async def getGroupData():
        """
        获取群数据
        :return: 群数据
        """
        # 通过接口获取群数据
        rowGroupData = await RobotInfo.getGroupLList()
        GroupControl.updateGroupData(rowGroupData)

    @staticmethod
    def isEnable(groupId: str) -> bool:
        """
        判断群是否启用
        :param group_id: 群号
        :return: 是否启用
        """
        return GroupControl.group_list.get(groupId, False)

    @staticmethod
    def updateGroupData(rowGroupData: dict):
        """
        更新文件中的群数据
        :param row_group_data: 群数据
        """
        try:
            with open("Cache/GroupList.json", "r+", encoding="utf-8") as f:
                groupDataList = json.load(f)
        except:
            groupDataList = []

        groupList = rowGroupData["data"]
        # 默认不启用
        is_enable = False
        # 通过推导式将api格式化获取到的数据
        groupList = [
            {
                "group_id": group["group_id"],
                "group_name": group["group_name"],
                "is_enable": is_enable,
            }
            for group in groupList
        ]

        # 将api获取的数据和文件读取的数据合并，更新群列表中的is_enable字段
        for i in range(len(groupList)):
            for item in groupDataList:
                if groupList[i]["group_id"] == item["group_id"]:

                    GroupControl.groupList[str(groupList[i]["group_id"])] = item[
                        "is_enable"
                    ]

                    groupList[i]["is_enable"] = item["is_enable"]

        # 更新文件中的群数据
        with open("Cache/GroupList.json", "w", encoding="utf-8") as f:
            json.dump(groupList, f, ensure_ascii=False, indent=4)
