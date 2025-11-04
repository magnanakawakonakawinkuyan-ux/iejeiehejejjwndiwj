import requests

# ANSI escape codes for color formatting
COLORS = {
    'bold_red': "\033[1;31m",
    'bold_green': "\033[1;32m",
    'bold_yellow': "\033[1;33m",
    'bold_cyan': "\033[1;36m",
    'reset': "\033[0m"
}

def get_ids_tokens(file_path):
    """Reads and returns lines from the given file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def save_valid_data(file_path, valid_data):
    """Saves valid data back to the file."""
    with open(file_path, 'w') as file:
        for line in valid_data:
            file.write(line + '\n')

def check_token_validity(token):
    """
    Checks if the token is valid by making a request to the Graph API.
    Returns True if valid, False otherwise, with an optional error reason.
    """
    url = "https://graph.facebook.com/me"
    params = {'access_token': token, 'fields': 'id'}

    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            print(f"{COLORS['bold_green']}Valid token: {token}{COLORS['reset']}")
            return True, None
        else:
            error_message = response.json().get('error', {}).get('message', 'Unknown error')
            print(f"{COLORS['bold_red']}Invalid token: {token}{COLORS['reset']} | "
                  f"{COLORS['bold_cyan']}Reason: {error_message}{COLORS['reset']}")
            return False, error_message
    except requests.RequestException as e:
        print(f"{COLORS['bold_red']}Error checking token: {token}{COLORS['reset']} | "
              f"{COLORS['bold_cyan']}Reason: {str(e)}{COLORS['reset']}")
        return False, str(e)

def validate_and_remove_invalid(ids_file, tokens_file):
    """Validates tokens and removes invalid ones along with their associated IDs."""
    ids = get_ids_tokens(ids_file)
    tokens = get_ids_tokens(tokens_file)

    valid_ids = []
    valid_tokens = []

    for token, actor_id in zip(tokens, ids):
        print(f"{COLORS['bold_yellow']}Checking token for ID: {actor_id}{COLORS['reset']}")
        is_valid, reason = check_token_validity(token)

        if is_valid:
            # Keep valid tokens and their associated IDs
            valid_ids.append(actor_id)
            valid_tokens.append(token)
        else:
            # Print and remove invalid tokens and their IDs
            print(f"{COLORS['bold_red']}Removing invalid token and ID: {actor_id} - {token}{COLORS['reset']}")

    # Save valid data back to the files
    save_valid_data(ids_file, valid_ids)
    save_valid_data(tokens_file, valid_tokens)

# File paths
ids_file_path = '/sdcard/Test/tokaid.txt'
tokens_file_path = '/sdcard/Test/toka.txt'

# Run the validation and cleanup process
validate_and_remove_invalid(ids_file_path, tokens_file_path)