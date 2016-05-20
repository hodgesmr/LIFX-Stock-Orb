import requests
import json
from yahoo_finance import Share

#Some constants
std_dev_change = 1.0
two_std_dev_change = 2*std_dev_change

#Get the share price and open, calculate percent change from open
gspc = Share('^gspc')
pct_change = 100 * (float(gspc.get_price()) - float(gspc.get_open()))/float(gspc.get_open())

#Set up the auth header
f = open('token.txt', 'r')
token = f.readline()
headers = {
    "Authorization": "Bearer %s" % token,
}

#Calculate color from pct_change
how_green = min(max(1.0 + (pct_change/two_std_dev_change), 0), 1.0)
how_red = min(max(1.0 - (pct_change/two_std_dev_change), 0), 1.0)
green = int(255.999*how_green)
red = int(255.999*how_red)

#Main color
my_color = "#" + hex(red)[2:].zfill(2) + hex(green)[2:].zfill(2) + "00"
#Color for breathe effect ... brighter version of main color
emph_color = "#" + hex((red+255)/2)[2:].zfill(2) + hex((green+255)/2)[2:].zfill(2) + "7f"


###First, set the light color
#Build the default/common parts of the payload
payload = {
    'power' : 'on',
    'color' : my_color,
    'duration' : 5,
}

response = requests.put('https://api.lifx.com/v1/lights/all/state', params=payload, headers=headers)

####Next, if it is a big change, do the breathe effect
if abs(pct_change) > 2*std_dev_change:
    breathe_rate = 2/(pct_change/std_dev_change)
    print breathe_rate

    #Build the default/common parts of the payload
    payload = {
        'power_on' : 'true',
        'from_color' : my_color,
        'color' : emph_color,
        'period' : breathe_rate,
        'cycles' : breathe_rate*15*60,
        'persist' : 'true'
    }

    response = requests.post('https://api.lifx.com/v1/lights/all/effects/breathe', params=payload, headers=headers)
    print response.text
