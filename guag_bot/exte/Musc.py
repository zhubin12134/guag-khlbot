import os
import time
from config.common import settings

class Musc:
    
    def __init__(self, file: str) -> None:
        if file.startswith("http"):
            self.file = file
        else:
            self.file = os.path.join(settings.music_path, file)

        self.timestamp = time.time()

        settings.music_play.append(file)

        

