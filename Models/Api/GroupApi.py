from Models.Api.BaseApi import ApiAdapter, RequestApi


class GroupApi:
    """LLOneBot 群组相关API"""

    @staticmethod
    async def getGroupList():
        """
        获取群列表
        """
        param = {"no_cache": False}
        args = RequestApi("get_group_list", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getGroupInfo(group_id: int):
        """
        获取群详情
        Parameters:
            group_id (int): 群号
        """
        param = {"group_id": group_id}
        args = RequestApi("get_group_info", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getGroupMemberList(group_id: int):
        """
        获取群成员列表
        Parameters:
            group_id (int): 群号
        """
        param = {"group_id": group_id, "no_cache": False}
        args = RequestApi("get_group_member_list", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getGroupMemberInfo(group_id: int, user_id: int):
        """
        获取群成员信息
        Parameters:
            group_id (int): 群号
            user_id (int): 用户QQ号
        """
        param = {"group_id": group_id, "user_id": user_id}
        args = RequestApi("get_group_member_info", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def groupPoke(group_id: int, user_id: int):
        """
        群员戳一戳（双击头像）
        Parameters:
            group_id (int): 群号
            user_id (int): 用户QQ号
        """
        param = {"group_id": group_id, "user_id": user_id}
        args = RequestApi("group_poke", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setGroupAddRequest(flag: str, approve: bool, reason: str = ""):
        """
        处理加群请求
        Parameters:
            flag (str): 请求标识
            approve (bool): 是否同意
            reason (str): 拒绝理由（可选）
        """
        param = {"flag": flag, "approve": approve, "reason": reason}
        args = RequestApi("set_group_add_request", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setGroupLeave(group_id: int):
        """
        退群
        Parameters:
            group_id (int): 群号
        """
        param = {"group_id": group_id}
        args = RequestApi("set_group_leave", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setGroupAdmin(group_id: int, user_id: int, enable: bool):
        """
        设置群管理员
        Parameters:
            group_id (int): 群号
            user_id (int): 用户QQ号
            enable (bool): 是否设置为管理员
        """
        param = {"group_id": group_id, "user_id": user_id, "enable": enable}
        args = RequestApi("set_group_admin", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setGroupCard(group_id: int, user_id: int, card: str):
        """
        设置群名片
        Parameters:
            group_id (int): 群号
            user_id (int): 用户QQ号
            card (str): 群名片,为空则删除群名片
        """
        param = {"group_id": group_id, "user_id": user_id, "card": card}
        args = RequestApi("set_group_card", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setGroupBan(group_id: int, user_id: int, duration: int):
        """
        群禁言
        Parameters:
            group_id (int): 群号
            user_id (int): 用户QQ号
            duration (int): 禁言时长（秒）
        """
        param = {"group_id": group_id, "user_id": user_id, "duration": duration}
        args = RequestApi("set_group_ban", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setGroupWholeBan(group_id: int, enable: bool):
        """
        群全体禁言
        Parameters:
            group_id (int): 群号
            enable (bool): 是否开启全体禁言
        """
        param = {"group_id": group_id, "enable": enable}
        args = RequestApi("set_group_whole_ban", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setGroupName(group_id: int, group_name: str):
        """
        设置群名
        Parameters:
            group_id (int): 群号
            group_name (str): 新群名
        """
        param = {"group_id": group_id, "group_name": group_name}
        args = RequestApi("set_group_name", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setGroupKick(
        group_id: int, user_id: int, reject_add_request: bool = False
    ):
        """
        群踢人
        Parameters:
            group_id (int): 群号
            user_id (int): 用户QQ号
            reject_add_request (bool): 是否拒绝此人的加群请求
        """
        param = {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add_request,
        }
        args = RequestApi("set_group_kick", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setGroupSpecialTitle(group_id: int, user_id: int, special_title: str):
        """
        设置群头衔
        Parameters:
            group_id (int): 群号
            user_id (int): 用户QQ号
            special_title (str): 专属头衔
        """
        param = {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title,
        }
        args = RequestApi("set_group_special_title", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getGroupHonorInfo(group_id: int):
        """
        获取群荣誉信息
        Parameters:
            group_id (int): 群号
        """
        param = {"group_id": group_id}
        args = RequestApi("get_group_honor_info", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getEssenceMsgList(group_id: int):
        """
        获取群精华消息
        Parameters:
            group_id (int): 群号
        """
        param = {"group_id": group_id}
        args = RequestApi("get_essence_msg_list", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setEssenceMsg(message_id: int):
        """
        设置群精华消息
        Parameters:
            message_id (int): 消息ID
        """
        param = {"message_id": message_id}
        args = RequestApi("set_essence_msg", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def deleteEssenceMsg(message_id: int):
        """
        删除群精华消息
        Parameters:
            message_id (int): 消息ID
        """
        param = {"message_id": message_id}
        args = RequestApi("delete_essence_msg", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getGroupRootFiles(group_id: int):
        """
        获取群根目录文件列表
        Parameters:
            group_id (int): 群号
        """
        param = {"group_id": group_id}
        args = RequestApi("get_group_root_files", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def uploadGroupFile(group_id: int, file: str, name: str, folder: str = "/"):
        """
        上传群文件
        Parameters:
            group_id (int): 群号
            file (str): 本地文件路径
            name (str): 文件名
            folder_id (str): 文件夹路径，默认根目录,文件夹id，可通过get_group_root_files获取
        """
        param = {"group_id": group_id, "file": file, "name": name, "folder": folder}
        args = RequestApi("upload_group_file", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def deleteGroupFile(group_id: int, file_id: str):
        """
        删除群文件
        Parameters:
            group_id (int): 群号
            file_id (str): 文件ID
        """
        param = {"group_id": group_id, "file_id": file_id}
        args = RequestApi("delete_group_file", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def createGroupFileFolder(group_id: int, name: str):
        """
        创建群文件文件夹
        Parameters:
            group_id (int): 群号
            name (str): 文件夹名
        """
        param = {"group_id": group_id, "name": name}
        args = RequestApi("create_group_file_folder", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def deleteGroupFolder(group_id: int, folder_id: str):
        """
        删除群文件文件夹
        Parameters:
            group_id (int): 群号
            folder_id (str): 文件夹ID
        """
        param = {"group_id": group_id, "folder_id": folder_id}
        args = RequestApi("delete_group_folder", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getGroupFileUrl(file_id: str):
        """
        获取群文件资源链接
        Parameters:
            file_id (str): 文件ID
        """
        param = {"file_id": file_id}
        args = RequestApi("get_group_file_url", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getGroupAtAllRemain(group_id: int):
        """
        获取群 @全体成员 剩余次数
        Parameters:
            group_id (int): 群号
        """
        param = {"group_id": group_id}
        args = RequestApi("get_group_at_all_remain", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def sendGroupNotice(group_id: int, content: str, image: str = ""):
        """
        发送群公告
        Parameters:
            group_id (int): 群号
            content (str): 公告内容
            image (str): 图片路径（可选）
        """
        param = {"group_id": group_id, "content": content, "image": image}
        args = RequestApi("_send_group_notice", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getGroupNotice(group_id: int):
        """
        获取群公告
        Parameters:
            group_id (int): 群号
        """
        param = {"group_id": group_id}
        args = RequestApi("_get_group_notice", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getGroupSystemMsg(group_id: int):
        """
        获取群系统消息
        """
        param = {"group_id": group_id}
        args = RequestApi("get_group_system_msg", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def getGroupIgnoreAddRequest(group_id: int):
        """
        获取已过滤的加群通知
        Parameters:
            group_id (int): 群号
            message_seq (int): 消息序号（可选）
        """
        param = {"group_id": group_id}
        args = RequestApi("get_group_ignore_add_request", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def sendGroupSign(group_id: int):
        """
        群打卡
        Parameters:
            group_id (int): 群号
        """
        param = {"group_id": group_id}
        args = RequestApi("send_group_sign", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setGroupMsgMask(group_id: int, option: int):
        """
        设置群消息接受方式
        Parameters:
            group_id (int): 群号
            option (int): 接收选项（1-接收并提醒，2-收到不提醒，3-屏蔽群消息）
        """
        param = {"group_id": group_id, "option": option}
        args = RequestApi("set_group_msg_mask", param)
        return await ApiAdapter.sendActionApi(args, 10)

    @staticmethod
    async def setGroupRemark(group_id: int, remark: str):
        """
        设置群备注
        Parameters:
            group_id (int): 群号
            remark (str): 群备注
        """
        param = {"group_id": group_id, "remark": remark}
        args = RequestApi("set_group_remark", param)
        return await ApiAdapter.sendActionApi(args, 10)
