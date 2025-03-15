from Net.CoreServer import coreServer
from Utils.Logs import Log
import asyncio


async def main():
    # 初始化配置
    # 启动api服务
    httpStart = asyncio.create_task(coreServer.httpStart())
    # 启动核心服务
    Start = asyncio.create_task(coreServer.start())
    await asyncio.gather(Start, httpStart)


if __name__ == "__main__":
    Log.info("正在启动澪...")
    asyncio.run(main())
