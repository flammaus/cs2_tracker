#Prices below last updated: 9/14/2026 - edit these prices for more accurate prediction

tracked_cases = [
    #Clutch is easiest to predict, no longer dropping
    {"name": "Clutch Case", "base_price": 0.81},
    {"name": "Spectrum 2 Case", "base_price": 4.40},
    {"name": "Chroma 2 Case", "base_price": 5.72},
    {"name": "Operation Phoenix Weapon Case", "base_price": 6.00},
    #May remove breakout if prices get too high
    {"name": "Operation Breakout Weapon Case", "base_price": 11.91},
]

import urllib.request
import urllib.parse
import json
import time
import gzip

####################################################################################################################
#****Connecting to steam cookie file for easier login and no error - PASTED FROM CLAUDE / KEPT GETTING 429 ERROR****
def load_steam_cookie():
    with open("steam_cookie.txt", "r") as file:
        return file.read().strip()

STEAM_LOGIN_COOKIE = load_steam_cookie()
#****Connecting to steam cookie file for easier login and no error - PASTED FROM CLAUDE / KEPT GETTING 429 ERROR****
####################################################################################################################

#Steam fee + Game fee = take ~13% on a sale, ending with ~87%
STEAM_SELL_RATE = 0.87

def get_case_price(item_name):
    base_url = "https://steamcommunity.com/market/priceoverview/"
    params = urllib.parse.urlencode({
        #CS2 = ID 730
        #USD = 1
        "appid": 730,
        "currency": 1,
        "market_hash_name": item_name
    })
    full_url = f"{base_url}?{params}"

    ####################################################################################
    #****Bypassing Steam bot detection - PASTED FROM CLAUDE / KEPT GETTING 429 ERROR****
    request = urllib.request.Request(full_url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://steamcommunity.com/market/",
        "Cookie": f"steamLoginSecure={STEAM_LOGIN_COOKIE}",
    })
    #****Bypassing Steam bot detection - PASTED FROM CLAUDE / KEPT GETTING 429 ERROR****
    ####################################################################################
    
    #"try" will attempt steams server, except will prevent from crashing
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read())
        return data
    except urllib.error.HTTPError as error:
        raw_body = error.read()
        try:
            body_text = gzip.decompress(raw_body).decode(errors="replace")
        except OSError:
            body_text = raw_body.decode(errors="replace")
        print(f"Steam blocked this request (HTTP {error.code}).")
        print(f"Response body: {body_text}")
        print(f"Response headers: {dict(error.headers)}")
        return None

def price_to_float(price_string):
    #Converting numbers and making them useful to the code: "$1.00" -> "1.00" -> 1.00
    cleaned = price_string.replace("$", "")
    return float(cleaned)

#Base price set by hand in tracked_cases, this the price we started watching at
#Current price pulled live from steam api every time script runs
for case in tracked_cases:
    price_data = get_case_price(case["name"])
    #if/else for steam errors
    if price_data is None:
        case["current_price"] = "error"
    else:
        case["current_price"] = price_to_float(price_data["lowest_price"])

#AFTER CURRENT PRICE SET ABOVE, BELOW IS CASE MATH AND MAKING SURE "price = error" WILL NOT HAPPEN
    if case["current_price"] == "error":
        case["signal"] = "unknown"
    else:
        breakeven_price = case["base_price"] * STEAM_SELL_RATE
        expected_gain_usd = breakeven_price - case["current_price"]
        #Green appears when $.01 profit is possible or more
        if expected_gain_usd >= 0.01:
            case["signal"] = "green"
            case["expected_gain_usd"] = expected_gain_usd
            case["expected_gain_percent"] = (expected_gain_usd / case["current_price"]) * 100
        else:
            case["signal"] = "red"

#LAYOUT FOR RED AND GREEN GUI - PROFIT PRICES AND PROFIT PERCENTAGES
    print(f"{case['name']}: watch price ${case['base_price']:.2f}, current price ${case['current_price']}")
    if case["signal"] == "green":
        print(f"  -> BUY, expected gain ${case['expected_gain_usd']:.2f} ({case['expected_gain_percent']:.1f}%)")
    elif case["signal"] == "red":
        print(f"  -> DON'T BUY")
    else:
        print(f"  -> unknown, steam error")
    time.sleep(2)