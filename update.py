"""
插件依赖自动安装脚本
自动扫描插件目录并使用uv安装依赖
"""

import subprocess
import threading
import random
import time
from pathlib import Path
import colorama
from Utils.Logs import Log


class SpinnerAnimation:
    """转圈动画类"""

    def __init__(self, message="更新中"):
        self.message = message
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        # 随机颜色
        self.colors = [
            colorama.Fore.RED,
            colorama.Fore.GREEN,
            colorama.Fore.YELLOW,
            colorama.Fore.BLUE,
            colorama.Fore.MAGENTA,
            colorama.Fore.CYAN,
            colorama.Fore.WHITE,
        ]
        self.running = False
        self.thread = None

    def _animate(self):
        i = 0
        while self.running:
            print(
                f"\r{random.choice(self.colors)} {self.spinner_chars[i % len(self.spinner_chars)]} {self.message}",
                end="",
                flush=True,
            )
            time.sleep(0.1)
            i += 1

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("\r", end="", flush=True)  # 清除当前行


def check_uv():
    """检查uv是否可用"""
    spinner = SpinnerAnimation("检查核心中的uv版本")
    spinner.start()

    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        spinner.stop()

        if result.returncode == 0:
            Log.info(f"✓ 找到uv: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    except Exception as e:
        spinner.stop()
        Log.error(f"⚠️ 检查uv时出现问题: {e}")

    spinner.stop()
    Log.error("❌ 未找到uv，请先安装uv")
    Log.error(
        '安装方法:powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'
    )
    return False


def find_requirements_file(plugin_path):
    """在插件目录中查找requirements文件"""
    possible_paths = [
        plugin_path / "requirements.txt",
        plugin_path / "requirements" / "requirements.txt",
    ]

    # 检查标准位置
    for req_path in possible_paths:
        if req_path.exists():
            return req_path

    # 查找requirements目录下的所有txt文件
    req_dir = plugin_path / "requirements"
    if req_dir.exists():
        for txt_file in req_dir.glob("*.txt"):
            return txt_file

    # 查找插件根目录下包含"req"的txt文件
    for txt_file in plugin_path.glob("*req*.txt"):
        return txt_file

    return None


def install_requirements(req_file):
    """使用uv安装requirements文件中的依赖"""
    Log.info(f"📦 正在安装: {req_file}")

    # 显示requirements文件内容
    try:
        with open(req_file, "r", encoding="utf-8") as f:
            requirements = f.read().strip()
            if requirements:
                print(f"💼 依赖列表:")
                for line in requirements.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        print(f"   - {line}")
    except Exception as e:
        Log.error(f"⚠️ 无法读取requirements文件: {e}\n")

    try:
        # 使用实时输出模式
        Log.info("🔄 开始安装...")
        process = subprocess.Popen(
            ["uv", "pip", "install", "-r", str(req_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            universal_newlines=True,
        )

        # 实时显示输出
        output_lines = []
        while True:
            if process.stdout is not None:
                output = process.stdout.readline()
            else:
                output = None

            if output == "" and process.poll() is not None:
                break
            if output:
                line = output.strip()
                if line:
                    print(f"   {line}")
                    output_lines.append(line)

        return_code = process.poll()

        if return_code == 0:
            Log.info("✓ 安装成功")
            return True
        else:
            Log.error(f"❌ 安装失败 (返回码: {return_code})")
            return False

    except Exception as e:
        Log.error(f"❌ 安装出错: {e}")
        return False


def updataPluginsDependencies():
    """
    自动安装插件依赖
    """

    Log.info("🚀 开始插件依赖自动安装...")

    # 配置 - 自动检测插件目录名
    possible_dirs = ["plugins", "Plugins", "plugin", "Plugin"]
    plugin_dir = None

    for dir_name in possible_dirs:
        if Path(dir_name).exists():
            plugin_dir = Path(dir_name)
            break

    if plugin_dir is None:
        plugin_dir = Path("plugins")  # 默认值

    # 检查插件目录是否存在
    if not plugin_dir.exists():
        Log.error(f"❌ 插件目录 '{plugin_dir}' 不存在")
        return

    # 检查uv是否可用
    if not check_uv():
        return

    Log.info(f"📁 扫描插件目录: {plugin_dir}")

    # 统计变量
    total_plugins = 0
    success_count = 0
    failed_plugins = []

    # 扫描所有插件目录
    for plugin_path in plugin_dir.iterdir():
        if not plugin_path.is_dir():
            continue

        plugin_name = plugin_path.name
        Log.info(f"🔍 检查插件: {plugin_name}")

        # 查找requirements文件
        req_file = find_requirements_file(plugin_path)

        if req_file:
            total_plugins += 1
            try:
                rel_path = req_file.relative_to(Path.cwd())
                Log.info(f"📋 找到requirements文件: {rel_path}")
            except ValueError:
                Log.info(f"📋 找到requirements文件: {req_file}")

            if install_requirements(req_file):
                success_count += 1
            else:
                failed_plugins.append(plugin_name)
        else:
            Log.info("未找到requirements文件，不需要进行更新")

        print("-" * 40)

    print("=" * 40)
    print("自检结果:")
    print("=" * 40)
    print(f"发现插件数量: {total_plugins}")
    print(f"成功安装: {success_count}")
    print(f"安装失败: {len(failed_plugins)}")

    if failed_plugins:
        print("❌ 安装失败的插件:")
        for plugin in failed_plugins:
            print(f"  - {plugin}")
        print("建议检查:")
        print("  - requirements文件格式是否正确")
        print("  - 网络连接是否正常")
        print("  - uv配置是否正确")
        exit(1)
    elif success_count > 0:
        print("所有插件依赖安装成功！")
    else:
        print("没有找到需要安装的插件依赖")

    Log.info("✅ 系统更新完成！")


def removeUnusedDependencies():
    """
    移除未使用的依赖
    """

    print("🚀 开始移除未使用的依赖...")
    if not check_uv():  # 检查uv是否可用
        return False

    process = subprocess.Popen(
        ["uv", "sync"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        universal_newlines=True,
    )
    # 实时显示输出
    output_lines = []
    while True:
        if process.stdout is not None:
            output = process.stdout.readline()
        else:
            output = None

        if output == "" and process.poll() is not None:
            break
        if output:
            line = output.strip()
            if line:
                print(f"   {line}")
                output_lines.append(line)

    return_code = process.poll()

    if return_code == 0:
        Log.info("✓ 安装成功")
        return True
    else:
        Log.error(f"❌ 清理依赖失败 (返回码: {return_code})")
        return False
