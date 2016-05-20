import requests
import json

#Set up the auth header
f = open('token.txt', 'r')
token = f.readline()
headers = {
    "Authorization": "Bearer %s" % token,
}

std_dev_change = 1.0
two_std_dev_change = 2*std_dev_change

pct_change = -2.01

#Calculate color from pct_change
how_green = min(max(1.0 + (pct_change/two_std_dev_change), 0), 1.0)
how_red = min(max(1.0 - (pct_change/two_std_dev_change), 0), 1.0)
green = int(255.999*how_green)
red = int(255.999*how_red)

my_color = "#" + hex(red)[2:].zfill(2) + hex(green)[2:].zfill(2) + "00"
emph_color = "#" + hex((red+255)/2)[2:].zfill(2) + hex((green+255)/2)[2:].zfill(2) + "7f"
print my_color

#Build the default/common parts of the payload
payload = {
    'power' : 'on',
    'color' : my_color,
    'duration' : 5,
}


response = requests.put('https://api.lifx.com/v1/lights/all/state', params=payload, headers=headers)
print response.text

if abs(pct_change) > 2*std_dev_change:
    #Build the default/common parts of the payload
    payload = {
        'power_on' : 'true',
        'from_color' : my_color,
        'color' : emph_color,
        'period' : 1,
        'cycles' : 15*60,
        'persist' : 'true'
    }

    response = requests.post('https://api.lifx.com/v1/lights/all/effects/breathe', params=payload, headers=headers)
    print response.text
