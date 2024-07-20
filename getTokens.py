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

if len(tokens) - len(authorizations) != 0:
    # refetch tokens
    f=open('tokens.txt', 'w')
    for i in range(len(authorizations)):
        token = fetch_token(authorizations[i], i)
        f.write(token)
        print(i)
        f.write('\n')