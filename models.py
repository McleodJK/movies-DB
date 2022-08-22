from main import db
from flask_login.mixins import UserMixin

class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    year = db.Column(db.Integer)
    description = db.Column(db.String())
    actors = db.relationship('Role', back_populates='movie',cascade = "all, delete-orphan")

  #use the magic method __repr__ to display it when people use it.
    def __repr__(self):
        return f"New Movie = {self.title} : {self.year}"

class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    birthdate = db.Column(db.String(30))
    movies = db.relationship('Role', back_populates='actor')
 
    def __str__(self):
        return self.name

class Role(db.Model):
    __tablename__ = 'Role'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable = False)
    actor_id = db.Column(db.Integer, db.ForeignKey('Actor.id'), nullable = False)
    role = db.Column(db.String(80), nullable = False)

    actor = db.relationship('Actor', back_populates='movies')
    movie = db.relationship('Movie', back_populates='actors')

# from flask_login.mixins import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(50))
    def __repr__(self):
        return f"Username: {self.username}"
    def check_password(self,password):
        return self.password == password
