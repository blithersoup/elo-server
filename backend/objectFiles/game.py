from flask import request
from models import League, Person, Game
from models import game_schema
from .league import UpdateLeague

def AddGame(db):
    winner = request.json['winner']
    loser = request.json['loser']
    leagueID = request.json['leagueID']

    league = League.query.get(leagueID)

    WinPlayer = Person.query.filter_by(username=winner).first()
    LossPlayer = Person.query.filter_by(username=loser).first()

    game = Game(WinPlayer.id, LossPlayer.id, leagueID)
    league.gamelist.append(game)
    db.session.add(game)

    WinPlayer.winlist = WinPlayer.winlist + 1
    LossPlayer.losslist = LossPlayer.losslist + 1
    UpdateLeague(db, leagueID)

    db.session.commit()
    return game_schema.jsonify(game)

def DeleteGame(db, id):
    game = Game.query.get(id)
    if game is None:
        return "Game does not exist"
    league_id = game.leagueID
    db.session.delete(game)
    db.session.commit()
    UpdateLeague(db, league_id)
    return game_schema.jsonify(game)

