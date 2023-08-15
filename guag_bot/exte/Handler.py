import json
from exte.Logger import log
from exte.Message import Messags
from config.common import settings

class Handler:
    def __init__(self, msg: json):
        self.msg = Messags(msg)
        log.info(f"{self.msg}")


    async def handler(self):
        log.debug(f"是否为机器人: {self.msg.is_bot}")
        if self.msg.is_bot: # 判断是否为机器人发的消息
            return
        
        if not self.msg.obj.content.startswith(settings.register_startswith): # 是否为/ 开头
            return

        split_content = self.msg.obj.content.split(" ", 1) # 切割消息,获取命令和参数
      
        if func := settings.registered_functions.get(split_content[0][1:]): # 从注册中心获取函数
            try:
                if len(split_content) > 1:  # 如果有参数
                    await func(self.msg, split_content[1])
                else: # 如果没有参数
                    await func(self.msg)
            except:
                pass



        