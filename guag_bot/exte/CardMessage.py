from exte.Logger import log

class Card():
    def __init__(self, type: str, foo: str, ) -> None:
        pass

    def append(self, text: str) -> None:
        pass
    

    def to_str(self) -> str:
        return 
    

class modules():
    
    @staticmethod
    def test(txt):
        pass



async def card_test():
    card = [
        {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "modules": [
            {
                "type": "section",
                "text": {
                "type": "plain-text",
                "content": "KOOK：专属游戏玩家的文字、语音与组队工具。"
                }
            }
            ]
        }
    ]   
    import json
    msg = json.dumps(card, separators=(',', ':'))
    print(msg)
    # await send_channel_card(msg)