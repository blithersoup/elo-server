from __init__ import db, ma
import datetime
#from werkzeug.security import generate_password_hash, check_password_hash


class Person(db.Model): #person
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    #email = db.Column(db.String(100), unique=True, nullable=False)
    #passwd = db.Column(db.String(256), unique=True, nullable=False)
    leagueID = db.Column(db.Integer, db.ForeignKey('league.id'))
    elo_score = db.Column(db.Integer, nullable=False)
    winlist = db.Column(db.Integer())
    losslist = db.Column(db.Integer())

    def __init__(self, username, leagueID):
        self.username = username
        self.winlist = 0
        self.losslist = 0
        self.leagueID = leagueID
        self.elo_score = 800
''' 
    def VerifyPassword(self, password):
        if self is not None and check_password_hash(self.passwd, password):
            return self.username
'''


class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username','LID','leagueID', 'elo_score')

person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner = db.Column(db.Integer, db.ForeignKey('person.id'))
    loser = db.Column(db.Integer, db.ForeignKey('person.id'))
    date = db.Column(db.DateTime, default = datetime.datetime.now)
    leagueID = db.Column(db.Integer, db.ForeignKey('league.id'))
    
    def __init__(self, winner, loser, leagueID):
        self.winner = winner
        self.loser = loser
        self.leagueID = leagueID

class GameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'winner','loser','date')

game_schema = GameSchema()
games_schema = GameSchema(many=True)


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False) #Name of League, string
    #adminID = db.Column(db.Integer, nullable=False) #ID of admin
    playerlist = db.relationship('Person',backref='league', lazy=True) #This and below store lists of players and games
    gamelist = db.relationship('Game', backref='league', lazy=True)

    def __init__(self, name):
        self.name = name
        # self.adminID = 0

class LeagueSchema(ma.Schema):
    class Meta:
        fields = ('id','name','playerlist','gamelist')

league_schema = LeagueSchema()
leagues_schema = LeagueSchema(many=True)
