import cloudscraper
import time

CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def post_request(url, headers, payload=None, proxies=None):
    scraper = cloudscraper.create_scraper()
    response = scraper.post(url, json=payload, headers=headers, proxies=proxies)
    
    if response.status_code in [200, 201]:
        try:
            return response.json(), response.cookies
        except ValueError:
            return response.text, response.cookies
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response text: {response.text}")
        return None, None

def get_request(url, headers, query_id, proxies=None):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(f"{url}?query_id={query_id}", headers=headers, proxies=proxies)
    
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Response is not JSON.")
            return None
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response text: {response.text}")
        return None

def read_init_data(filename):
    try:
        with open(filename, 'r') as file:
            query_ids = [line.strip().split('=')[1] for line in file if line.startswith("query_id=")]
            return query_ids
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def read_proxies(filename):
    try:
        with open(filename, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
            return proxies
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def process_query_id(query_id, proxies):
    url_base = "https://api-tg-app.midas.app/api/"
    
    # Use the first proxy or default to None if no proxies are provided
    proxy = {"http": proxies.pop(0), "https": proxies.pop(0)} if proxies else None

    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Mobile Safari/537.36",
    }

    print(f"{CYAN}Processing query_id: {query_id}{RESET}")
    
    # Example request: Get user info
    url_user = f"{url_base}user"
    user_data = get_request(url_user, headers, query_id, proxies=proxy)

    if user_data:
        print(f"{GREEN}User data retrieved successfully.{RESET}")
        # Display user data (you can modify this as needed)
        for key, value in user_data.items():
            print(f"{key}: {value}")
    else:
        print(f"{RED}Failed to retrieve user data for query_id: {query_id}{RESET}")

def main():
    query_ids = read_init_data('auth.txt')
    proxies = read_proxies('proxies.txt')  # Optional file with proxy list

    for query_id in query_ids:
        process_query_id(query_id, proxies)
        print(f"{YELLOW}Waiting 10 seconds before processing the next query_id...{RESET}")
        time.sleep(10)

if __name__ == "__main__":
    main()
