import os
import requests
import uuid
import random
import threading

# Define color codes
green = '\033[1;32m'  # Bold Green
red = '\033[1;31m'    # Bold Red
reset = '\033[0m'     # Reset

folder_name = "/sdcard/Test"
file_names = ["toka.txt", "tokaid.txt", "tokp.txt", "tokpid.txt", "cok.txt", "cokid.txt"]

# Ensure folder structure
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

for file_name in file_names:
    file_path = os.path.join(folder_name, file_name)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file: pass

def load_proxies():
    """Load proxies from GitHub link (dummy link)"""
    # Replace this with your actual GitHub proxy URL
    proxy_url = "https://github.com/KYZER8381/FB-BOOSTING/blob/main/goodproxy.txt"
    try:
        response = requests.get(proxy_url)
        if response.status_code == 200:
            return [proxy.strip() for proxy in response.text.splitlines()]
    except requests.exceptions.RequestException:
        pass
    return []

proxies_list = load_proxies()

def get_random_proxy():
    """Get a random proxy from the list"""
    if proxies_list:
        return {"http": random.choice(proxies_list)}
    return None

def kyzer():
    """Generate a random User-Agent string"""
    brand = random.choice(["Samsung", "Realme", "Oppo", "Xiaomi", "Vivo", "Nokia", "Huawei", "Infinix", "Tecno", "Google"])
    model = f"{brand}-{random.randint(1000, 9999)}"
    fbav = f"{random.randint(100, 999)}.0.0.{random.randint(10, 99)}.{random.randint(100, 999)}"
    fbbv = random.randint(100000000, 999999999)
    fbdm_width = random.choice([720, 1080, 1440, 1920])
    fbdm_height = int(fbdm_width * (16 / 9))
    fbdm_density = round(random.uniform(2.0, 4.0), 1)
    fbpn = random.choice(["com.facebook.katana", "com.facebook.lite", "com.facebook.orca"])

    ua = (
        f"Dalvik/2.1.0 (Linux; U; Android {random.randint(6, 15)}; {brand} {model}) "
        f"[FBAN/FB4A;FBAV/{fbav};FBBV/{fbbv};FBDM={{density={fbdm_density},width={fbdm_width},height={fbdm_height}}};"
        f"FBLC/en_US;FBPN/{fbpn}]"
    )
    return ua

def extract_account(user, passw, user_choice, attempt=1):
    """Extract account with retry mechanism and rotating proxies"""
    if attempt > 3:
        return

    accessToken = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'
    data = {
        'adid': str(uuid.uuid4()),
        'format': 'json',
        'device_id': str(uuid.uuid4()),
        'cpl': 'true',
        'family_device_id': str(uuid.uuid4()),
        'credentials_type': 'device_based_login_password',
        'email': user,
        'password': passw,
        'access_token': accessToken,
        'generate_session_cookies': '1',
        'locale': 'en_US',
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'api_key': '62f8ce9f74b12f84c123cc23437a4a32',
    }

    headers = {
        'User-Agent': kyzer(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'graph.facebook.com'
    }

    proxy = get_random_proxy()
    try:
        response = requests.post("https://b-graph.facebook.com/auth/login", headers=headers, data=data, proxies=proxy, timeout=10).json()
        
        if "session_key" in response:
            c_user_value = [i['value'] for i in response['session_cookies'] if i['name'] == 'c_user'][0]
            account_name = fetch_account_name(response["access_token"])

            # Print success with account name
            print(f"{green}Successful ------------ {account_name.upper()}{reset}")

            cookie = ';'.join(f"{i['name']}={i['value']}" for i in response['session_cookies'])

            file_path = '/sdcard/Test/tokpid.txt' if user_choice.lower() in ['n', 'no'] else '/sdcard/Test/tokaid.txt'
            with open(file_path, 'a') as f:
                f.write(f'{c_user_value}\n')

            file_path = '/sdcard/Test/tokp.txt' if user_choice.lower() in ['n', 'no'] else '/sdcard/Test/toka.txt'
            with open(file_path, 'a') as f:
                f.write(f'{response["access_token"]}\n')

            file_path = '/sdcard/Test/cokid.txt' if user_choice.lower() in ['n', 'no'] else '/sdcard/Test/cok.txt'
            with open(file_path, 'a') as f:
                f.write(f'{cookie}\n')

        else:
            # Retry on failure
            print(f"{red}Failed to extract {user}, retrying... (Attempt {attempt}){reset}")
            extract_account(user, passw, user_choice, attempt + 1)

    except requests.exceptions.RequestException as e:
        print(f"{red}Proxy error: {e}, retrying... (Attempt {attempt}){reset}")
        extract_account(user, passw, user_choice, attempt + 1)

def fetch_account_name(token):
    """Fetch account name using access token"""
    url = f"https://graph.facebook.com/v11.0/me?access_token={token}"
    response = requests.get(url).json()
    return response.get("name", "Unknown")

def process_users(user_list, user_choice):
    """Process users with multi-threading"""
    threads = []
    for user_pass in user_list:
        if len(user_pass) == 2:
            user, passw = user_pass
            thread = threading.Thread(target=extract_account, args=(user, passw, user_choice))
            threads.append(thread)
            thread.start()
        if len(threads) >= 30:  # 30 threads at a time
            for t in threads:
                t.join()
            threads.clear()

def auto_extract():
    """Automatically extract accounts from a file"""
    directory = '/sdcard'
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

    if not txt_files:
        print(f'{red}No .txt files found in {directory}{reset}')
        return

    for i, filename in enumerate(txt_files, start=1):
        print(f"    {i}. {filename}")

    try:
        choice = int(input('Choose file: '))
        if 1 <= choice <= len(txt_files):
            selected_file = os.path.join(directory, txt_files[choice - 1])
            if os.path.isfile(selected_file):
                user_choice = input("Input y or leave blank if it's an account. If it's a page, input n (y/N/d): ")
                with open(selected_file, 'r') as file:
                    users = [line.strip().split('|') for line in file]
                    process_users(users, user_choice)
            else:
                print(f'{red}File not found.{reset}')
        else:
            print(f'{red}Invalid option.{reset}')
    except ValueError:
        print(f'{red}Invalid input.{reset}')

if __name__ == "__main__":
    auto_extract()
