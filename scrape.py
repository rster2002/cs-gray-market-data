import requests, os, datetime, json, threading

games = json.load(open("games.json"))

mydir = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
os.makedirs(mydir)

def yeet(x):
    print("Getting " + x)
    try:
        response = requests.get(f"https://webapi.g2a.com/ppa/offers/list?productId={games[x]}&hasPlus=false&wholesale=false&isLoggedIn=false&currencyCode=EUR&countryCode=DK&sortBy=rating&sortOrder=desc&lang=english&promotedOffers=true", headers={"Accept-Language": "en-GB,en;q=0.5", "Accept-Encoding": "gzip, deflate, br"}, timeout=30)
    except Exception as e:
        print(f"Exception during request: {e}")
        return

    if (response.status_code != 200):
        print("Err on " + x)
        return

    print("Writing " + x)
    with open(f"{mydir}/{x}.json", "w") as fp:
        fp.write(json.dumps(response.json()))
        
for x in games:
    #threading.Thread(target=yeet, args=(x,)).start()
    yeet(x)