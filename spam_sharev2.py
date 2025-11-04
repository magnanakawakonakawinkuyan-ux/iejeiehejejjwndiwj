import os
import requests
import threading
import time
from datetime import timedelta

# Global shared count with thread lock for accuracy
lock = threading.Lock()
shared_count = 0  # Only successful shares count


def share_post(token, link):
    """Shares a post on the user's feed with 'Only Me' privacy."""
    url = "https://graph.facebook.com/v13.0/me/feed"
    payload = {
        "link": link,
        "published": "0",  # Prevents posting publicly
        "privacy": '{"value":"SELF"}',  # 'Only Me'
        "access_token": token
    }

    try:
        response = requests.post(url, data=payload, timeout=10).json()
        if "id" in response:
            return response["id"]
    except requests.exceptions.RequestException:
        pass

    return None


def load_tokens(file_path):
    """Loads tokens from a file, one token per line."""
    if not os.path.exists(file_path):
        print("❌ Token file not found.")
        return []

    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def worker(tokens, link, target):
    """Thread worker function to share posts while ensuring exact target count."""
    global shared_count
    token_index = 0

    while True:
        with lock:
            if shared_count >= target:
                break
            token = tokens[token_index % len(tokens)]
            token_index += 1

        post_id = share_post(token, link)
        if post_id:
            with lock:
                shared_count += 1
                count = shared_count
            print(f"{count}/{target} ✅ {token[:10]}... shared successfully (Post ID: {post_id})")
        else:
            print(f"❌ {token[:10]}... failed to share")


def fast_share(tokens, link, share_count):
    """Executes the sharing process using multiple threads with thread safety."""
    global shared_count
    shared_count = 0  # Reset counter before starting

    threads = []
    start_time = time.time()

    print("\n🚀 Starting sharing process...")

    thread_count = min(len(tokens), 70)  # Limit threads for safety
    for _ in range(thread_count):
        thread = threading.Thread(target=worker, args=(tokens, link, share_count))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_td = timedelta(seconds=int(elapsed_time))

    print(f"\n🚀 Target Link: {link}")
    print(f"✅ Completed: {shared_count}/{share_count} successful shares")
    print(f"⏳ Elapsed Time: {elapsed_td}")


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
        print("❌ Invalid input. Please enter a valid number.")
        return

    fast_share(tokens, link, total_shares)


if __name__ == "__main__":
    main()
