import json
import asyncio
import websockets
import zlib
import time
import aiohttp
from aiohttp import ClientWebSocketResponse
from typing import List

from config.common import settings
from exte.URLGenerator import kook_api
from exte.Logger import log
from exte.Handler import Handler



class ConnectWs:

    ws_clients: List[ClientWebSocketResponse] = []
    
    mesgs: List[str] = []

    sn: int = 0

    ping_status: dict = {"date": time.time(), "status":{}}

    async def get_ws(self, token_type: str, token: str) -> json:
        # url = 'https://www.kookapp.cn/api/v3/gateway/index'
        url = kook_api.api.gateway.index.str
        headers = {
            "Authorization": f"{token_type} {token}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                log.info(f"网关获取中, code: {resp.status}")

                if resp.status == 200:
                    result = await resp.json()
                    log.debug(result)

                    if result['code'] != 0:
                        raise RuntimeError(f"网关获取失败,message: {result.get('message')}")
                    
                    log.info("网关获取成功")
                    return (result.get('data').get('url'))
                
                else:
                    raise RuntimeError(f"网关获取失败,code: {resp.status}")


    async def connect_ws(self, ws_url):
        while True:
            async with websockets.connect(ws_url) as ws:
                self.ws_clients.append(ws)
                async for msg in ws:
                    data = json.loads(zlib.decompress(msg))  # 解压缩
                    log.debug(data)
                    await self.msg_filter(data)



        
    async def msg_filter(self, msg: json):
        if msg["s"] == 0:
            self.sn = msg.get("sn")
            await Handler(msg["d"]).handler()
        elif msg["s"] == 1:
            log.info("登录成功")
        elif msg["s"] == 3:
            self.ping_status["date"] = time.time()
            self.ping_status["status"] = msg
        elif msg["s"] == 5:
            raise RuntimeError("请重新连接")
        elif msg["s"] == 6:
            raise RuntimeError("请重新连接")
        else:
            raise RuntimeError("未知错误")



    async def ws_ping(self):
        while True:
            if len(self.ws_clients) != 0:
                break
            await asyncio.sleep(0.1)
            
        ping_time = 0.0
        while True:
            await asyncio.sleep(0.1)
            if len(self.ws_clients) == 0:
                return
            

            now_time = time.time()
            if now_time - ping_time >= 30:  # 每30秒发一次ping包
                ping_msg = json.dumps({"s": 2, "sn": self.sn}, separators=(',', ':'))
                await self.ws_clients[0].send(ping_msg.encode())
                ping_time = now_time
                log.debug(f"发送了ping, sn: {self.sn}")


                while True:
                    if abs(ping_time - time.time()) < 6:  # 如果6秒内收到 {'s':3} 则判断连接状态正常
                        await asyncio.sleep(0.1)
                        if self.ping_status.get("date") >= ping_time:
                            if self.ping_status.get("status").get("s") == 3:
                                log.debug(f"收到pong: {self.ping_status}")
                                break
                    else:
                        log.debug(f"{self.ping_status}")
                        raise RuntimeError("ping超时,连接断开")  



        
    async def run(self):
        ws = await self.get_ws(token_type=settings.token_type, token=settings.token)
        tasks = [asyncio.create_task(task) for task in [self.connect_ws(ws), self.ws_ping()]]
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)