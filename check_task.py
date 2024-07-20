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

# Function to get random color
def get_random_color():
    colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return random.choice(colors)

def format_balance(balance):
    value = float(balance)
    return "{:.1f}".format(value)

# Read and parse the query.txt file
with open('query.txt', 'r') as file:
    lines = file.readlines()

# Extract authorization data from each line
authorizations = [line.strip() for line in lines]

def get_token(headers, auth):
    body = {'initData': auth}
    try:
        response = requests.post('https://xapi.goldminer.app/auth/login', headers=headers, json=body)
        if response.status_code == 200:
            try:
                token = response.json()['data']['token']
                return token
            except ValueError as e:
                print(f"Error decoding JSON with token auth: {e}, Response content: {response.text}")
        elif response.status_code not in [500, 503, 502, 520, 521]:
            print(f"Request with token {auth} failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"get token error with token auth: {e}")  
        
def checktask(headers, token):
    taskPayload = {
        '_token' : token
    }
    response = requests.post('https://xapi.goldminer.app/task/list', headers=headers, json=taskPayload)
    data = response.json()
    status_array = [item['status'] for item in data['data']]
    # print(status_array)
    # Check if any value in the status array is not 1
    if any(status != 1 for status in status_array):
        print("Task belum selesai..")
        cleartask(headers, token)
    print("Task selesai!")

def cleartask(headers, token):
    # list of task
    taskPayload = {
        '_token' : token
    }
    # clear task
    for i in (1,2,3,4,5,11):
        taskPayload = {
            'id' : i,
            '_token' : token
        }
        response = requests.post('https://xapi.goldminer.app/task/url', headers=headers, json=taskPayload)
        if response.status_code == 200:
            print(f'Task{i} selesai! ' + response.json()['data'])
  
def run_bot(auth, index):
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
    
    while True:
        try:
            # time.sleep(2)
            # get token
            token = get_token(headers, auth)
            
            # check task
            print(f'Check task akun {index}')
            checktask(headers, token)
            
            return None
        
        except Exception as e:
            print(Fore.RED + f"Error fetching data for Akun {index + 1}: {e}")
            time.sleep(5)  # Wait before retrying
        
for index, auth in enumerate(authorizations):
    run_bot(auth, index)
    