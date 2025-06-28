import os
from pathlib import Path
import sys

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)

load_dotenv()


class Setting:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    PLATFORM: str = os.environ.get("PLATFORM", "openai")
    LLM_MODEL: str = os.environ.get("LLM_MODEL", "gpt-4.1")
    
    __log_dir = 'logs'
    @property
    def LOG_DIR(self):
        _log_path = os.path.join(BASE_DIR, self.__log_dir)
        os.makedirs(_log_path, exist_ok=True)
        return _log_path
        
    
setting = Setting()