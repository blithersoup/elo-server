from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import socket
from flask_cors import CORS
import json
from elo import EloRating
from __init__ import app, db, ip
from models import League, Person, Game
from models import league_schema, leagues_schema, game_schema, games_schema, person_schema, persons_schema



@app.route('/league/update/<id>/', methods = ['PUT'])
def update_league(id):
    league = League.query.get(id)
    players = league.playerlist
    for player in players:
        player.elo_score = 800
    db.session.commit()
    games = league.gamelist
    for game in games:
        w = game.winner
        l = game.loser
        winnerscore = w.score
        loserscore = l.score
        newranks = EloRating(winnerscore, loserscore)
        w.elo_score = newranks[0]
        l.elo_score = newranks[1]
    db.session.commit()
    return "League updated"

@app.route('/person/add', methods = ['POST'])
def add_person():
    username = request.json['username']
    email = request.json['email']
    passwd = request.json['passwd']
    leagueID = request.json['leagueID']
    league = League.query.get(leagueID)
    person = Person(username, email, passwd, leagueID)
    league.playerlist.append(person)
    db.session.add(person)
    db.session.commit()
    return person_schema.jsonify(person)
#create an account to join {adminID}'s league {league name}

@app.route('/person/delete/<id>/', methods = ['DELETE'])
def person_delete(id):
    person = Person.query.get(id)
    db.session.delete(person)
    gameslost = Game.query.filter_by(loser=id)
    gameswon = Game.query.filter_by(winner=id)
    db.session.delete(gameswon)
    db.session.delete(gameslost)
    db.session.commit()
    update_league()
    return

@app.route('/person/getstat/<id>/', methods = ['GET'])
def GetPlayerStats(db, id):
    person = Person.query.get(id)
    wins = person.winlist.count()
    losses = person.losslist.count()
    elo = person.elo_score
    stats = {
        'wins' : wins,
        'losses' : losses,
        'elo' : elo
    }
    return json.dump(stats)


@app.route('/game/delete/<id>/', methods = ['DELETE'])
def game_delete(id):
    game = Game.query.get(id)
    db.session.delete(game)
    db.session.commit()
    #update player game lists
    update_league()
    return

@app.route('/game/add', methods = ['POST'])
def add_game():
    winner = request.json['winner']
    loser = request.json['loser']
    leagueID = request.json['leagueID']
    league = League.query.get(leagueID)


    game = Game(winner, loser, leagueID)
    league.gamelist.append(game)
    db.session.add(game)
    WinPlayer = Person.query.get(winner)
    LossPlayer = Person.query.get(loser)
    WinPlayer.winlist.append(game.id)
    LossPlayer.losslist.append(game.id)

    db.session.commit()
    return game_schema.jsonify(game)

@app.route('/league/delete/<id>/', methods = ['DELETE'])
def league_delete(id):
    league = League.query.get(id)
    leagueplayers = Person.query.find(leagueID=id)
    db.session.delete(league)
    db.session.delete(leagueplayers)
    db.session.commit()
    #update_league(id)
    return "league deleted"

@app.route('/league/add', methods = ['POST'])
def add_league():
    name = request.json['name']

    league = League(name)
    db.session.add(league)
    db.session.commit()
    return league_schema.jsonify(league)
@app.route('/league/setadmin/<id>/', methods = ['POST'])
def set_admin(id):
    adminID = request.json['adminID']
    league = League.query.get(id)
    league.adminID = adminID
    return "Admin changed"

if __name__ == "__main__":
    app.run(host = ip,port=3000,debug=True)





'''
@app.route('/delete/<id>/', methods = ['DELETE'])
def article_delete(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return article_schema.jsonify(article)
'''
'''
@app.route('/get', methods = ['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    results = jsonify(results)
    return results

@app.route('/get/<id>/', methods = ['GET'])
def post_details(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)
'''

