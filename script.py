from requests import post, get, delete

p = input("Password: ")
# baseurl = "https://localhost:3000" 
baseurl = "https://psk-chess-api.herokuapp.com"
lid = 1

v = input("Add game or player (g/p): ")

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
    print(res.status_code)
    print("ok")

if v == 'd':
    id = int(input("Deleted game: "))
    res = delete(f"{baseurl}/game/delete/{id}/",
             headers = {
            "Content": "application/json"
        }, 
        json = {
            "password": p,
            "leagueID": lid
        }

            )
    print(res.status_code)
    print("ok")

