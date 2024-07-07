from dotenv import set_key, load_dotenv
from pathlib import Path
import os

class EnvManager:
    def __init__(self, dotenv_folder):
        self.dotenv_folder = Path(dotenv_folder)
        self.dotenv_file = self.dotenv_folder / '.env'
        self.dotenv_file.touch(exist_ok=True)  # Ensure the .env file exists
        load_dotenv(dotenv_path=self.dotenv_file, override=True)

    def set_env_variable(self, key, value):
        set_key(str(self.dotenv_file), key, value)
        os.environ[key] = value  # Update os.environ for immediate use
        load_dotenv(dotenv_path=self.dotenv_file, override=True)  # Reload dotenv file

    def get_env_variable(self, key):
        return os.getenv(key)

# Instantiate EnvManager globally for use
dotenv_folder = 'env'
env_manager = EnvManager(dotenv_folder)
