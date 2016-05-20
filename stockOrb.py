import requests
from yahoo_finance import Share

######################
#Configuration constants
DAILY_STD_DEV = 1.0 #In percent, what is the standard deviation of stock price change?
CALL_FREQUENCY = 5 #How often this script will be called, in minutes
STOCK_TO_TRACK = '^gspc'
GOOD_COLOR = [0, 255, 0]
BAD_COLOR = [255, 0, 0]

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

############################
#Calculate color from pct_change

#very good gives lerp_amt of 1, very bad gives 0
lerp_amt = min(max((2*DAILY_STD_DEV + pct_change)/(4*DAILY_STD_DEV), 0), 1)
lerped_color = [int(lerp_amt*GOOD_COLOR[i] + (1-lerp_amt)*BAD_COLOR[i]) for i in range(3)]
highlight_color = [int((255+i)/2) for i in lerped_color]

#Main color
my_color = "#" + ''.join([hex(i)[2:].zfill(2) for i in lerped_color])
#Color for breathe effect ... brighter version of main color
emph_color = "#" + ''.join([hex(i)[2:].zfill(2) for i in highlight_color])

###########################
#First, set the light color

#Build the payload
payload = {
    'power'    : 'on',
    'color'    : my_color,
    'duration' : 5,
}

#Send it, and check results
response = requests.put('https://api.lifx.com/v1/lights/all/state', params=payload, headers=headers)
response.raise_for_status()

###########################
#If it is a big change, do the breathe effect
if abs(pct_change) > 2*DAILY_STD_DEV:
    #The bigger the change, the faster the breathe effect. But keep it
    # between 1 and 8 cycles per second
    breathe_rate = min(max(abs(2/(pct_change/DAILY_STD_DEV)), 1), 8)

    #Build the payload
    payload = {
        'power_on'   : 'true', #Light should already be on, but just in case.
        'from_color' : my_color,
        'color'      : emph_color,
        'period'     : breathe_rate,
        'cycles'     : (1/breathe_rate)*CALL_FREQUENCY*60, #Repeat until the next script call
        'persist'    : 'true'
    }

    #Send message and check response
    response = requests.post('https://api.lifx.com/v1/lights/all/effects/breathe', params=payload, headers=headers)
    response.raise_for_status()
