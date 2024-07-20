import threading
import requests
import time
import json
import urllib.parse
import sys
from colorama import init, Fore, Style
import base64
import random
from concurrent.futures import ThreadPoolExecutor
import math
init(autoreset=True)

# Read and parse the query.txt file
with open('query.txt', 'r') as file:
    lines = file.readlines()

# Extract authorization data from each line
authorizations = [line.strip() for line in lines]

# Read and parse the query.txt file
with open('tokens.txt', 'r') as file:
    lines2 = file.readlines()
tokens = [line.strip() for line in lines2]

def fetch_token(auth, index):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7',
        'access-control-allow-origin': '*',
        'authorization': auth,
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': f'https://game.goldminer.app/{auth}',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Android WebView";v="126"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AG Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.134 Mobile Safari/537.36',
        'x-requested-with': 'org.telegram.messenger.web'
    }
    
    body = {
        'initData': auth
    }
    
    response = requests.post('https://xapi.goldminer.app/auth/login', headers=headers, json=body)
    
    if response.status_code == 200:
        token = response.json()['data']['token']
        return token

if len(tokens) - len(authorizations) != 0:
    # refetch tokens
    f=open('tokens.txt', 'w')
    for i in range(len(authorizations)):
        token = fetch_token(authorizations[i], i)
        f.write(token)
        print(i)
        f.write('\n')
