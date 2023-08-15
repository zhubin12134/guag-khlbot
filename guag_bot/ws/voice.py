import asyncio
import time
import aiohttp
import random
import json

from aiohttp import ClientWebSocketResponse
from typing import List

from .voice_json import voice_json
from exte.URLGenerator import kook_api
from exte.Logger import log
from config.common import settings


class VoidClientSocket:
    ws_clients: List[ClientWebSocketResponse] = []
    wait_handler_msgs = []
    rtp_url = ""
    
    is_exit: bool = False
    

    async def get_gateway(self):

        gateway_url = kook_api.api.gateway.voice.str
        async with aiohttp.ClientSession() as session:
            async with session.get(gateway_url, 
                                   params={"channel_id": settings.channel_id}, 
                                   headers={'Authorization': f'{settings.token_type} {settings.token}'}
                                   ) as resp:
                result = await resp.json()
                log.debug(f"result: {result}")
                if result["code"] == 0:
                    return result['data']['gateway_url']
                else:
                    log.error(f"推流地址获取失败: {result}")
                    return


    async def connect_ws(self):
        gateway = await self.get_gateway()
        if not gateway:
            return
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64,ssl=False)) as session:
            async with session.ws_connect(gateway) as ws:
                self.ws_clients.append(ws)
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        if (len(self.ws_clients) != 0) and (self.ws_clients[0] == ws):
                            self.wait_handler_msgs.append(msg.data)
                            if self.is_exit:
                                return
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break
                    else:
                        break


    

    async def ws_ping(self):
        ping_time = 0.0
        while not self.is_exit:  # 在循环内部检查 self.is_exit
            await asyncio.sleep(0.1)
            if len(self.ws_clients) == 0:
                continue
            now_time = time.time()
            if now_time - ping_time >= 30:
                await self.ws_clients[0].ping()
                ping_time = now_time


    async def ws_msg(self):
        while True:
            if len(self.ws_clients) != 0:
                break
            await asyncio.sleep(0.1)
            if self.is_exit:
                return
        a = voice_json
        a['1']['id'] = random.randint(1000000, 9999999)
        await self.ws_clients[0].send_json(a['1'])
        now = 1
        ip = ''
        port = 0
        rtcp_port = 0
        while not self.is_exit:
            if len(self.wait_handler_msgs) != 0:
                data = json.loads(self.wait_handler_msgs.pop(0))
                
                if now == 1:
                    print(__name__, '1:', data)
                    a['2']['id'] = random.randint(1000000, 9999999)
                    print('2:', a['2'])
                    await self.ws_clients[0].send_json(a['2'])
                    now = 2
                elif now == 2:
                    print('2:', data)
                    a['3']['id'] = random.randint(1000000, 9999999)
                    print('3:', a['3'])
                    await self.ws_clients[0].send_json(a['3'])
                    now = 3
                elif now == 3:
                    print('3:', data)
                    transport_id = data['data']['id']
                    ip = data['data']['ip']
                    port = data['data']['port']
                    rtcp_port = data['data']['rtcpPort']
                    a['4']['data']['transportId'] = transport_id
                    a['4']['id'] = random.randint(1000000, 9999999)
                    print('4:', a['4'])
                    await self.ws_clients[0].send_json(a['4'])
                    now = 4
                elif now == 4:
                    print('4:', data)
                    print(f'ssrc=1357 ffmpeg rtp url: rtp://{ip}:{port}?rtcpport={rtcp_port}')
                    rtp_url = f'rtp://{ip}:{port}?rtcpport={rtcp_port}'
                    print(f"rtcp_port: {rtp_url}")
                    self.rtp_url = rtp_url
                    now = 5
                else:
                    if 'notification' in data and 'method' in data and data['method'] == 'disconnect':
                        print('The connection had been disconnected', data)
                    else:
                        pass
            await asyncio.sleep(0.1)


    async def stop(self):
        self.is_exit = True
        for ws in self.ws_clients:
            await ws.close()
        self.ws_clients.clear()

    async def main(self):
        tasks = [asyncio.create_task(task) for task in [self.connect_ws(), self.ws_msg(), self.ws_ping()]]
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)



if __name__ == '__main__':
    c = VoidClientSocket()
    asyncio.run(c.main())
    print(c.rtp_url)