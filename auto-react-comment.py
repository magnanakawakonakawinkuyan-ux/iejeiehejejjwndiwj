import requests, json, time, uuid, base64, re
from concurrent.futures import ThreadPoolExecutor

r = "\033[1;31m"  # Bold Red
g = "\033[1;32m"  # Bold Green
reset = "\033[0m"  # Reset color

def AutoReact():
    def Reaction(actor_id: str, comment_id: str, react: str, token: str):
        rui = requests.Session()
        feedback_id = str(base64.b64encode(('feedback:{}'.format(comment_id)).encode('utf-8')).decode('utf-8'))
        var = {
            "input": {
                "feedback_referrer": "native_newsfeed",
                "tracking": [None],
                "feedback_id": feedback_id,
                "client_mutation_id": str(uuid.uuid4()),
                "nectar_module": "newsfeed_ufi",
                "feedback_source": "native_newsfeed",
                "feedback_reaction_id": react,
                "actor_id": actor_id,
                "action_timestamp": str(time.time())[:10]
            }
        }
        data = {
            'access_token': token,
            'method': 'post',
            'pretty': False,
            'format': 'json',
            'server_timestamps': True,
            'locale': 'id_ID',
            'fb_api_req_friendly_name': 'ViewerReactionsMutation',
            'fb_api_caller_class': 'graphservice',
            'client_doc_id': '2857784093518205785115255697',
            'variables': json.dumps(var),
            'fb_api_analytics_tags': ["GraphServices"],
            'client_trace_id': str(uuid.uuid4())
        }

        pos = rui.post('https://graph.facebook.com/graphql', data=data).json()
        try:
            if react == '0':
                print(f"{g}「Success」» Removed reaction from {actor_id} on {comment_id}{reset}")
                return True
            elif react in str(pos):
                print(f"{g}「Success」» Reacted with » {actor_id} to {comment_id}{reset}")
                return True
            else:
                print(f"{r}「Failed」» Reacted with » {actor_id} to {comment_id}{reset}")
                return False
        except Exception:
            print(f"{r}Reaction failed due to an error.{reset}")
            return False

    def extract_comment_id(input_text):
        """Extracts the comment ID from a URL or returns the input if it's already an ID."""
        match = re.search(r"comment_id=(\d+)", input_text)
        return match.group(1) if match else input_text

    def choose_reaction():
        print("Please choose the reaction you want to use.\n")
        reactions = {
            '1': 'Like',
            '2': 'Love',
            '3': 'Haha',
            '4': 'Wow',
            '5': 'Care',
            '6': 'Sad',
            '7': 'Angry',
            '8': 'Remove Reaction'
        }
        for key, value in reactions.items():
            print(f"     「{key}」 {value}")
        
        rec = input('Choose a reaction: ')
        reaction_ids = {
            '1': '1635855486666999',  # Like
            '2': '1678524932434102',  # Love
            '3': '115940658764963',   # Haha
            '4': '478547315650144',   # Wow
            '5': '613557422527858',   # Care
            '6': '908563459236466',   # Sad
            '7': '444813342392137',   # Angry
            '8': '0'                 # Remove Reaction
        }
        return reaction_ids.get(rec)

    def get_ids_tokens(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]

    actor_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    tokens = get_ids_tokens('/sdcard/Test/toka.txt')

    comment_input = input('Enter the Facebook comment ID or link: ')
    comment_id = extract_comment_id(comment_input)
    
    react = choose_reaction()

    def process_reactions(actor_token_pair):
        actor_id, token = actor_token_pair
        return Reaction(actor_id, comment_id, react, token)

    if react == '0':
        remove_count = int(input("How many reactions do you want to remove? "))
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(process_reactions, zip(actor_ids[:remove_count], tokens[:remove_count])))
        success_count = sum(1 for result in results if result)
        print(f"{g}All {success_count} reactions have been successfully removed! You're awesome!{reset}")
    elif react:
        react_count = int(input("How many reactions do you want to send? "))
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(process_reactions, zip(actor_ids[:react_count], tokens[:react_count])))
        success_count = sum(1 for result in results if result)
        print(f"{g}All {success_count} reactions have been successfully sent! You're awesome!{reset}")
    else:
        print(f"{r}Invalid reaction option.{reset}")

# Run the AutoReact script
AutoReact()