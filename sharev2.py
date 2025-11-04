import os
import requests
import threading
import time
from datetime import timedelta
from queue import Queue

def share_post(token, link):
    """Shares a post on the user's feed with 'Only Me' privacy."""
    url = "https://graph.facebook.com/v13.0/me/feed"
    payload = {
        'link': link,
        'published': '0',  
        'privacy': '{"value":"SELF"}',  
        'access_token': token
    }

    try:
        response = requests.post(url, data=payload).json()
        if 'id' in response:
            print(f"✅ Successfully shared post: {response['id']}")  
            return response.get('id')  
        else:
            print(f"❌ Failed to share: {response}")  
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Network error: {e}")  
    return None  

def load_tokens(file_path):
    """Loads tokens from a file, one token per line."""
    if not os.path.exists(file_path):
        print("❌ Token file not found.")
        return []

    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def worker(tokens, link, total_shares, success_queue):
    """Thread worker function to share posts across multiple tokens."""
    while not total_shares.empty():
        token_index = total_shares.get()
        token = tokens[token_index % len(tokens)]  
        post_id = share_post(token, link)
        if post_id:
            success_queue.put(f"{token[:8]}_{post_id}")  
        total_shares.task_done()

def fast_share(tokens, link, share_count):
    """Executes the sharing process using multiple threads."""
    threads = []
    success_queue = Queue()
    total_shares = Queue()

    for i in range(share_count):
        total_shares.put(i)

    start_time = time.time()

    print("🚀 Starting sharing process...")  
    for _ in range(min(len(tokens), 70)):  
        thread = threading.Thread(target=worker, args=(tokens, link, total_shares, success_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    avg_time = timedelta(seconds=int(elapsed_time))
    days, hours, minutes, seconds = avg_time.days, avg_time.seconds // 3600, (avg_time.seconds // 60) % 60, avg_time.seconds % 60

    print("\n📋 Success Details:")
    if success_queue.empty():
        print("❌ No posts were successfully shared.")  # Debug print
    while not success_queue.empty():
        print(f"✅ {success_queue.get()}")

    print(f"\n🚀 Target: {link}")
    print(f"✅ Completed {share_count} shares.")
    print(f"⏳ Average Time: {days:02d}|{hours:02d}|{minutes:02d}|{seconds:02d}")

def main():
    token_file = "/sdcard/Test/toka.txt"
    tokens = load_tokens(token_file)

    if not tokens:
        print("❌ No valid tokens found. Exiting...")
        return

    link = input("Enter the post link to share: ").strip()
    try:
        total_shares = int(input("Enter the total number of shares: ").strip())
        if total_shares <= 0:
            print("❌ Total shares must be greater than 0.")
            return
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return

    fast_share(tokens, link, total_shares)

if __name__ == "__main__":
    main()
