import json
import os
from typing import List
from munch import DefaultMunch

from API.api_kook import KookApi
from exte.Logger import log
from exte.CardMessage import Card
from exte.Musc import Musc
from config.common import settings




class Messags:
    
    type_map: dict = {
        1:"文字信息",
        2:"图片信息",
        3:"视频信息",
        4:"文件信息",
        8:"音频信息",
        9:"KMarkdown信息",
        10:"card信息",
        255:"系统信息"
    }

    
    def __init__(self, msg:json) -> None:
        self.obj: DefaultMunch = DefaultMunch.fromDict(msg, default=" ")
        self.extra: DefaultMunch = DefaultMunch.fromDict(self.obj.extra, default=" ")
        self._extra_map()

    def _extra_map(self):
        if not self.extra:
            return
        if self.obj.type in [2, 3, 4, 8, 255]:
            self.is_bot: bool = True
            return
        
        self.kmarkdown: DefaultMunch = DefaultMunch.fromDict(self.extra.kmarkdown)

        
        self.mentions = [DefaultMunch.fromDict(user) for user in self.kmarkdown.mention_part] if self.extra.mention else []

        self.is_bot: bool = self.extra.author.bot

    @property
    async def void_channel_id(self):
        resp = await KookApi.get_joined_channel(
            user_id=self.obj.author_id,
            guild_id=self.extra.guild_id,
        )
        if resp["code"] == 0:
            return resp["data"]["items"][0]["id"]
        else:
            return None

    def __repr__(self) -> str:
        if self.obj.type != 255:
            return "类型: {}, 频道: {}, 用户: {}, 发送了: {}".format(
                self.type_map.get(self.obj.type), self.obj.target_id, self.extra.author.username, self.obj.content
            )
        else:
            return "类型: {} 频道: {} 事件: xxx" .format(
                self.type_map.get(self.obj.type), self.obj.target_id
            )

    

    async def send_channel_message(self, message: str, quote: bool = False) -> None:
        msgId = self.obj.msg_id if quote else ""
        resp = await KookApi.send_channel_message(
            channel_id=self.obj.target_id, 
            msg_type=1, 
            msg=message,
            msgId=msgId
            )
        log.debug(f"请求结果: {resp}")


    async def send_channenl_image(self, file_name: str):
        file_path = os.path.join(settings.image_path, file_name)
        result = await KookApi.upload_files(channel_id=self.obj.target_id, file_path=file_path)
        if result.get("code") == 0:
            img_url = result.get("data").get("url")
            await KookApi.send_channel_message(channel_id=self.obj.target_id, msg_type=2, msg=img_url)
        else:
            log.error(f"url获取失败: {result.get('message')}")


    async def send_channenl_image_byte(self, file_byte: bytes):
        result = await KookApi.upload_files(file_byte=file_byte)
        if result.get("code") == 0:
            img_url = result.get("data").get("url")
            await KookApi.send_channel_message(channel_id=self.obj.target_id, msg_type=2, msg=img_url)
        else:
            log.error(f"url获取失败: {result.get('message')}")
    


    async def send_channel_card(self, card: Card):
        if not isinstance(card, Card):
            log.error("请传入正确的card")
            return
        
        resp = await KookApi.send_channel_message(
            channel_id=self.obj.target_id, 
            msg_type=10, 
            msg=card.to_str(),
            )
        log.debug(f"请求结果: {resp}")


    async def add_playlist(self, music: Musc):
        if not isinstance(music, Musc):
            log.error("请传入正确的music")
            return
        
        settings.music_list.append(music)





