import json
import os
import sys

import requests

cas_url = "https://imdcapps.be/"

tokenPath = os.path.join(os.path.dirname(__file__), "ossToken.json")
configurationPath = os.path.join(os.path.dirname(__file__), "ossConfig.json")

if os.path.exists(configurationPath):
    config = json.load(open(configurationPath, "r"))
else:
    print("First define configuration using oss configure ...")
    sys.exit(2)

if os.path.exists(tokenPath):
    token = json.load(open(tokenPath, "r"))
else:
    token = None

authenticated = False
if token:
    rr = requests.post(cas_url + "api-token-verify/", {"token": token})
    if rr.ok:
        authenticated = True
    else:
        print("Token invalid, Fetching new token")

if not authenticated:
    rr = requests.post(cas_url + "api-token-auth/", {
        "username": config["username"],
        "password": config["password"]
    })
    if rr.ok:
        token = rr.json()["token"]
        json.dump(token, open(tokenPath, "w"))
    elif rr.status_code == 401:
        print("Wrong authentication, configure correct username/password combo")
        

def tokenAuth(f):
    def wrapper(s, *args, **kwargs):
        s.headers.update({"Authentication": "token %s"%token})
        f(s, *args, **kwargs)

    return wrapper
