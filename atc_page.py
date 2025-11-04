
import requests
import time
import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class reg_pro5():
    def __init__(self, cookies, name) -> None:
        self.cookies = cookies
        self.name = name  # Store the name in an instance variable
        self.id_acc = self.cookies.split('c_user=')[1].split(';')[0]
        headers = self.get_headers()
        
        url_profile = requests.get('https://www.facebook.com/me', headers=headers).url
        profile = requests.get(url_profile, headers=headers).text
        try:
            self.fb_dtsg = profile.split('{"name":"fb_dtsg","value":"')[1].split('"},')[0]
        except:
            self.fb_dtsg = profile.split(',"f":"')[1].split('","l":null}')[0]
    
    def get_headers(self):
        """Randomize some header fields to simulate real behavior."""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36',
            # Add more user agents here
        ]
        
        headers = {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': self.cookies,
            'sec-ch-prefers-color-scheme': 'light',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': random.choice(user_agents),
            'viewport-width': str(random.randint(800, 1920)),
        }
        return headers

    def random_delay(self, min_time=2, max_time=5):
        """Random delay to mimic human-like behavior."""
        time.sleep(random.uniform(min_time, max_time))

    def create_profile(self):
        headers = self.get_headers()
        self.random_delay()  # Add a random delay

        data = {
            'av': self.id_acc,
            '__user': self.id_acc,
            '__a': '1',
            '__dyn': '7AzHxq1mxu1syUbFuC0BVU98nwgU29zEdEc8co5S3O2S7o11Ue8hw6vwb-q7oc81xoswIwuo886C11xmfz81sbzoaEnxO0Bo7O2l2Utwwwi831wiEjwZwlo5qfK6E7e58jwGzE8FU5e7oqBwJK2W5olwuEjUlDw-wUws9ovUaU3qxWm2Sq2-azo2NwkQ0z8c84K2e3u362-2B0oobo',
            '__csr': 'gP4ZAN2d-hbbRmLObkZO8LvRcXWVvth9d9GGXKSiLCqqr9qEzGTozAXiCgyBhbHrRG8VkQm8GFAfy94bJ7xeufz8jK8yGVVEgx-7oiwxypqCwgF88rzKV8y2O4ocUak4UpDxu3x1K4opAUrwGx63J0Lw-wa90eG18wkE7y14w4hw6Bw2-o069W00CSE0PW06aU02Z3wjU6i0btw3TE1wE5u',
            '__req': 't',
            '__hs': '19296.HYP:comet_pkg.2.1.0.2.1',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1006496476',
            '__s': '1gapab:y4xv3f:2hb4os',
            '__hsi': '7160573037096492689',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': '25404',
            'lsd': 'ZM7FAk6cuRcUp3imwqvHTY',
            '__aaid': '800444344545377',
            '__spin_r': '1006496476',
            '__spin_b': 'trunk',
            '__spin_t': '1667200829',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'AdditionalProfilePlusCreationMutation',
            'variables': '{"input":{"bio":"","categories":["181475575221097"],"creation_source":"comet","name":"'+self.name+'","page_referrer":"launch_point","actor_id":"'+self.id_acc+'","client_mutation_id":"1"}}',
            'server_timestamps': 'true',
            'doc_id': '5903223909690825',  # You may need to find the correct doc_id for profile creation
        }

        self.random_delay()  # Add another random delay
        response = requests.post('https://www.facebook.com/api/graphql/', headers=headers, data=data).json()

        try:
            profile_id = response['data']['additional_profile_plus_create']['additional_profile']['id']
            print(Fore.GREEN + "Successfully Created Profile")
            print(Fore.GREEN + f"Profile Name: {self.name}")
            print(Fore.GREEN + f"Profile ID: {profile_id}")
        except:
            print(Fore.RED + '「Failed 」 to create profile.')

# Menu function
def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Create a new Facebook profile")
        print("2. Exit")
        choice = input("Enter your choice (1/2): ")

        if choice == '1':
            cookies = input(Fore.GREEN + "Enter your Facebook cookies: ")
            name = input("Enter the name for the new profile: ")
            profile_creator = reg_pro5(cookies, name)
            profile_creator.create_profile()
        elif choice == '2':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
