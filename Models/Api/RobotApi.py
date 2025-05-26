from Models.Api.BaseApi import ApiAdapter, RequestApi


class RobotApi:

    @staticmethod
    async def sendLike(user_id: int, times: int):
        """
        点赞
        Parameters:
            user_id(int): 好友QQ号
            times(int): 点赞次数
        """
        param = {"user_id": user_id, "times": times}
        args = RequestApi("send_like", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getFriendList():
        """
        获取好友列表
        """
        param = {"no_cache": False}
        args = RequestApi("get_friend_list", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getFriendListWithCategory():
        """
        获取好友列表(带分类)
        """
        param = {"no_cache": False}
        args = RequestApi("get_friends_with_category", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def deleteFriend(user_id: int):
        """
        删除好友
        Parameters:
            user_id(int): 好友QQ号
        """
        param = {"user_id": user_id}
        args = RequestApi("delete_friend", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setFriendAddRequest(
        flag: str, approve: bool, remark: str
    ):  # -> str | dict[Any, Any] | None:
        """
        处理好友请求
        Parameters:
            flag(str): 请求id
            approve(bool): 是否同意请求
            remark(str): 添加后的好友备注
        """
        param = {"flag": flag, "approve": approve, "remark": remark}
        args = RequestApi("set_friend_add_request", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setFriendRemark(user_id: int, remark: str):
        """
        设置好友备注
        Parameters:
            user_id (int):好友QQ号
            remark (str): 备注
        """
        param = {"user_id": user_id, "remark": remark}
        args = RequestApi("set_friend_remark", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getStrangerInfo(user_id: int):
        """
        获取好友或群消息
        Parameters:
            user_id (int):好友QQ号
        """
        param = {"user_id": user_id}
        args = RequestApi("get_stranger_info", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setQQAvatar(file: str):
        """
        设置QQ头像

        Parameters:
            file(str): 图片文件

        支持三种格式
        1. 图片文件路径
        2. 图片网址链接
        3. 图片文件base64编码
        {
            // 支持三种形式:
            // file://d:/1.png
            // http://baidu.com/xxxx/1.png
            // base64://xxxxxxxx
            "file": "file://d:\\1.png"
        }
        """
        param = {"file": file}
        args = RequestApi("set_qq_avatar", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def friendPoke(user_id: int):
        """
        发送好友戳一戳

        Parameters:
            user_id (int): 好友QQ号
        """
        param = {"user_id": user_id}
        args = RequestApi("friend_poke", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def uploadPrivateFile(user_id: int, file: str, name: str | None = None):
        """
        Parameters:
            name (str): 用户的名字。
            age (int): 用户的年龄。

        Returns:
            str: 生成的问候语句。
        """
        if name is None:
            param = {"user_id": user_id, "file": file}
        else:
            param = {"user_id": user_id, "file": file, "name": name}
        args = RequestApi("upload_private_file", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getProfileLike(start: int = -1, count: int = 20):
        """
        获取我赞过谁列表

        Parameters:
            start (int): 开始位置,从0开始，-1表示获取全部，获取全部的时候非好友nick可能为空
            count (int): 一页的数量，最多30
        """
        args = RequestApi("get_profile_like", {"start": start, "count": count})
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getWhoLikedMe(start: int = -1, count: int = 20):
        """
        获取谁赞过我列表
        Parameters:
            start (int): 开始位置,从0开始，-1表示获取全部，获取全部的时候非好友nick可能为空
            count (int): 一页的数量，最多30
        """
        args = RequestApi("get_who_liked_me", {"start": start, "count": count})
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getRobotUinRange():
        """
        获取官方机器人QQ号范围
        """
        args = RequestApi("get_robot_uin_range", {})
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setFriendCategory(user_id: int, category: str):
        """
        移动好友到指定分组

        Parameters:
            user_id (int): 好友QQ号
            category (str): 分组名称
        """
        param = {"user_id": user_id, "category": category}
        args = RequestApi("set_friend_category", param)
        return await ApiAdapter.sendActionApi(args, 10)
