from typing import Any
import colorama

# 自动重置颜色
colorama.init(autoreset=True)


class Log:
    """
    简单的日志类
    包含五个方法: info, warning, error,adapter,apiResponse
    """

    pluginErrorList: dict[str, list[str]] = {}

    @staticmethod
    def info(msg: Any) -> None:
        """
        输出普通信息
        """
        print(f"{colorama.Fore.GREEN}\n信息:{msg}")

    @staticmethod
    def debug(msg: Any) -> None:
        """
        输出警告信息
        """
        print(f"{colorama.Fore.BLUE}\n调试:{msg}")

    @staticmethod
    def warning(msg: Any) -> None:
        """
        输出警告信息
        """
        print(f"{colorama.Fore.YELLOW}\n警告:{msg}")

    @staticmethod
    def error(msg: Any) -> None:
        """
        输出错误信息
        """
        print(f"{colorama.Fore.RED}\n错误:{msg}")

    @staticmethod
    def pluginError(pluginName: str, msg: Any) -> None:
        """
        输出并记录插件错误信息
        """
        print(f"{colorama.Fore.RED}\n错误:{msg}")
        if pluginName in Log.pluginErrorList:
            Log.pluginErrorList[pluginName].append(msg)
        else:
            Log.pluginErrorList[pluginName] = []
            Log.pluginErrorList[pluginName].append(msg)

    @staticmethod
    def adapter(msg: Any) -> None:
        """
        输出收到的上报消息
        """
        print("\n上报消息:", msg)

    @staticmethod
    def apiResponse(msg: Any) -> None:
        """
        输出API返回的消息
        """
        print(f"{colorama.Fore.GREEN}\nAPI返回消息:", msg)
