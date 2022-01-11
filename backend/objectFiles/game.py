from flask import request
from models import League, Person, Game
from models import game_schema
from .league import UpdateLeague

def AddGame(db):
    winner = request.json['winner']
    loser = request.json['loser']
    leagueID = request.json['leagueID']
    league = League.query.get(leagueID)


    game = Game(winner, loser, leagueID)
    league.gamelist.append(game)
    db.session.add(game)
    WinPlayer = Person.query.get(winner)
    LossPlayer = Person.query.get(loser)
    WinPlayer.winlist = WinPlayer.winlist + 1
    LossPlayer.losslist = LossPlayer.losslist + 1

    db.session.commit()
    UpdateLeague(leagueID)
    return game_schema.jsonify(game)



def DeleteGame(db, id):
    game = Game.query.get(id)
    if game is None:
        return "Game does not exist"
    league_id = game.leagueID
    db.session.delete(game)
    db.session.commit()
    UpdateLeague(league_id)
    return game_schema.jsonify(game)

