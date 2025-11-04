import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import threading

# Lock to ensure only one thread updates the successful reactions at a time
lock = threading.Lock()

# Function to load ids and tokens from a file
def get_ids_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to extract the Reel ID from a given link
def extract_reel_id(reels_link):
    match = re.search(r'reel/(\d+)', reels_link)
    if match:
        return match.group(1)
    else:
        print("Invalid reel link format!")
        return None

# Function to perform reactions
def auto_react_to_reels_fast(reels_link, reaction_type, num_reactions, tokens):
    reel_id = extract_reel_id(reels_link)
    if not reel_id:
        return  # Exit if the reel ID is invalid

    url = f'https://graph.facebook.com/v13.0/{reel_id}/reactions'

    # Global counter for successful reactions
    total_successful_reactions = 0

    def react_with_token(access_token):
        nonlocal total_successful_reactions  # Allow modification of the outer variable
        with lock:  # Ensure accurate count with threading
            if total_successful_reactions >= num_reactions:
                return 0  # Stop if the target is already reached

        if access_token.startswith("EA") or access_token.startswith("EAA"):
            params = {'access_token': access_token, 'type': reaction_type}
            try:
                response = requests.post(url, params=params)
                if response.status_code == 200:
                    with lock:  # Lock before modifying shared variable
                        if total_successful_reactions < num_reactions:
                            total_successful_reactions += 1
                            print(f"Successful reaction with token {access_token[:10]}... ({total_successful_reactions}/{num_reactions})")
                    return 1  # Return 1 for successful reaction
                else:
                    print(f"Failed reaction with token {access_token[:10]}... Status Code: {response.status_code}")
                    return 0  # Return 0 for failed reaction
            except requests.exceptions.RequestException as e:
                print(f"Request failed with token {access_token[:10]}... Error: {e}")
                return 0  # Return 0 for failed reaction
        return 0  # Return 0 for invalid token format

    # Calculate how many reactions are possible based on available tokens
    available_tokens = len(tokens)
    if num_reactions > available_tokens:
        print(f"Requested {num_reactions} reactions, but only {available_tokens} tokens are available.")
        num_reactions = available_tokens  # Limit to available tokens

    # Using ThreadPoolExecutor for parallel processing
    total_failed_reactions = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_token = {executor.submit(react_with_token, token): token for token in tokens}

        for future in as_completed(future_to_token):
            with lock:  # Check after task completion
                if total_successful_reactions >= num_reactions:
                    break  # Stop processing if the target number is reached
            successful_reaction = future.result()
            if not successful_reaction:
                total_failed_reactions += 1

    # Summary of reactions
    print(f'Total successful reactions: {total_successful_reactions}')
    print(f'Total failed reactions: {total_failed_reactions}')


# Main Menu Function
def main_menu():
    print("=== Facebook Auto-Reactor ===")
    print("1. Start Reacting to Reels")
    print("2. Exit")

    choice = input("Choose an option: ")

    if choice == '1':
        reels_link = input("Enter the Reel link: ")
        reaction_type = input("Enter the Reaction Type (e.g., LIKE, LOVE): ")
        num_reactions = int(input("Enter the Number of Reactions to Send: "))

        # Load tokens from the specified files
        tokens = get_ids_tokens('/sdcard/Test/toka.txt')

        if len(tokens) == 0:
            print("No tokens found. Please add tokens to the file.")
            return

        # Call the function to auto-react
        auto_react_to_reels_fast(reels_link, reaction_type, num_reactions, tokens)

    elif choice == '2':
        print("Exiting the program.")
        exit()

    else:
        print("Invalid choice! Please select a valid option.")
        main_menu()  # Recursively call the menu if an invalid choice is made

# Run the main menu
if __name__ == "__main__":
    main_menu()
