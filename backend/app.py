from __init__ import app, ip, db
from objectFiles import game, league, person
from utils.auth import Login

@app.route("/login", methods=["POST"])
def login():
    return Login()



@app.route('/league/update/<id>/', methods = ['PUT'])
def update_league(id):
    return league.UpdateLeague(id)

@app.route('/person/add', methods = ['POST'])
def add_person():
    return person.AddPerson(db)

@app.route('/person/delete/<id>/', methods = ['DELETE'])
def person_delete(id):
    return person.DeletePerson(db, id)

@app.route('/person/getstat/<id>/', methods = ['GET'])
def GetPlayerStats(id):
    return person.GetStats(id)

@app.route('/game/get/<id>/', methods = ['GET'])
def GetGame(id):
    return league.GetGame(id)

@app.route('/game/delete/<id>/', methods = ['DELETE'])
def game_delete(id):
    return game.DeleteGame(db, id)

@app.route('/game/add', methods = ['POST'])
def add_game():
    return game.AddGame(db)

@app.route('/league/delete/<id>/', methods = ['DELETE'])
def league_delete(id):
    return league.DeleteLeague(db, id)

@app.route('/league/add', methods = ['POST'])
def add_league():
    return league.AddLeague(db)

@app.route('/league/setadmin/<id>/', methods = ['POST'])
def set_admin(id):
    return league.SetAdmin(db, id)

@app.route('/league/games/<id>/', methods = ['GET'])
def getLeagueGames(id):
    return league.GetGames(id)

@app.route('/league/players/<id>/', methods = ['GET'])
def getLeaguePlayers(id):
    return league.GetPlayers(id)

@app.route('/league/info/<id>/', methods = ['GET'])
def LeagueInfo(id):
    return league.LeagueInfo(id)

@app.route('/league/list', methods = ['GET'])
def ListLeagues():
    return league.ListLeagues()
    


if __name__ == "__main__":
    app.run(host = ip,port=3000,debug=True)