import os
import requests
import time
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

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
        response = requests.post(url, data=payload, timeout=8)
        data = response.json()

        # Debug errors for invalid tokens
        if "error" in data:
            err = data["error"].get("message", "")
            print(f"⚠️ Token {token[:10]}... error: {err}")
            return None

        return data.get("id")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Network issue: {e}")
        return None

def load_tokens(file_path):
    """Loads tokens from a file, one token per line."""
    if not os.path.exists(file_path):
        print("❌ Token file not found.")
        return []

    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def worker(token, link):
    """Single token worker that tries to share once."""
    post_id = share_post(token, link)
    if post_id:
        return f"✅ {token[:8]} shared successfully ({post_id})"
    return None

def fast_share(tokens, link, share_count):
    """Executes the sharing process using threads."""
    start_time = time.time()
    print("🚀 Starting sharing process...\n")

    success = []
    lock = Lock()

    # Create limited thread pool — not 1 per share, that’s wasteful
    with ThreadPoolExecutor(max_workers=min(len(tokens), 50)) as executor:
        futures = []

        # Loop until target shares reached or no valid tokens left
        while len(success) < share_count:
            for token in tokens:
                if len(success) >= share_count:
                    break
                futures.append(executor.submit(worker, token, link))

            for future in as_completed(futures):
                result = future.result()
                if result:
                    with lock:
                        success.append(result)
                        print(f"{len(success)}/{share_count} {result}")
                if len(success) >= share_count:
                    break

            # If all tokens failed, break out — avoid infinite loop
            if all(f.result() is None for f in futures):
                print("\n⚠️ All tokens failed or expired. Stopping.")
                break

    elapsed = timedelta(seconds=int(time.time() - start_time))
    print(f"\n✅ Completed: {len(success)}/{share_count} successful shares")
    print(f"⏳ Total Time: {elapsed}")
    print(f"🚀 Target Link: {link}")

def main():
    token_file = "/sdcard/Test/toka.txt"
    tokens = load_tokens(token_file)

    if not tokens:
        print("❌ No valid tokens found. Exiting...")
        return

    link = input("Enter the post link to share: ").strip()
    print(f"\n✅ Link Confirmed: {link}")

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
