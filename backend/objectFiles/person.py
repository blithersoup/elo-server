from flask import request
import json
from models import League, Person, Game
from models import person_schema
from utils.elo import EloRating

def UpdateLeague(db, id):
    league = League.query.get(id)
    if league is None:
        return "League does not exist"
    players = league.playerlist
    for player in players:
        player.elo_score = 800
        player.winlist = 0
        player.losslist = 0
    db.session.commit()
    games = league.gamelist
    for game in games:
        w = Person.query.get(game.winner)
        l = Person.query.get(game.loser)
        winnerscore = w.elo_score
        loserscore = l.elo_score
        newranks = EloRating(winnerscore, loserscore)
        w.elo_score = newranks[0]
        l.elo_score = newranks[1]
        w.winlist = w.winlist + 1
        l.losslist = l.losslist + 1
    db.session.commit()
    return "League updated"

def AddPerson(db):
    username = request.json['username']
    #email = request.json['email']
    #passwd = request.json['passwd']
    leagueID = request.json['leagueID']
    league = League.query.get(leagueID)
    person = Person(username, leagueID)
    league.playerlist.append(person)
    db.session.add(person)
    db.session.commit()
    return person_schema.jsonify(person)
#create an account to join {adminID}'s league {league name}

def GetStats(id):
    person = Person.query.get(id)
    if person is None:
        return "Person does not exist"
    wins = person.winlist
    losses = person.losslist
    elo = person.elo_score
    username = person.username
    stats = {
        'username': username,
        'wins' : wins,
        'losses' : losses,
        'elo' : elo,
        'id' : person.id
    }
    return json.dumps(stats)

def DeletePerson(db, id):
    person = Person.query.get(id)
    if person is None:
        return "Person does not exist"
    league_id = person.leagueID
    db.session.delete(person)
    gameslost = Game.query.filter_by(loser=id)
    gameswon = Game.query.filter_by(winner=id)
    for game in gameswon:
        db.session.delete(game)
    for game in gameslost:
        db.session.delete(game)
    db.session.commit()
    UpdateLeague(db, league_id)
    return person_schema.jsonify(person)

