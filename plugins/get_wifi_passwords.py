import subprocess

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

if __name__ == "__main__":
    wifi_profiles_and_passwords()
