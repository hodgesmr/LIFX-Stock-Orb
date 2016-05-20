import requests
from yahoo_finance import Share

######################
#Configuration constants
DAILY_STD_DEV = 1.0 #In percent, what is the standard deviation of stock price change?
CALL_FREQUENCY = 5 #How often this script will be called, in minutes
STOCK_TO_TRACK = '^gspc'

######################
#Get the share price and open, calculate percent change from open
stock = Share(STOCK_TO_TRACK)
pct_change = 100 * (float(stock.get_price()) - float(stock.get_open()))/float(stock.get_open())

######################
#Set up the auth header
f = open('token.txt', 'r')
token = f.readline()
headers = {
    "Authorization": "Bearer %s" % token,
}

#Calculate color from pct_change
how_green = min(max(1.0 + (pct_change/(2*DAILY_STD_DEV)), 0), 1.0)
how_red = min(max(1.0 - (pct_change/(2*DAILY_STD_DEV)), 0), 1.0)
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
if abs(pct_change) > 2*DAILY_STD_DEV:
    breathe_rate = 2/(pct_change/DAILY_STD_DEV)
    print breathe_rate

    #Build the default/common parts of the payload
    payload = {
        'power_on' : 'true',
        'from_color' : my_color,
        'color' : emph_color,
        'period' : breathe_rate,
        'cycles' : breathe_rate*CALL_FREQUENCY*60,
        'persist' : 'true'
    }

    response = requests.post('https://api.lifx.com/v1/lights/all/effects/breathe', params=payload, headers=headers)
    print response.text
