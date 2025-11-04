import requests
import concurrent.futures
from rich import print

def get_ids_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def get_profile_id(profile_link, access_token):
    if profile_link.isdigit():
        return profile_link  # Already a numeric ID

    url = f'https://graph.facebook.com/v19.0/{profile_link}'
    params = {'access_token': access_token, 'fields': 'id'}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get('id', 'Unknown ID')
    return 'Unknown ID'

def get_profile_username(profile_id, access_token):
    url = f'https://graph.facebook.com/v19.0/{profile_id}'
    params = {'access_token': access_token, 'fields': 'name'}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get('name', 'Unknown Profile')
    return 'Unknown Profile'

def follow_facebook_profile():
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')

    profile_link = input('Enter the Facebook profile link: ')
    profile_id = get_profile_id(profile_link.split('/')[-1], access_tokens[0])
    num_followers = int(input('How many followers do you want to add? '))
    
    def follow_profile(profile_id, access_token):
        try:
            url = f'https://graph.facebook.com/v19.0/{profile_id}/subscribers'
            params = {'access_token': access_token}
            response = requests.post(url, params=params)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    follow_count = 0

    def handle_following(access_token, i):
        nonlocal follow_count
        if follow_count >= num_followers:
            return  # Stop once the required followers are added

        profile_name = get_profile_username(profile_id, access_token)
        
        if follow_profile(profile_id, access_token):
            print(f"[bold green]Success: Followed the profile '{profile_name}' with token ID {i + 1}[/bold green]")
            follow_count += 1
        else:
            print(f"[bold red]Failed: Could not follow the profile '{profile_name}' with token ID {i + 1}[/bold red]")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i, access_token in enumerate(access_tokens):
            if follow_count >= num_followers:
                break
            futures.append(executor.submit(handle_following, access_token, i))
        concurrent.futures.wait(futures)

    print(f"Successfully followed {follow_count} profiles out of {num_followers} requested.")

def remove_facebook_follower():
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')

    profile_link = input('Enter the Facebook profile link to remove followers from: ')
    profile_id = get_profile_id(profile_link.split('/')[-1], access_tokens[0])
    num_to_remove = int(input('How many followers do you want to remove? '))

    def remove_follower(profile_id, access_token):
        try:
            url = f'https://graph.facebook.com/v19.0/{profile_id}/subscribers'
            params = {'access_token': access_token}
            response = requests.delete(url, params=params)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    remove_count = 0

    def handle_removing(access_token, i):
        nonlocal remove_count
        if remove_count >= num_to_remove:
            return  # Stop once the required followers are removed

        profile_name = get_profile_username(profile_id, access_token)
        
        if remove_follower(profile_id, access_token):
            print(f"[bold green]Success: Removed a follower from profile '{profile_name}' with token ID {i + 1}[/bold green]")
            remove_count += 1
        else:
            print(f"[bold red]Failed: Could not remove a follower from profile '{profile_name}' with token ID {i + 1}[/bold red]")

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = []
        for i, access_token in enumerate(access_tokens):
            if remove_count >= num_to_remove:
                break
            futures.append(executor.submit(handle_removing, access_token, i))
        concurrent.futures.wait(futures)

    print(f"Successfully removed {remove_count} followers out of {num_to_remove} requested.")

def main_menu():
    while True:
        print("Menu:")
        print("1. Follow a Facebook Profile/Page")
        print("2. Remove followers from a Facebook Profile/Page")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            follow_facebook_profile()
        elif choice == '2':
            remove_facebook_follower()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

# Start the menu
main_menu()
