import os
import sys
import importlib
import importlib.util
import inspect
from types import ModuleType
from typing import List, Type, Dict
from Utils.Logs import Log

# 缓存已导入的模块
imported_modules: Dict[str, ModuleType] = {}


def loadModuleFromFile(file_path: str, module_name: str | None = None) -> ModuleType:
    """
    从文件路径直接加载 Python 模块

    Args:
        file_path: Python 文件的完整路径
        module_name: 可选的模块名，如果不提供则使用文件名

    Returns:
        加载的模块对象
    """
    if module_name is None:
        module_name = os.path.splitext(os.path.basename(file_path))[0]

    # 使用 importlib.util 从文件路径加载模块
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法从 {file_path} 创建模块规范")

    module = importlib.util.module_from_spec(spec)

    # 将模块添加到 sys.modules 中，这样模块内的相对导入才能正常工作
    sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        # 如果加载失败，从 sys.modules 中移除
        if module_name in sys.modules:
            del sys.modules[module_name]
        raise ImportError(f"执行模块 {file_path} 时出错: {e}")


def findPluginsInDirectory(
    directory: str,
    base_class: Type,
    reload_modules: bool = False,
    recursive: bool = True,
    file_pattern: str = "*.py",
) -> List[Type]:
    """
    扫描目录中的所有 Python 文件，查找继承自指定基类的插件类

    Args:
        directory: 要扫描的目录路径
        base_class: 基类
        reload_modules: 是否重新加载已缓存的模块
        recursive: 是否递归扫描子目录
        file_pattern: 文件匹配模式（暂时只支持 *.py）

    Returns:
        找到的所有插件类列表
    """
    import glob

    if not os.path.exists(directory):
        Log.error(f"目录不存在: {directory}")
        return []

    if not os.path.isdir(directory):
        Log.error(f"路径不是目录: {directory}")
        return []

    plugins = []

    # 构建搜索模式
    if recursive:
        pattern = os.path.join(directory, "**", file_pattern)
        py_files = glob.glob(pattern, recursive=True)
    else:
        pattern = os.path.join(directory, file_pattern)
        py_files = glob.glob(pattern)

    # 过滤掉 __init__.py 文件（如果不想加载的话）
    py_files = [f for f in py_files if not f.endswith("__init__.py")]

    for file_path in py_files:
        try:
            # 生成唯一的模块名，避免冲突
            rel_path = os.path.relpath(file_path, directory)
            module_name = rel_path.replace(os.sep, ".").replace(".py", "")

            # 检查是否需要重新加载
            if reload_modules and file_path in imported_modules:
                # 重新加载模块
                try:
                    module = loadModuleFromFile(file_path, module_name)
                    imported_modules[file_path] = module
                except Exception as e:
                    Log.error(f"重新加载模块 {file_path} 失败: {e}")
                    continue
            elif file_path not in imported_modules:
                # 首次加载模块
                try:
                    module = loadModuleFromFile(file_path, module_name)
                    imported_modules[file_path] = module
                except Exception as e:
                    Log.error(f"加载模块 {file_path} 失败: {e}")
                    continue
            else:
                # 使用缓存的模块
                module = imported_modules[file_path]

            # 在模块中查找插件类
            for name, cls in inspect.getmembers(module, inspect.isclass):
                # 检查是否是基类的子类，且不是基类本身
                if (
                    issubclass(cls, base_class)
                    and cls is not base_class
                    and cls.__module__ == module_name
                ):  # 确保类定义在当前模块中
                    plugins.append(cls)
                    Log.info(f"找到插件: {cls.__name__} 在 {file_path}")

        except Exception as e:
            Log.error(f"处理文件 {file_path} 时出错: {e}")
            continue

    return plugins


def findPluginsFromFiles(
    file_paths: List[str], base_class: Type, reload_modules: bool = False
) -> List[Type]:
    """
    从指定的文件列表中查找插件类

    Args:
        file_paths: Python 文件路径列表
        base_class: 基类
        reload_modules: 是否重新加载已缓存的模块

    Returns:
        找到的所有插件类列表
    """
    plugins = []

    for file_path in file_paths:
        if not os.path.exists(file_path):
            Log.info(f"文件不存在: {file_path}")
            continue

        if not file_path.endswith(".py"):
            Log.info(f"跳过非Python文件: {file_path}")
            continue

        try:
            # 生成模块名
            module_name = os.path.splitext(os.path.basename(file_path))[0]

            # 检查是否需要重新加载
            if reload_modules and file_path in imported_modules:
                module = loadModuleFromFile(file_path, module_name)
                imported_modules[file_path] = module
            elif file_path not in imported_modules:
                module = loadModuleFromFile(file_path, module_name)
                imported_modules[file_path] = module
            else:
                module = imported_modules[file_path]

            # 在模块中查找插件类
            for name, cls in inspect.getmembers(module, inspect.isclass):
                if (
                    issubclass(cls, base_class)
                    and cls is not base_class
                    and cls.__module__ == module_name
                ):
                    plugins.append(cls)
                    Log.info(f"找到插件: {cls.__name__} 在 {file_path}")

        except Exception as e:
            Log.error(f"处理文件 {file_path} 时出错: {e}")
            continue

    return plugins
