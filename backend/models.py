from __init__ import db, ma
import datetime

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.datetime.now)


    def __init__(self, title, body):
        self.title = title
        self.body = body

class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)



class Person(db.Model): #person
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    passwd = db.Column(db.String(256), unique=True, nullable=False)
    leagueID = db.Column(db.Integer, db.ForeignKey('league.id'))
    elo_score = db.Column(db.Integer, nullable=False)
    winlist = db.Column(db.ARRAY(db.Integer()))
    losslist = db.Column(db.ARRAY(db.Integer()))

    def __init__(self, username, email, passwd, leagueID):
        self.username = username
        self.email = email
        self.passwd = passwd
        self.leagueID = leagueID
        self.elo_score = 800
        self.winlist = None
        self.losslist = None
class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username','email','passwd','LID','leagueID', 'elo_score')

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
        fields = ('id', 'winnner','loser','date', 'leagueID')

game_schema = GameSchema()
games_schema = GameSchema(many=True)


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False) #Name of League, string
    adminID = db.Column(db.Integer, nullable=False) #ID of admin
    playerlist = db.relationship('Person',backref='league', lazy=True) #This and below store lists of players and games
    gamelist = db.relationship('Game', backref='league', lazy=True)

    def __init__(self, name):
        self.name = name
        self.adminID = 0

class LeagueSchema(ma.Schema):
    class Meta:
        fields = ('id','name','adminID','playerlist','gamelist')

league_schema = LeagueSchema()
leagues_schema = LeagueSchema(many=True)
