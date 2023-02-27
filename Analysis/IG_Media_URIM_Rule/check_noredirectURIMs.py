import requests

# Open the file containing URLs
with open('final_noredirect_urim.txt', 'r') as f:
    urls = f.readlines()

# Remove whitespace and newlines from URLs
urls = [url.strip() for url in urls]

# Loop through URLs and check status code
for url in urls:
    try:
        response = requests.get(url)
        print(f'{url},{response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'{url},error')