import requests
import json

f = open('token.txt', 'r')
token = f.readline()
print token

headers = {
    "Authorization": "Bearer %s" % token,
}

payload = {
    'power' : 'on',
    'color' : 'red',
}

print payload

response = requests.put('https://api.lifx.com/v1/lights/all/state', params=payload, headers=headers)
print response.text
