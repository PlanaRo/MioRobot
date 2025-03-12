from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
from Utils.Logs import Log
import json
import threading
from config import Config


import psutil
import importlib.util
import getpass
import platform
import ast
import astor
from PluginLoader import PluginLoaderControl
from GroupControl import GroupControl
from Models.Api.BaseApi import RequestApi, ApiAdapter
from pynvml import *
from Net.Receives import recv
import os


appHttp = FastAPI()


@appHttp.get("/bot_info")
async def bot_info():
    """
    获取bot账号信息
    """
    api = "get_login_info"
    param = {0: 0}
    args = RequestApi(api, param)
    iii = await ApiAdapter.sendActionApi(recv.websocket, args, 5)
    return iii["data"]


@appHttp.get("/plugin_error_list")
async def plugin_error_list():
    """
    获取插件报错记录
    """
    return Log.plugin_error_list


@appHttp.post("/plugin_trigger_list")
async def plugin_trigger_list(request: Request):
    """
    获取插件触发记录（时间戳）
    """
    post_data = await request.json()
    callback_name = post_data.get("callback_name")
    return {callback_name: PluginLoaderControl.trigger_list[callback_name].runtime}


@appHttp.get("/group_list")
async def get_features():
    """
    获取群列表
    """
    with open("Cacha\group_list.json", "r", encoding="utf-8") as file:
        group_data = json.load(file)
    return group_data


@appHttp.post("/group_list")
async def post_features(request: Request):
    """
    修改群启用
    """
    with open("Cacha\group_list.json", "r", encoding="utf-8") as file:
        group_data = json.load(file)
    post_data = await request.json()
    group_id = post_data.get("group_id")
    NEW_is_enable = post_data.get("is_enable")
    for group in group_data:
        if group["group_id"] == group_id:
            group["is_enable"] = NEW_is_enable

    with open("Cacha/group_list.json", "w", encoding="utf-8") as file:
        json.dump(group_data, file, ensure_ascii=False, indent=4)

    await GroupControl.get_group_data()
    return {"message": "OK"}


def run_api():
    from Models.Api.modelModApi import openapi_qwen2

    uvicorn.run(
        "Models.Api.modelModApi.openapi_qwen2:app", host="0.0.0.0", port=6006, workers=1
    )


@appHttp.get("/modelModApi")
async def modelModApi():
    """
    运行模型
    """
    thread = threading.Thread(target=run_api)
    thread.start()
    return {"message": "OK"}


@appHttp.get("/get_cpu_usage")
async def get_cpu_usage():
    """
    获取总CPU使用率
    """
    usage = psutil.cpu_percent(interval=1)
    return {"cpu_usage": usage}


@appHttp.get("/get_free_memory")
async def get_free_memory():
    """
    获取剩余内存（单位：GB）
    """
    virtual_memory = psutil.virtual_memory()
    free_memory_gb = round(virtual_memory.free / (1024.0**3), 2)
    return {"free_memory_gb": free_memory_gb}


@appHttp.get("/get_memory_usage")
async def get_memory_usage():
    """
    获取内存使用率
    """
    virtual_memory = psutil.virtual_memory()
    memory_usage = round((virtual_memory.used / virtual_memory.total) * 100, 2)
    return {"memory_usage": memory_usage}


@appHttp.get("/get_system")
async def get_username():
    """
    获取当前系统硬件信息
    """
    try:
        nvmlInit()
        nvidia_countt = nvmlDeviceGetName(nvmlDeviceGetHandleByIndex(0))
    except NVMLError as _:
        nvidia_countt = "No NVIDIA GPUs found"
    finally:
        try:
            nvmlShutdown()
        except:
            pass
    username = getpass.getuser()
    u_name = platform.uname()
    processor_name = platform.processor()
    memory = int(round(psutil.virtual_memory().total, 2) / (1024.0**3))
    time = psutil.boot_time()
    for disk_partition in psutil.disk_partitions():
        o_usage = psutil.disk_usage(disk_partition.device)
    return {
        "username": username,
        "system_name": u_name.system + u_name.version,
        "gpu_name": nvidia_countt,
        "system_memory": memory,
        "cpu_model": processor_name,
        "start_time": time,
        "eisk": int(o_usage.total / (1024.0**3)),
    }


@appHttp.get("/get_nvidia_gpu_memory_usage")
async def get_nvidia_gpu_memory_usage():
    """
    获取所有NVIDIA GPU的显存使用情况
    """
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        memory_info = nvmlDeviceGetMemoryInfo(handle)
        used_memory_percentage = (
            round((memory_info.used / memory_info.total) * 100, 2)
            if memory_info.total > 0
            else 0
        )
    except NVMLError as _:
        used_memory_percentage = "No NVIDIA GPUs found"
    finally:
        try:
            nvmlShutdown()
        except:
            pass
    return {"memory_usage": used_memory_percentage}


@appHttp.get("/get_nvidia_gpu_utilization")
async def get_nvidia_gpu_utilization():
    """
    获取所有NVIDIA GPU的利用率
    """
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        utilization = nvmlDeviceGetUtilizationRates(handle).gpu
    except NVMLError as _:
        utilization = "No NVIDIA GPUs found"
        try:
            nvmlShutdown()
        except:
            pass
    return {"utilization": utilization}


def load_Plugin(module_path):
    try:
        # 检查文件是否存在
        if not os.path.exists(module_path):
            raise FileNotFoundError(f"模块文件未找到: {module_path}")

        # 动态加载模块
        spec = importlib.util.spec_from_file_location("module.name", module_path)
        if spec is None:
            raise ImportError(f"无法创建模块spec: {module_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 获取模块中的数据属性
        author = getattr(module, "author_data", "未提供作者信息")
        name = getattr(module, "name_data", "未提供名称")
        display_name = getattr(module, "display_name_data", "未提供显示名称")
        version = getattr(module, "version_data", "未提供版本号")
        description = getattr(module, "description_data", "未提供描述")
        setting = getattr(module, "setting_data", "未提供设置信息")
        developer_setting = getattr(
            module, "developer_setting_data", "未提供开发者设置信息"
        )

        return {
            "setting": setting,
            "author": author,
            "name": name,
            "display_name": display_name,
            "version": version,
            "description": description,
            "developer_setting": developer_setting,
        }

    except FileNotFoundError as fnf_error:
        print(f"文件错误: {fnf_error}")
    except ImportError as import_error:
        print(f"导入错误: {import_error}")
    except AttributeError as attr_error:
        print(f"属性错误: {attr_error}")
    except Exception as e:
        print(f"发生未知错误: {e}")
    return None  # 如果出错返回None或其他合适的值


@appHttp.get("/plugin_list")
async def get_plugin_list():
    """
    插件列表
    """
    plugin_list = os.listdir("Plugin")
    plugin_list_r = {}
    for plugin_name in plugin_list:
        module_path = f"Plugin/{plugin_name}/__init__.py"
        plugin_list_r[plugin_name] = load_Plugin(module_path)

    return plugin_list_r


class UpdateLoadValue(ast.NodeTransformer):
    def __init__(self, new_load_value):
        self.new_load_value = new_load_value

    def visit_Assign(self, node):
        if not node.targets:
            return node

        target = node.targets[0]
        if isinstance(target, ast.Name):
            target_id = target.id

            # Mapping of variable names to keys in new_load_value
            key_map = {
                "author_data": "author",
                "name_data": "name",
                "display_name_data": "display_name",
                "version_data": "version",
                "description_data": "description",
                "developer_setting_data": "developer_setting",
                "setting_data": "setting",
            }

            if target_id in key_map:
                key = key_map[target_id]
                new_value = self.new_load_value.get(key)

                if new_value is not None:
                    # Convert new_value to appropriate AST node
                    node.value = self.value_to_ast_node(new_value)
        return node

    def value_to_ast_node(self, value):
        """Convert a Python value to the corresponding AST node."""
        if isinstance(value, (str, int, float, bool, type(None))):
            return ast.Constant(value=value)
        elif isinstance(value, dict):
            keys = [self.value_to_ast_node(k) for k in value.keys()]
            values = [self.value_to_ast_node(v) for v in value.values()]
            return ast.Dict(keys=keys, values=values)
        elif isinstance(value, list):
            elts = [self.value_to_ast_node(v) for v in value]
            return ast.List(elts=elts, ctx=ast.Load())
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")


def update_setting_data(file_path, new_setting_data_value):
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()

    tree = ast.parse(source)

    transformer = UpdateLoadValue(new_setting_data_value)
    transformer.visit(tree)
    ast.fix_missing_locations(tree)

    try:
        updated_source = ast.unparse(tree)  # Python 3.9+后使用
    except AttributeError:
        updated_source = astor.to_source(tree)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_source)


@appHttp.post("/plugin_list")
async def post_plugin_list(request: Request):
    """
    管理插件
    """
    post_data = await request.json()
    callback_name_path = post_data.get("callback_name")
    setting_data_path = post_data.get("setting_data")

    module_path = f"Plugin/{callback_name_path}/__init__.py"
    update_setting_data(module_path, setting_data_path)
    PluginLoaderControl.reload()
    return {"message": "OK"}
