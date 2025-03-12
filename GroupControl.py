from Models.Api.RobotInfo import RobotInfo
import websockets
import json
import asyncio
from Utils.Logs import Log
from Utils.WebsocketControl import WebsocketControl


class GroupControl:
    """
    群控制类
    """

    # 群列表,群号为键,群是否开启为值
    groupList: dict = {}
    websocket: websockets.WebSocketClientProtocol

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
        rowGroupData = await RobotInfo.getGroupList()
        if rowGroupData is not None:
            GroupControl.updateGroupData(rowGroupData)  # type: ignore
        else:
            Log.error("获取群数据失败")

    @staticmethod
    def setGroupStatus(groupId: str, status: bool):
        """
        设置群是否启用
        :param groupId: 群号
        :param status: 状态
        """
        try:
            with open("Cache/GroupList.json", "r+", encoding="utf-8") as f:
                groupDataList = json.load(f)
        except:
            groupDataList = []

        for i in range(len(groupDataList)):
            if groupDataList[i]["group_id"] == groupId:
                groupDataList[i]["status"]["enable"] = status
                # 更新groupList的数据
                GroupControl.groupList[groupId]["enable"] = status

        with open("Cache/GroupList.json", "w", encoding="utf-8") as f:
            json.dump(groupDataList, f, ensure_ascii=False, indent=4)

    @staticmethod
    def isEnable(groupId: str) -> bool:
        """
        判断群是否启用
        :param group_id: 群号
        :return: 是否启用
        """
        return GroupControl.groupList.get(groupId, {}).get("enable", False)

    @staticmethod
    def isEnablePlugin(groupId: str, pluginName: str) -> bool:
        """
        判断群是否启用插件
        :param group_id: 群号
        :param plugin_name: 插件名
        :return: 是否启用
        """
        return (
            GroupControl.groupList.get(groupId, {})
            .get("plugins", {})
            .get(pluginName, False)
        )

    @staticmethod
    def updateGroupData(rowGroupData: dict, pluginList: list[str]):
        """
        更新文件中的群数据,将文件中的群数据与api获取到的数据合并
        :param row_group_data: 群数据
        :param plugin_list: 插件列表
        """
        try:
            with open("Cache/GroupList.json", "r+", encoding="utf-8") as f:
                groupDataList = json.load(f)
        except:
            groupDataList = []

        groupList = rowGroupData["data"]
        # 默认不启用
        isEnable = False
        # 通过推导式将api格式化获取到的数据
        newGroupList = [
            {
                "group_id": group["group_id"],
                "group_name": group["group_name"],
                "status": {
                    "enable": isEnable,
                    "plugins": {pluginName: False for pluginName in pluginList},
                },
            }
            for group in groupList
        ]

        # 将api获取的数据和文件读取的数据合并，更新群列表中的status字段
        for i in range(len(newGroupList)):
            for item in groupDataList:
                if newGroupList[i]["group_id"] == item["group_id"]:

                    GroupControl.groupList[str(newGroupList[i]["group_id"])] = {
                        "enable": item["status"]["enable"],
                        "plugins": item["status"]["plugins"],
                    }

                    newGroupList[i]["status"] = item["status"]

        # 更新文件中的群数据
        with open("Cache/GroupList.json", "w", encoding="utf-8") as f:
            json.dump(newGroupList, f, ensure_ascii=False, indent=4)

    @staticmethod
    def updateGroupStatus(groupId: str, status: bool, pluginName: str):
        """
        更新群状态
        :param group_id: 群号
        :param status: 状态
        :param plugin_name: 插件名
        """
        # 获取群数据
        try:
            with open("Cache/GroupList.json", "r+", encoding="utf-8") as f:
                groupDataList = json.load(f)
        except:
            groupDataList = []

        for i in range(len(groupDataList)):
            if groupDataList[i]["group_id"] == groupId:
                groupDataList[i]["status"]["enable"] = status
                groupDataList[i]["status"]["plugins"][pluginName] = status
                # 更新groupList的数据
                GroupControl.groupList[groupId] = {
                    "enable": status,
                    "plugins": groupDataList[i]["status"]["plugins"],
                }
                break
        # 更新文件中的群数据
        with open("Cache/GroupList.json", "w", encoding="utf-8") as f:
            json.dump(groupDataList, f, ensure_ascii=False, indent=4)
