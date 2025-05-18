import json


class Config:
    """
    初始化配置信息
    """

    def __init__(self):
        with open("Cache\config.json") as jsonFile:
            jsonData = json.load(jsonFile)

        self.__setData(jsonData)
        self.__setManageData(jsonData)

    def __str__(self):
        return str(self.__dict__)

    def __setData(self, jsonData):
        # websocket配置信息
        self.websocket = "{0}/?access_token={1}".format(
            jsonData["websocket"], jsonData["token"]
        )

    def __setManageData(self, jsonData):
        # Uvicorn配置信息
        self.uvicornPort = jsonData["managePort"]
