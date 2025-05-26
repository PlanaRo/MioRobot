from Models.Api.BaseApi import RequestApi, ApiAdapter


class SystemApi:
    """LLOneBot 系统相关API接口类"""

    @staticmethod
    async def get_login_info():
        """
        获取登录号信息
        """
        param = {}
        args = RequestApi("get_login_info", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def get_version_info():
        """
        获取版本信息
        """
        param = {}
        args = RequestApi("get_version_info", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def get_status():
        """
        获取bot状态
        """
        param = {}
        args = RequestApi("get_status", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def clean_cache():
        """
        清理缓存
        """
        param = {}
        args = RequestApi("clean_cache", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def download_file(
        url: str, name: str, base64: str | None = None, headers: list = []
    ):
        """
        下载文件到bot所在服务器

        Parameters:
            url (str): 文件下载链接
            name (str, optional): 文件保存名称，为空则自动获取
            headers (str, optional): 请求头，格式为JSON字符串
            base64 (str, optional): 文件base64编码，为空则使用url下载
        """
        param = {"url": url, "name": name, "headers": headers, "base64": base64}
        args = RequestApi("download_file", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def get_cookies(domain: str = ""):
        """
        获取cookies

        Parameters:
            domain (str, optional): 指定域名，为空则获取所有cookies
        """
        param = {"domain": domain}
        args = RequestApi("get_cookies", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def set_online_status(
        status: int, ext_status: int = 0, battery_status: int = 100
    ):
        """
        设置在线状态

        Parameters:
            status (int): 在线状态 (10:在线 30:离开 40:隐身 50:忙碌 60:Q我吧 70:请勿打扰)
            ext_status (int, optional): 扩展状态，默认为0
            battery_status (int) : 电量状态，默认认为100
        """
        param = {
            "status": status,
            "ext_status": ext_status,
            "battery_status": battery_status,
        }
        args = RequestApi("set_online_status", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def ocr_image(image: str):
        """
        图片OCR识别

        Parameters:
            image (str): 图片路径或Base64编码或url
        """
        param = {"image": image}
        args = RequestApi("ocr_image", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def fetchCustomFace():
        """
        获取收藏表情列表
        """
        param = {}
        args = RequestApi("fetch_custom_face", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def restart():
        """
        重启机器人
        """
        param = {}
        args = RequestApi("restart", param)
        return await ApiAdapter.sendActionApi(args, 10)
