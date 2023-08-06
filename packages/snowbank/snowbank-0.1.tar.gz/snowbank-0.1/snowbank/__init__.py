import requests


def initUser(token):
    url = "https://snowbank.me:8000/init-user"
    payload = ""
    headers = {
    'Authorization': "%s"%(token),
    'Content-Type': "application/json"
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    return str(response.text)

def createUser(password,userHash,token):
    url = "https://snowbank.me:8000/create-user"

    payload = "{ \"password\": '%s', \"userHash\": '%s' }"%(password,userHash)
    headers = {
    'Content-Type': "application/json",
    'Authorization': "%s"%(token),
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text

def userBalance(userHash,token):
    url = "https://snowbank.me:8000/user/balance"
    payload = "{\"userHash\":'%s' }"%(userHash)
    headers = {
    'Authorization': "%s"%(token),
    'Content-Type': "application/json"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text

def generateAddress(userHash,token):
    url = "https://snowbank.me:8000/user/generate-address"
    payload = "{\"userHash\": '%s'}"%(userHash)
    headers = {
    'Authorization': "%s"%(token),
    'Content-Type': "application/json",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text

def publicKey(userHash,token):
    url = "https://snowbank.me:8000/user/public-key"
    payload = "{\"userHash\": '%s'}"%(userHash)
    headers = {
    'Authorization': "%s"%(token),
    'Content-Type': "application/json"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text

def getUsers(token):
    url = "https://snowbank:8000/get-users"
    payload = ""
    headers = {
    'Authorization': "%s"%(token),
    'Content-Type': "application/json"
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    return response.text

def createChannel(fromUserHash,toUserHash,satoshi,token):
    url = "https://snowbank.me:8000/create-channel"
    payload = "{\"fromUserHash\": '%s', \"toUserHash\": '%s', \"satoshi\": '%s'}"%(fromUserHash,toUserHash,satoshi)
    headers = {
    'Authorization': "%s"%(token),
    'Content-Type': "application/json"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text

def sendCoin(fromUserHash,toUserHash,satoshi,token):
    url = "https://snowbank.me:8000/send-coin"
    payload = "{\"fromUserHash\": '%s' , \"toUserHash\": '%s', \"satoshi\": '%s'}"%s(fromUserHash,toUserHash,satoshi)
    headers = {
    'Authorization': "%s"%(token),
    'Content-Type': "application/json"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text