import json
import os


class Config:
    """
    初始化配置信息
    """

    def __init__(self):

        configPath = "Cache/config.json"

        if not os.path.exists(configPath):
            defaultConfig = {
                "websocket": "ws://localhost:5800",
                "token": "",
                "managePort": "580",
            }
            with open(configPath, "w") as jsonFile:
                json.dump(defaultConfig, jsonFile)

        with open(configPath) as jsonFile:
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
