games = {}

while True:
    a = input("Enter URL: ")
    sub = a.split("/")[-1]
    b = sub.split("-i1")
    games[b[0]] = "1" + b[1]
    print(games)