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
        
def check_miner(headers, token, index):
    body = {"amount": 0, "_token": token}

    try:
        response = requests.post('https://xapi.goldminer.app/account/info', headers=headers, json=body)
        if response.status_code == 200:
            try:
                data            = response.json()['data']
                username        = data['username']
                miners          = len(data['miners'])
                balance_gold    = int(data['coin'])
                print(f'check akun {index} username {username}, miners: {miners}, gold: {balance_gold}')
                if miners == 1 and balance_gold > 1500:
                    buy_miner(headers, token)
                # work(headers, token)
                # work2(headers, token)
                    
            except ValueError as e:
                print(f"Error decoding JSON with token auth: {e}, Response content: {response.text}")
        elif response.status_code not in [500, 503, 502, 520, 521]:
            print(f"Request with index {index} failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request to tap error with token auth: {e}")       

def buy_miner(headers, token):
    # beli miner
    recruitPayload = {
        'asset': 'coin',
        '_token' : token
    }
    try:
        response = requests.post('https://xapi.goldminer.app/miner/recruit', headers=headers, json=recruitPayload)
        if response.status_code == 200:
            print("Sukses beli miner!")
        elif response.status_code not in [500, 503, 502, 520, 521]:
            print(f"Request with index {index} failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request to tap error with token auth: {e}")           

def work(headers, token):
    # list of miners
    listPayload = {
        'page': 1,  
        'perPage' : 10,
        '_token' : token
    }
    response = requests.post('https://xapi.goldminer.app/miner/list', headers=headers, json=listPayload)
    dataMiners = response.json()['data']['items'][0]['id']
    # print(dataMiners)
    
     # list of mine
    listPayload = {
        'page': 1,  
        'perPage' : 20,
        'status' : 1,
        '_token' : token
    }
    response = requests.post('https://xapi.goldminer.app/mine/list', headers=headers, json=listPayload)
    mineData = response.json()['data']['items'][0]['id']
    # print(mineData)
    
    # pasang miner baru
    recruitPayload = {
        'id': dataMiners, # id dari miner nya, ambil dr hasil recruit
        'position' : 1,
        'mine_id' : mineData, # ambil dr [data][mine]
        '_token' : token
    }
    response = requests.post('https://xapi.goldminer.app/miner/work', headers=headers, json=recruitPayload)
    print(f'Berhasil bekerja 1!')   

def work2(headers, token):
    # list of miners
    listPayload = {
        'page': 1,  
        'perPage' : 10,
        '_token' : token
    }
    response = requests.post('https://xapi.goldminer.app/miner/list', headers=headers, json=listPayload)
    dataMiners = response.json()['data']['items'][1]['id']
    # print(dataMiners)
    
     # list of mine
    listPayload = {
        'page': 1,  
        'perPage' : 20,
        'status' : 1,
        '_token' : token
    }
    response = requests.post('https://xapi.goldminer.app/mine/list', headers=headers, json=listPayload)
    mineData = response.json()['data']['items'][0]['id']
    # print(mineData)
    
    # pasang miner baru
    recruitPayload = {
        'id': dataMiners, # id dari miner nya, ambil dr hasil recruit
        'position' : 2,
        'mine_id' : mineData, # ambil dr [data][mine]
        '_token' : token
    }
    response = requests.post('https://xapi.goldminer.app/miner/work', headers=headers, json=recruitPayload)
    print(f'Berhasil bekerja 2!')   

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
            
            # check miner
            check_miner(headers, token, index)

            return None
        
        except Exception as e:
            print(Fore.RED + f"Error fetching data for Akun {index + 1}: {e}")
            time.sleep(5)  # Wait before retrying
        
for index, auth in enumerate(authorizations):
    run_bot(auth, index)
    