from dotenv import set_key, load_dotenv
from pathlib import Path
import os

class EnvManager:
    def __init__(self, dotenv_path):
        self.dotenv_path = dotenv_path
        load_dotenv(dotenv_path=self.dotenv_path)

    def set_env_variable(self, key, value):
        set_key(self.dotenv_path, key, value)
        os.environ[key] = value  # Directly set in os.environ for immediate use

    def get_env_variable(self, key):
        return os.getenv(key)

# Instantiate EnvManager globally for use
dotenv_path = Path('env/.env')
env_manager = EnvManager(dotenv_path)
