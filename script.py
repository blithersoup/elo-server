from requests import post

p = input("Password: ")
# baseurl = "https://localhost:3000" 
baseurl = "http://192.168.0.252:3030"
lid = 1

v = input("Add game or player: (g/p)")

if v == 'p':
    n = input("Name: ")
    res = post(f"{baseurl}/person/add", 
        headers = {
            "Content": "application/json"
        }, 
        json = {
            "password": p,
            "username": n,
            "leagueID": lid
        }
    )
    print(res.status_code)
    print("ok")

if v == 'g':
    w = input("Winner: ")
    l = input("Loser: ")
    res = post(f"{baseurl}/game/add", 
        headers = {
            "Content": "application/json"
        }, 
        json = {
            "password": p,
            "winner": w,
            "loser": l,
            "leagueID": lid
        }
    )
    #print(res.json())
    print(res.status_code)
    print("ok")
