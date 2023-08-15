import aiohttp
import aiofiles
import json
from typing import Union


from config.common import settings
from exte.URLGenerator import kook_api
from exte.Logger import log


headers = {
    "Authorization": f"{settings.token_type} {settings.token}",
    "X-Rate-Limit-Limit": "5",
    "X-Rate-Limit-Remaining": "0",
    "X-Rate-Limit-Reset": "14",
    "X-Rate-Limit-Bucket": "user/info",
    "X-Rate-Limit-Global": ""
}

kook_api = kook_api.api

class KookApi:

    @staticmethod
    async def make_kook_request(url, method='GET', params=None, data=None, json_data=None, **kw) -> json or None:
        """
        request模板
        returns json
        """
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.request(method, url, params=params, data=data, json=json_data, **kw) as resp:
                    resp.raise_for_status()
                    return await resp.json()
            except Exception as e:
                log.error(f'Error occurred during request: {e}')
                return None
            


            
    @staticmethod
    async def send_channel_message(channel_id: str, msg_type: int, msg: str, msgId: str = '') -> json or None:
        """
        params channel_id: 聊天频道id
        params msg_type: 消息类型
        params msg: 消息
        params msgId: 回复的消息id
        """
        url = kook_api.message.create.str

        json_data = {
            "type": msg_type,
            "target_id": channel_id,
            "content": msg,
        }
        if msgId:
            json_data["quote"] = msgId

        response = await KookApi.make_kook_request(url, method='POST', json_data=json_data)
        return response
    
    @staticmethod
    async def send_channel_card():
        pass


    @staticmethod
    async def upload_files(file_byte: bytes) -> str:
        """
        params file_byte: 文件字节
        returns 图片url
        """
        url = kook_api.asset.create.str
        file_data = aiohttp.FormData()
        try:
            # async with aiofiles.open(file_path, "rb") as file:
            file_data.add_field("file", file_byte, filename="file.txt")
            response = await KookApi.make_kook_request(url, method='POST', data=file_data)
            return response
        except FileNotFoundError as error:
            log.error(error)

    @staticmethod
    async def get_joined_channel(user_id: str, guild_id: str, page: int = 1, page_size: int = 10) -> json or None:
        """
        params user_id: 用户id
        params guild_id: 频道id
        params page: 页数
        params page_size: 每页数量
        returns json
        """
        url = kook_api.channel_user.get_joined_channel.str
        params = {
            "user_id": user_id,
            "guild_id": guild_id,
            "page": page,
            "page_size": page_size
        }
        response = await KookApi.make_kook_request(url, method='GET', params=params)
        return response            
    


if __name__ == '__main__':
    import asyncio
    asyncio.run(KookApi.send_channel_message('1', 1, 'hello world'))