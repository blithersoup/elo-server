from flask import Flask, jsonify, request
import json
from models import League, Person, Game
from models import league_schema
from utils.elo import EloRating
from .person import GetStats

def AddLeague(db):
    name = request.json['name']

    league = League(name)
    db.session.add(league)
    db.session.commit()
    return league_schema.jsonify(league)

def GetGame(id):
    game = Game.query.get(id)
    if game is None:
        return "Game does not exist"
    stats = {
        'date': str(game.date),
        'id': game.id,
        'leagueID': game.leagueID,
        'loser': game.loser,
        'winner': game.winner
    }
    return json.dumps(stats)

def GetGames(id):
    games = Game.query.filter_by(leagueID=id)
    x = {}
    num = 1
    for game in games:
        gameret = GetGame(game.id)
        gamestat = json.loads(gameret)
        x[f'{num}'] = gamestat
        num = num + 1
    return json.dumps(x)

def GetPlayers(id):
    players = Person.query.filter_by(leagueID=id)
    x = {}
    num = 1
    for player in players:
        playerret = GetStats(player.id)
        playerstat = json.loads(playerret)
        playerstat['username'] = player.username
        x[f'{num}'] = playerstat
        num = num + 1
    return json.dumps(x)

def ListLeagues():
    all_leagues = League.query.all()
    x = {}
    num = 1
    for league in all_leagues:
        leagueret = LeagueInfo(league.id)
        leaguestat = json.loads(leagueret)
        x[f'{num}'] = leaguestat
        num = num + 1
    return jsonify(x)

def LeagueInfo(id):
    league = League.query.get(id)
    if league is None:
        return "League does not exist"
    admin = Person.query.get(league.adminID)
    if admin is None:
        return "League has no admin"
    ret = {
        'name': league.name,
        'id': league.id,
        'adminUser': admin.username
    }
    return json.dumps(ret)

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

def DeleteLeague(db, id):
    league = League.query.get(id)
    if league is None:
        return "League does not exist"
    leagueplayers = Person.query.filter_by(leagueID=id)
    db.session.delete(league)
    for player in leagueplayers:
        db.session.delete(player)
    db.session.commit()
    return "league deleted"

def SetAdmin(db, id):
    adminID = request.json['adminID']
    league = League.query.get(id)
    if league is None:
        return "League does not exist"
    league.adminID = adminID
    db.session.commit()
    return "Admin changed"

