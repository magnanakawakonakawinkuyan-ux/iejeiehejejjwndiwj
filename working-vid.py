import requests
import re
import threading

# Define color codes for console output
success_color = "\033[1;32m"  # Bold green
error_color = "\033[1;31m"    # Bold red
reset_color = "\033[0m"       # Reset color

def Video_Extractid(url):
    # Extract media ID from the URL
    match = re.search(r'/(videos|photos)/(\d+)', url)
    return match.group(2) if match else None

def load_data(filepath):
    # Load access tokens from a file
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        return []

def has_reacted(media_id, access_token):
    # Dummy implementation; replace with actual logic to check if the user has reacted
    return False

def react_to_media(media_id, access_token, reaction_type, reactions_count, reactions_limit, count_lock):
    user_id = access_token[:10]  # Using a portion of the token as a placeholder for user ID
    try:
        if access_token.startswith("EA") or access_token.startswith("EAA"):
            if not has_reacted(media_id, access_token):
                url = f'https://graph.facebook.com/v18.0/{media_id}/reactions'
                params = {'access_token': access_token, 'type': reaction_type}
                response = requests.post(url, params=params)

                with count_lock:
                    if response.status_code == 200:
                        reactions_count[0] += 1
                        print(f"{success_color}[SUCCESS] User '{user_id}' reacted successfully on media ID '{media_id}'.{reset_color}")
                    else:
                        print(f"{error_color}[FAILED] User '{user_id}' failed to react on media ID '{media_id}'.{reset_color}")

                if reactions_count[0] >= reactions_limit:
                    return
    except requests.exceptions.RequestException as error:
        print(f"{error_color}[EXCEPTION] User '{user_id}' failed due to a request error on media ID '{media_id}': {error}{reset_color}")
    except Exception as e:
        print(f"{error_color}[ERROR] User '{user_id}' encountered an unexpected error on media ID '{media_id}': {e}{reset_color}")

def perform_reaction_media(url, reaction_type, num_reactions):
    media_id = Video_Extractid(url)
    if not media_id:
        print("[ERROR] Invalid URL or unable to extract media ID.")
        return

    access_tokens = load_data('/sdcard/Test/toka.txt')
    reactions_count = [0]  # Use a list to store the count for mutability across threads
    count_lock = threading.Lock()

    threads = []
    for access_token in access_tokens:
        if reactions_count[0] >= num_reactions:
            break
        t = threading.Thread(target=react_to_media, args=(media_id, access_token, reaction_type, reactions_count, num_reactions, count_lock))
        threads.append(t)
        t.start()
        if len(threads) >= 10:  # Limit to 10 threads
            for t in threads:
                t.join()
            threads = []  # Reset the threads list after joining

    # Join any remaining threads
    for t in threads:
        t.join()

    print(f"Total successful reactions sent: {reactions_count[0]}")

# Example usage
if __name__ == "__main__":
    url = input("Enter the media URL: ")
    reaction_type = input("Enter the reaction type (like, love, wow, etc.): ")
    num_reactions = int(input("Enter the number of reactions to perform: "))
    
    perform_reaction_media(url, reaction_type, num_reactions)
