# LIFX-Stock-Orb
Basic stock orb implemented using a LIFX color changing light bulb

## Intended use
This script checks the current price of the S&P 500, and then changes the light color between red and green based on the percentage
above or below the morning's open price. If the price is up or down drastically, it also kicks in a breathe effect. The intention is
for this script to be fired once every fifteen minutes via a cron job (or similar).

## Pre-reqs

1. python 2.7.6
2. yahoo-finance 1.2.1: https://pypi.python.org/pypi/yahoo-finance
3. requests 2.2.1: http://docs.python-requests.org/en/master/

## Setup

1. Use https://cloud.lifx.com/settings to create an authorization token. Put this token in a file called token.txt.
2. Check the "Configuration constants" at the top of the script, and modify them if desired.
3. Set up some process on your machine to call the script at a rate that matches the CALL_FREQUENCY variable (default is 5 minutes)
