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

# Read and parse the query.txt file
with open('tokens.txt', 'r') as file:
    lines2 = file.readlines()
tokens = [line.strip() for line in lines2]

# Store previous results
previous_results = {}
           
def get_acc_info(auth, token, index):
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
        "amount": 0,
        "_token": token
    }
    response = requests.post('https://xapi.goldminer.app/account/info', headers=headers, json=body)

    if response.status_code == 200:
        data            = response.json()['data']
        username        = data['username']
        balance_gold    = format_balance(data['coin'])
        sellable_gold   = format_balance(data['free_coin'])
        pph             = format_balance(data['power'] * 3600)
        energy          = format_balance(data['store_coin'])
        capacity        = data['store_max']
        # add info miners?, upgrade miners? taro miners di tempat kosong?
        
        result = (
            f"{get_random_color()}{index+1} | "
            f"{get_random_color()}{username}{Style.RESET_ALL} | "
            f"Gold: {Fore.GREEN}{balance_gold}{Style.RESET_ALL} | "
            f"S_Gold: {Fore.YELLOW}{sellable_gold}{Style.RESET_ALL} | "
            f"PPh: {Fore.GREEN}{pph}{Style.RESET_ALL} | "
            f"Energy: {get_random_color()}{energy}{Style.RESET_ALL} | "
            f"Capacity: {get_random_color()}{capacity}{Style.RESET_ALL}"
        )
        # print(result)
        return result
    # return None, None

def buy_and_work(headers, token):
    # beli miner
    recruitPayload = {
        'asset': 'coin',
        '_token' : token
    }
    response = requests.post('https://xapi.goldminer.app/miner/recruit', headers=headers, json=recruitPayload)

    # list of miners
    listPayload = {
        'page': 1,  
        'perPage' : 20,
        'status' : 1,
        '_token' : token
    }
    response = requests.post('https://xapi.goldminer.app/mine/list', headers=headers, json=recruitPayload)
    print(response.json()['data'])

    # pasang miner baru
    recruitPayload = {
        'id': 'asd', # ambil dr 
        'position' : 1, # ambil position yg kosong
        'mine_id' : 974768, # ambil dr [data][mine]
        '_token' : token
    }
    response = requests.post('https://xapi.goldminer.app/miner/work', headers=headers, json=recruitPayload)

def cleartask(headers, token):
    # list of task
    # taskPayload = {
    #     '_token' : token
    # }
    # response = requests.post('https://xapi.goldminer.app/miner/work', headers=headers, json=taskPayload)

    # all task clear
    for i in (1,2,3,4,5,11):
        taskPayload = {
            'id' : i,
            '_token' : token
        }
        response = requests.post('https://xapi.goldminer.app/task/url', headers=headers, json=taskPayload)
        if response.status_code == 200:
            print(response.json())


def tap_tap(auth, token, index):
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
        "amount": 0,
        "_token": token
    }

    # check before
    response = requests.post('https://xapi.goldminer.app/account/info', headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()['data']
        amount = math.floor(data['store_coin'])
    
    # beresin task
    # if task clear semua (fetch list, lalu check, maka gausa ngerun)
    # cleartask(headers, token)

    # beli & pasang miner
    # if len(data['miners']) == 1 and data['coin'] > 1500:
        # buy_and_work(headers, token)

    body = {
        "amount": amount,
        "_token": token
    }

    response = requests.post('https://xapi.goldminer.app/account/info', headers=headers, json=body)
    if response.status_code == 200:
        data            = response.json()['data']
        username        = data['username']
        balance_gold    = format_balance(data['coin'])
        sellable_gold   = format_balance(data['free_coin'])
        pph             = format_balance(data['power'] * 3600)
        energy          = format_balance(data['store_coin'])
        capacity        = data['store_max']
        miners          = len(data['miners'])
        # add info miners?, upgrade miners? taro miners di tempat kosong?
        
        result = (
            f"{get_random_color()}{index+1} | "
            f"{get_random_color()}{username}{Style.RESET_ALL} | "
            f"Miner: {miners}{Style.RESET_ALL} | "
            f"Gold: {Fore.GREEN}{balance_gold}{Style.RESET_ALL} | "
            f"S_Gold: {Fore.YELLOW}{sellable_gold}{Style.RESET_ALL} | "
            f"PPh: {Fore.GREEN}{pph}{Style.RESET_ALL} | "
            f"Energy: {get_random_color()}{energy}{Style.RESET_ALL} | "
            f"Capacity: {get_random_color()}{capacity}{Style.RESET_ALL}"
        )
        print(result)
        return result

# beli miner baru
# taro miner baru biar bekerja

# # TESTING
# get_acc_info(authorizations[0], tokens[0], 0)
# tap_tap(authorizations[1], tokens[1], 1)   

while True:
    
    results = []        
    # Use ThreadPoolExecutor to make requests concurrently
    with ThreadPoolExecutor(max_workers=len(authorizations)) as executor:
        futures = [executor.submit(tap_tap, auth, tokens[index], index) for index, auth in enumerate(authorizations)]
        # futures = [executor.submit(get_acc_info, auth, tokens[index], index) for index, auth in enumerate(authorizations)]
        for future in futures:
            result = future.result()  # Wait for all threads to complete
            if result:
                results.append(result)
    
    if results:
        # Clear the previous output
        print("\033c", end="")  # ANSI escape code to clear the screen
        # Print all results at once
        print("\n".join(results), end="\r", flush=True)
    
    # time.sleep(2)  # Adjust sleep time as needed
    time.sleep(60)  # semenit sekali
    