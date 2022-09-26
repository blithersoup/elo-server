from __init__ import app, ip, db
from objectFiles import game, league, person
from utils.auth import Login
from flask import request
import os
import json

r = json.dumps({"Status": "Not Authorized"})

def passAuth():
    reqpass  = os.environ.get('PASS')
    name = request.json['password']
    return name == reqpass

@app.route("/login", methods=["POST"])
def login():
    if not passAuth(): return r
    return Login()

# @app.route('/league/update/<id>/', methods = ['PUT'])
# def update_league(id):
#     if not passAuth(): return r
#     return league.UpdateLeague(id)

@app.route('/person/add', methods = ['POST'])
def add_person():
    if not passAuth(): return r
    return person.AddPerson(db)

@app.route('/person/delete/<id>/', methods = ['DELETE'])
def person_delete(id):
    if not passAuth(): return r
    return person.DeletePerson(db, id)

@app.route('/person/getstat/<id>/', methods = ['GET'])
def GetPlayerStats(id):
    if not passAuth(): return r
    return person.GetStats(id)

@app.route('/game/get/<id>/', methods = ['GET'])
def GetGame(id):
    if not passAuth(): return r
    return league.GetGame(id)

@app.route('/game/delete/<id>/', methods = ['DELETE'])
def game_delete(id):
    if not passAuth(): return r
    return game.DeleteGame(db, id)

@app.route('/game/add', methods = ['POST'])
def add_game():
    if not passAuth(): return r
    return game.AddGame(db)

@app.route('/league/delete/<id>/', methods = ['DELETE'])
def league_delete(id):
    if not passAuth(): return r
    return league.DeleteLeague(db, id)

@app.route('/league/add', methods = ['POST'])
def add_league():
    if not passAuth(): return r
    return league.AddLeague(db)

'''
@app.route('/league/setadmin/<id>/', methods = ['POST'])
def set_admin(id):
    if not passAuth(): return r
    return league.SetAdmin(db, id)
'''
@app.route('/league/games/<id>/', methods = ['GET'])
def getLeagueGames(id):
    if not passAuth(): return r
    return league.GetGames(id)

@app.route('/league/players/<id>/', methods = ['GET', 'POST'])
def getLeaguePlayers(id):
    if not passAuth(): return r
    return league.GetPlayers(id)

@app.route('/league/info/<id>/', methods = ['GET'])
def LeagueInfo(id):
    if not passAuth(): return r
    return league.LeagueInfo(id)

@app.route('/league/list', methods = ['GET'])
def ListLeagues():
    if not passAuth(): return r
    return league.ListLeagues()

if __name__ == "__main__":
    app.run(host = ip,port=3030,debug=True)
