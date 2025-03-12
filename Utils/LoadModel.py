# LoadModel.py
import pkgutil
import importlib
import inspect
from types import ModuleType
from typing import List, Type, Dict

# 缓存已导入的模块
imported_modules: Dict[str, ModuleType] = {}


# def findSubclasses(
#     pack_name: str, base_class: Type, reload_modules: bool = False
# ) -> List[Type]:
#     """
#     动态导入指定目录下的所有模块，并查找所有继承自指定类的子类
#     如果 reload_modules 为 True，则重新加载所有模块
#     """
#     package = importlib.import_module(name=pack_name)
#     package_path = package.__path__
#     package_prefix = package.__name__ + "."

#     subclasses = []

#     for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
#         full_module_name = package_prefix + module_name
#         if is_pkg:
#             # 如果是包，递归查找子类
#             subclasses.extend(
#                 findSubclasses(full_module_name, base_class, reload_modules)
#             )
#         else:
#             # 如果是模块，导入或重新加载模块
#             if reload_modules and full_module_name in imported_modules:
#                 module = importlib.reload(imported_modules[full_module_name])
#             else:
#                 module = importlib.import_module(full_module_name)
#                 imported_modules[full_module_name] = module

#             for name, cls in inspect.getmembers(module, inspect.isclass):
#                 if issubclass(cls, base_class) and cls is not base_class:
#                     subclasses.append(cls)

#     return subclasses


# LoadModel.py
import pkgutil
import importlib
import inspect
from types import ModuleType
from typing import List, Type, Dict

# 缓存已导入的模块
imported_modules: Dict[str, ModuleType] = {}


def findSubclasses(
    package_name: str, base_class: Type, reload_modules: bool = False
) -> List[Type]:
    """
    动态导入指定目录下的所有模块，并查找所有继承自指定类的子类
    如果 reload_modules 为 True，则重新加载所有模块
    """
    package = importlib.import_module(package_name)
    package_path = package.__path__
    package_prefix = package.__name__ + "."

    subclasses = []

    for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
        full_module_name = package_prefix + module_name
        if is_pkg:
            # 如果是包，递归查找子类
            subclasses.extend(
                findSubclasses(full_module_name, base_class, reload_modules)
            )
        else:
            # 如果是模块，导入或重新加载模块
            if reload_modules and full_module_name in imported_modules:
                module = importlib.reload(imported_modules[full_module_name])
            else:
                module = importlib.import_module(full_module_name)
                imported_modules[full_module_name] = module

            for name, cls in inspect.getmembers(module, inspect.isclass):
                if issubclass(cls, base_class) and cls is not base_class:
                    subclasses.append(cls)

    return subclasses
