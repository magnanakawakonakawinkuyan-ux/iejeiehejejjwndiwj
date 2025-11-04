import requests
import re

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

# Function to perform auto comments on reels
def auto_comment_on_reels(reels_link, comments, num_comments, tokens):
    reel_id = extract_reel_id(reels_link)
    if not reel_id:
        return  # Exit if the reel ID is invalid

    url = f'https://graph.facebook.com/v13.0/{reel_id}/comments'

    total_successful_comments = 0
    total_failed_comments = 0
    token_index = 0  # Start with the first token
    comment_index = 0  # Start with the first comment

    # Calculate how many comments are possible based on available tokens
    available_tokens = len(tokens)
    if num_comments > available_tokens * len(comments):
        print(f"Requested {num_comments} comments, but only {available_tokens * len(comments)} comments are possible with available tokens.")
        num_comments = available_tokens * len(comments)  # Limit to possible comments

    # Loop until the desired number of successful comments is reached
    while total_successful_comments < num_comments:
        # Cycle through each token
        for _ in range(available_tokens):  
            if total_successful_comments >= num_comments:
                break  # Stop if the target is already reached

            current_token = tokens[token_index % available_tokens]  # Use current token
            current_comment = comments[comment_index % len(comments)]  # Use current comment

            if current_token.startswith("EA") or current_token.startswith("EAA"):
                params = {'access_token': current_token, 'message': current_comment}
                try:
                    response = requests.post(url, params=params)
                    if response.status_code == 200:
                        total_successful_comments += 1
                        print(f"Comment: '{current_comment}' then successful token {current_token[:10]}... ({total_successful_comments}/{num_comments})")
                        # Move to the next comment after a successful comment
                        comment_index += 1
                    else:
                        total_failed_comments += 1
                        error_message = response.json().get("error", {}).get("message", "Unknown error")
                        print(f"Failed comment: '{current_comment}' with token {current_token[:10]}... Status Code: {response.status_code} - Error: {error_message}")
                except requests.exceptions.RequestException as e:
                    print(f"Request failed with token {current_token[:10]}... Error: {e}")
                    total_failed_comments += 1  # Increment the failed comment count
            else:
                print(f"Invalid token format: {current_token[:10]}...")

            # Move to the next token
            token_index += 1

        # Reset token_index if we have used all tokens
        if token_index >= available_tokens:
            token_index = 0

    # Summary of comments
    print(f'Total successful comments: {total_successful_comments}')
    print(f'Total failed comments: {total_failed_comments}')

# Main Menu Function
def main_menu():
    print("=== Facebook Auto-Commenter ===")
    print("1. Auto Comment with the Same Comment")
    print("2. Auto Comment with Different Comments")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == '1':
        reels_link = input("Enter the Reel link: ")
        comment = input("Enter the Comment: ")
        num_comments = int(input("Enter the Number of Comments to Send: "))

        # Load tokens from the specified file
        tokens = get_ids_tokens('/sdcard/Test/toka.txt')

        if len(tokens) == 0:
            print("No tokens found. Please add tokens to the file.")
            return

        # Call the function to auto-comment
        auto_comment_on_reels(reels_link, [comment], num_comments, tokens)

    elif choice == '2':
        reels_link = input("Enter the Reel link: ")
        num_comments = int(input("Enter the Number of Comments to Send: "))
        
        # Load comments from the user
        comments = []
        for i in range(num_comments):
            comment = input(f"Enter Comment {i + 1}: ")
            comments.append(comment)

        # Load tokens from the specified file
        tokens = get_ids_tokens('/sdcard/Test/toka.txt')

        if len(tokens) == 0:
            print("No tokens found. Please add tokens to the file.")
            return

        # Call the function to auto-comment with different comments
        auto_comment_on_reels(reels_link, comments, num_comments, tokens)

    elif choice == '3':
        print("Exiting the program.")
        exit()

    else:
        print("Invalid choice! Please select a valid option.")
        main_menu()  # Recursively call the menu if an invalid choice is made

# Run the main menu
if __name__ == "__main__":
    main_menu()