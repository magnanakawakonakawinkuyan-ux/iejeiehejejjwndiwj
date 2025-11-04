import requests

# File paths
tokens_file = "/sdcard/Test/toka.txt"
ids_file = "/sdcard/Test/tokaid.txt"

# Function to enable profile guard
def enable_profile_guard(token, user_id):
    url = "https://graph.facebook.com/graphql"
    headers = {
        "Authorization": f"OAuth {token}",
        "User-Agent": "Mozilla/5.0"
    }
    payload = {
        "variables": '{"0":{"is_shielded":true,"actor_id":"' + user_id + '","client_mutation_id":"1"}}',
        "doc_id": "1477043292367183"
    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200 and "errors" not in response.text:
        print(f"✅ Profile Guard Enabled: {user_id}")
    else:
        print(f"❌ Failed: {user_id} → {response.text}")

# Function to disable profile guard
def disable_profile_guard(token, user_id):
    url = "https://graph.facebook.com/graphql"
    headers = {
        "Authorization": f"OAuth {token}",
        "User-Agent": "Mozilla/5.0"
    }
    payload = {
        "variables": '{"0":{"is_shielded":false,"actor_id":"' + user_id + '","client_mutation_id":"1"}}',
        "doc_id": "1477043292367183"
    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200 and "errors" not in response.text:
        print(f"✅ Profile Guard Disabled: {user_id}")
    else:
        print(f"❌ Failed: {user_id} → {response.text}")

# Function to process tokens and user IDs
def process_guard(action):
    try:
        with open(tokens_file, "r") as tf, open(ids_file, "r") as idf:
            tokens = tf.read().strip().split("\n")
            user_ids = idf.read().strip().split("\n")

            # Check if both files have equal lines
            if len(tokens) != len(user_ids):
                print("❌ Error: Token and ID count mismatch!")
            else:
                for token, user_id in zip(tokens, user_ids):
                    if action == "enable":
                        enable_profile_guard(token.strip(), user_id.strip())
                    elif action == "disable":
                        disable_profile_guard(token.strip(), user_id.strip())

    except FileNotFoundError:
        print("❌ Error: One or both files not found!")

# Menu
while True:
    print("\n[ MENU ]")
    print("1️⃣ Enable Profile Guard")
    print("2️⃣ Disable Profile Guard")
    print("0️⃣ Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        process_guard("enable")
    elif choice == "2":
        process_guard("disable")
    elif choice == "0":
        print("👋 Exiting...")
        break
    else:
        print("❌ Invalid choice! Please enter 1, 2, or 0.")
