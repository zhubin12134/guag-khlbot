from pydantic import BaseSettings
from typing import List, Dict


class CommonSettings(BaseSettings):
    debug: bool = False

    token_type: str = 'Bot'
    token: str = ""

    channel_id: str = "5531049522346518"

    register_file: List[str] = ["app.py"]
    registered_functions: dict = {}
    register_startswith: str = "+"

    image_path: str = "./images"

    font: str = "./fonts/msyh.ttc"

    ffmpg_path: str = "ffmpeg"

    music_path: str = "./music"
    music_list: List = []
    music_play: List = []
    cut: bool = False


    class Config:
        env_file = ".env"


settings = CommonSettings()
