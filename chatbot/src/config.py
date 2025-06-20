import os
from pathlib import Path
import sys

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(BASE_DIR)

load_dotenv()


class Setting:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")
    
    __log_dir = 'logs'
    @property
    def LOG_DIR(self):
        _log_path = os.path.join(BASE_DIR, self.__log_dir)
        os.makedirs(_log_path, exist_ok=True)
        return _log_path
        
    
setting = Setting()