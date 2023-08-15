import asyncio
import sys, signal
from exte.Logger import log
from exte.Register import flash_resgister
from exte.VoidUtil import playlist_handler
from ws.connect_ws import ConnectWs
from config.common import settings



class Bot:
    def __init__(self, token: str = '') -> None:
        """
        1. 注册信号处理函数,退出时关闭log文件,loop和终端
        2. 加载配置文件
        3. 加载map
        4. 启动ws通讯
        """
        log.setDebugMode(settings.debug)
        signal.signal(signal.SIGINT, self._signal_handler)


    def _signal_handler(self, signal, frame):
        loop = asyncio.get_event_loop()
        loop.stop()

        # 打印日志,并退出
        log.info("程序退出")
        log.close()
        sys.exit(0)



    async def connection(self):
        """
        连接socket
        """
        connect_ws = ConnectWs()
        await connect_ws.run()



    async def main(self):
        tasks = [asyncio.create_task(task) for task in [self.connection(), playlist_handler()]]
        # tasks = [asyncio.create_task(task) for task in [self.connection()]]
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        


    def run(self):
        if flash_resgister():
            # pass
            asyncio.run(self.main())
        else:
            raise RuntimeError("命令注册失败")    



if __name__ == '__main__':
    bot = Bot()
    bot.run()