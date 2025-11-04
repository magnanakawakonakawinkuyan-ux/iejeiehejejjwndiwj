import requests
from datetime import datetime

def get_ids_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def linktradio(post_link):
    try:
        if 'photo.php?fbid=' in post_link:
            post_id = post_link.split('fbid=')[1].split('&')[0]
        elif '/posts/' in post_link:
            post_id = post_link.split('/posts/')[1].split('/')[0]
        else:
            print("Invalid post link.")
            return None
        return post_id
    except IndexError:
        print("Could not extract post ID.")
        return None

def get_user_name():
    return "User"

def comment_on_facebook_post():
    user_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')
    
    comment_option = input('Choose comment option:\n1. Same comments\n2. Different comments\nEnter option (1 or 2): ')
    num_comments = int(input('Enter the number of comments to make: '))
    post_link = input('Enter the Facebook post link: ')
    post_id = linktradio(post_link)

    if post_id is None:
        print("Could not extract post ID. Exiting.")
        return

    comment_texts = []
    if comment_option == '1':
        comment_text = input('Enter the comment text (or leave blank for auto comment): ')
        if not comment_text:
            current_time = datetime.now().strftime("%I:%M %p")
            current_date = datetime.now().strftime("%Y-%m-%d")
            user_name = get_user_name()
            comment_text = f'Time:「{current_time}」「{current_date}」\n-「Auto comment by {user_name}」'
        comment_texts = [comment_text] * num_comments
    elif comment_option == '2':
        for i in range(num_comments):
            comment_text = input(f'Enter comment {i + 1}: ')
            if not comment_text:
                current_time = datetime.now().strftime("%I:%M %p")
                current_date = datetime.now().strftime("%Y-%m-%d")
                user_name = get_user_name()
                comment_text = f'Time:「{current_time}」「{current_date}」\n-「Auto comment by {user_name}」'
            comment_texts.append(comment_text)

    def has_commented(post_id, access_token, user_id):
        try:
            url = f'https://graph.facebook.com/v18.0/{user_id}_{post_id}/comments'
            params = {'access_token': access_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            comments = response.json().get('data', [])
            
            for comment in comments:
                if comment.get('from', {}).get('id') == user_id:
                    return True
        except requests.exceptions.RequestException:
            return False

    successful_comments = 0
    current_comment_index = 0
    user_count = len(user_ids)

    while successful_comments < num_comments:
        user_id = user_ids[current_comment_index % user_count]
        access_token = access_tokens[current_comment_index % user_count]
        comment_text = comment_texts[current_comment_index % len(comment_texts)]
        
        try:
            if not has_commented(post_id, access_token, user_id):
                url = f'https://graph.facebook.com/v19.0/{user_id}_{post_id}/comments'
                params = {'access_token': access_token, 'message': comment_text}
                response = requests.post(url, params=params)
                
                if response.status_code == 200:
                    print(f"Success: Commented on {post_id} with user ID {user_id}.")
                    successful_comments += 1
                else:
                    print(f"Failed to comment. User ID: {user_id}, Post ID: {post_id}")
            else:
                print(f"User {user_id} has already commented on this post.")
        except requests.exceptions.RequestException:
            print(f"Failed to comment. User ID: {user_id}, Post ID: {post_id}")
        
        current_comment_index += 1

    print(f"Total successful comments: {successful_comments}")

comment_on_facebook_post()
