import asyncio
import copy
import subprocess


from ws.voice import VoidClientSocket
from config.common import settings



class PlayHandler:


    def __init__(self):
        self.channel_id = copy.copy(settings.channel_id)
        self.void = VoidClientSocket()
    

    async def handler(self):
        while True:
            if self.void.rtp_url:
                rtp_url = self.void.rtp_url  # 获取 rtp 推流链接
                break
            await asyncio.sleep(0.1)

        rtp_cmmand = f"{settings.ffmpg_path} -re -loglevel level+info -nostats -stream_loop -1 -i zmq:tcp://127.0.0.1:1234 -map 0:a:0 -acodec libopus -ab 128k -filter:a volume=0.8 -ac 2 -ar 48000 -f tee [select=a:f=rtp:ssrc=1357:payload_type=100]{rtp_url}"
        rtp_prcess = await asyncio.create_subprocess_shell(rtp_cmmand,
                                                            stdout=subprocess.DEVNULL,
                                                            stderr=subprocess.DEVNULL)

        while True:
            if (len(settings.music_list) == 0) or (self.channel_id != settings.channel_id):
                # await asyncio.create_subprocess_shell("TASKKILL /F /PID {pid} /T".format(pid=rtp_prcess.pid), 
                await asyncio.create_subprocess_shell(f"pkill -TERM -P {rtp_prcess.pid}", 
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
                await self.void.stop()
                return
            
            
            play_info = settings.music_list.pop(0)
            audio_path = play_info.file  # 获取文件路径

            # 开始推流
            command = f'{settings.ffmpg_path} -re -nostats -i "{audio_path}" -acodec libopus -ab 128k -f mpegts zmq:tcp://127.0.0.1:1234'
            p = await asyncio.create_subprocess_shell(command, 
                                                      stdout=subprocess.DEVNULL,
                                                      stderr=subprocess.DEVNULL)
            
            
            while True:
                # 判断当前歌曲是否推流结束
                if settings.cut:
                    await asyncio.create_subprocess_shell(f"pkill -TERM -P {p.pid}", 
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
                    
                    settings.cut = False
                    if settings.music_play:
                        settings.music_play.pop(0)
                    break

                await asyncio.sleep(0.1)
            await asyncio.sleep(2)

                


    async def main(self):
        tasks = [asyncio.create_task(task) for task in [self.void.main(), self.handler()]]
        try:
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        except Exception as e:
            print(e)



async def playlist_handler():
    while True:
        if len(settings.music_list) == 0:
            await asyncio.sleep(0.1)
        else:
            await PlayHandler().main()