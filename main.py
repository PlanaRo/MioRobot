from Net.Receives import recv
from Utils.Logs import Log
import asyncio


async def main():
    # 初始化配置
    # 启动api服务
    # httpStart = asyncio.create_task(recv.httpStart())
    # 启动核心服务
    Start = asyncio.create_task(recv.start())
    # await asyncio.gather(httpStart, Start)
    await asyncio.gather(Start)


if __name__ == "__main__":
    Log.info("正在启动澪...")
    asyncio.run(main())
