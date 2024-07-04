# S124-Info-Stealers

**S124-Info-Stealers** is a Python-based project designed to extract and manage sensitive information from various local sources, primarily targeting browser data. This project facilitates the collection of browser passwords, cookies, Wi-Fi passwords, system details, and more. It also integrates features to send collected data to external endpoints like Discord and Telegram.

## Table of Contents

- [Overview](#overview)
- [Use Cases](#use-cases)
- [File Structure](#file-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Overview

**S124-Info-Stealers** is designed to help developers understand and manage sensitive local data by providing scripts that:
- Extract passwords and cookies from Chrome.
- Gather Wi-Fi passwords from the system.
- Collect system and user details.
- Send collected data to Discord and Telegram via configured webhooks.

### Features

- **Chrome Data Extraction**: Extracts passwords and cookies from Google Chrome.
- **Wi-Fi Password Retrieval**: Retrieves saved Wi-Fi passwords from the system.
- **Data Transmission**: Sends collected data to configured Discord and Telegram webhooks.
- **Cleanup**: Deletes temporary files after data transmission to maintain privacy.

## Use Cases

- **Security Audits**: For ethical hackers or system administrators to test the security and data exposure of local systems.
- **Data Recovery**: Assists in recovering lost passwords and cookies for legitimate purposes.
- **Educational Purposes**: Helps developers understand how local data can be accessed and the importance of securing sensitive information.

> **Warning:** This tool is intended for educational purposes and ethical use only. Unauthorized use of this tool on systems you do not own or have explicit permission to test is illegal and unethical.

## File Structure

```
S124-Info-Stealers/
│
├── env/
│   └── .env                  # Environment variables for configuration
│
├── plugins/
│   ├── steal_chrome.py       # Extracts Chrome passwords and cookies
│   ├── steal_discord.py      # Collects Discord token
│   ├── steal_user.py         # Gathers user details
│   ├── wifi_passwords.py     # Retrieves Wi-Fi passwords
│
├── main.py                   # Main script orchestrating the workflow
│
└── README.md                 # This readme file
```

### File Descriptions

- **`env/.env`**: Contains environment variables such as webhooks and tokens for Discord and Telegram.
- **`plugins/steal_chrome.py`**: Script for extracting passwords and cookies from Google Chrome.
- **`plugins/steal_discord.py`**: Script for collecting Discord tokens.
- **`plugins/steal_user.py`**: Script for gathering user and system details.
- **`plugins/wifi_passwords.py`**: Script for retrieving saved Wi-Fi passwords.
- **`main.py`**: The main script that executes the functions from the plugins.

## Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)

### Setup

1. **Clone the repository**:
   ```sh
   git clone https://github.com/WannaCry016/S124-Info-Stealers.git
   cd S124-Info-Stealers
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure the environment variables**:
   - Edit `env/.env` with your Discord and Telegram credentials.

## Usage

Run the main script using the following command:

```sh
python main.py
```

This will execute all the extraction functions and handle data transmission according to your configuration.

## Configuration

Edit the `env/.env` file to set up your Discord and Telegram webhooks:

```ini
DISCORD_WEBHOOK_URL=<Your_Discord_Webhook_URL>
TELEGRAM_BOT_TOKEN=<Your_Telegram_Bot_Token>
TELEGRAM_CHAT_ID=<Your_Telegram_Chat_ID>
```

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
