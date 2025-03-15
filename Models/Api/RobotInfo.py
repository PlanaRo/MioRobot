from Models.Api.BaseApi import RequestApi, ApiAdapter


class RobotInfo:

    @staticmethod
    async def getRobotInfo():
        """
        获取机器人信息
        """
        raise NotImplementedError

    @staticmethod
    async def getGroupList() -> str | dict | None:
        param = {"no_cache": False}
        args = RequestApi("get_group_list", param)
        return await ApiAdapter.sendActionApi(args, 10)
