*CS2 Case Tracker*

Python script that checks live CS2 case prices on the Steam Community Market and tells me if a case dropped low enough below my original watch price to be worth buying, after Steam's ~13% sell fee. Only using Python's standard library (urllib, json, time), no outside packages, since this is a learning project for me and I wanted to actually understand every line.

Steam's price check isn't a real public API and it blocks/rate-limits requests a lot, sometimes for no clear reason. I tried spoofing a browser user-agent, that didn't help. Adding a logged-in Steam cookie fixed it for a bit then it started getting blocked again anyway. Still not sure exactly why. Didn't want to add outside libraries just to fight it, so if a case gets blocked the script just shows it as an error instead of crashing.

Also want to be upfront, I used Claude for help in two spots since I'm still new to error handling/auth stuff:
- the cookie login part (load_steam_cookie() and the Cookie header in get_case_price()) - I didn't know how to send an authenticated request so Claude helped me figure that part out
- the try/except around the 429 error - Claude helped me handle it so it prints "error" instead of crashing the whole script

Everything else, the price math, the fee calc, the buy/don't buy logic, is mine.
