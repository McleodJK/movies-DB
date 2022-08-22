from flask import Flask, g, render_template, request, flash
from flask_login.utils import login_required, logout_user

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user

# import the db models
import models

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miniIMDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'correcthorsebatterystaple'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'

######################## LOGIN ########################
#required for the user longin
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id) # Fetch the user from the database


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        #we posted the form- try to login
        #get the user from the forms username field
        user = models.User.query.filter_by(username=request.form.get("username")).first()
        #chek if we got one and that the password's match- MUST USE HASHED PASSWORDS!!! THIS IS JUST A DEMO!!
        if user and user.check_password(request.form.get("password")):
            login_user(user)
            #now current_user is set to this user- redirect back to home
            movies = models.Movie.query.all()
            actors = models.Actor.query.all()
          
            return render_template("add_movie.html", movies = movies, actors = actors)
        #else flash a message?
        else:
            flash("Username and password not recognised")
    return render_template("login.html")

######################## LOGout ########################
@app.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    '''log out the user- pretty self-explanatory'''
    logout_user()
    return render_template("home.html")
  
######################## HOME ########################
# home route
@app.route('/')
def home():
    return render_template('home.html', page_title='IT WORKS!')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html', page_title='IT WORKS!')

######################## list all MOVIE ########################
  
# list all the movies
@app.route('/all_movies')
def all_movies():
    movies = models.Movie.query.all()
    return render_template('all_movies.html', page_title="ALL MOVIES", movies=movies)

######################## DISPLAY MOVIE ########################
  
# details of one movie
@app.route('/movie/<int:id>')
def movie(id):
  movie = models.Movie.query.filter_by(id=id).first()
  if movie == None:
    # throw 404
    return render_template("404.html")
  title = movie.title
  return render_template('movie.html',page_title=title,movie=movie)



######################## CHOOSE MOVIE ########################

  
@app.route('/choose_movie')
def choose_movie():
 movies = models.Movie.query.all()
 return render_template('choose_movie.html', title='Select A Movie', movies=movies) 

######################## GOTO MOVIE ########################
@app.route('/goto_movie', methods=['GET','POST'])
def goto_movie():
  #get the value of the hidden input named "movie_id" in the html template if the form exists from the post
    if request.form:
      movie_id = request.form.get("movie_id")
      movie = models.Movie.query.filter_by(id=movie_id).first()
      print(f'movie_id = {movie_id}')
      return render_template('movie.html', movie=movie)
######################## DELETE MOVIE ########################

@app.route('/delete_movie', methods=['GET','POST'])
@login_required
def delete_movie():
    #get the value of the hidden input named "movie_id" in the html template if the form exists from the post
    if request.form:
      movie_id = request.form.get("movie_id")
      # debug
      print(f"movie to delete = {movie_id}")
      #and do sql stuff to remove it! find the question we want to dlete from it's id
      movie_to_delete = models.Movie.query.filter_by(id=movie_id).first()
      # debug
      print(f"movie_to_delete = {movie_to_delete}")

  
# https://stackoverflow.com/questions/24291933/sqlalchemy-object-already-attached-to-session

      db.Session = db.Session.object_session(movie_to_delete)
      db.Session.delete(movie_to_delete)
      
      #db.session.delete(movie_to_delete)#delete it
      db.Session.commit()#commit change to db
      db.Session.close()

    #url_redirect = url_for("home")
    #print(url_redirect)
    #return redirect(url_for("add_movie"))
    movies= models.Movie.query.all()
    return render_template("add_movie.html", movies=movies, page_title = "Add")

######################## ADD MOVIE ########################

@app.route('/add_movie', methods=['GET','POST'])
@login_required
def add_movie():
  movies = models.Movie.query.all()
  actors = models.Actor.query.all()
#this will add a movie to the database and redirect to the add_movie route again
  if request.form:
        #we got a form back now process by getting the items by their name
    new_title = request.form.get("title")#get questions from form
    new_year = request.form.get("year")     #get answer from form
    new_description = request.form.get("description")
    new_movie =  models.Movie(title=new_title,year=new_year,description=new_description)  #create a new movie instance
    db.session.add(new_movie)
    db.session.commit()

    
  movies = models.Movie.query.all()
  return render_template('add_movie.html', page_title='Add', movies = movies, actors = actors)

######################## ADD ACTOR ########################

@app.route('/add_actor', methods=['GET','POST'])
def add_actor():
  movies = models.Movie.query.all()
#this will add a movie to the database and redirect to the add_movie route again
  if request.form:
        #we got a form back now process by getting the items by their name
    new_actor = request.form.get("name")#get actor from form
    new_dob = request.form.get("dob")     #get dob from form
    new_actor =  models.Actor(name=new_actor,birthdate=new_dob)  #create a new actor instance
    db.session.add(new_actor)
    db.session.commit()

    
  movies = models.Movie.query.all()
  return render_template('add_movie.html', page_title='Add', movies = movies)

######################## ADD ROLE ########################
@app.route('/add_role', methods=['GET','POST'])
def add_role():
  if request.form:
    new_movie = request.form.get("movie")
    new_actor = request.form.get("actor")
    # debug
    print(f"movie: {new_movie} actor: {new_actor}")
    new_position = request.form.get("role")
    new_role = models.Role(movie_id = new_movie, actor_id = new_actor, role = new_position)
    db.session.add(new_role)
    db.session.commit()
    movies = models.Movie.query.all()
    actors = models.Actor.query.all()
    return render_template('add_movie.html', page_title='Add', movies = movies, actors = actors)

# https://hackersandslackers.com/flask-wtforms-forms/
    
@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Standard `contact` form."""
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template(
        "contact.jinja2",
        form=form,
        template="form-template"
    )

    
######################## 404 ########################

@app.errorhandler(404)
def page_not_found(e):
   return render_template("404.html")

######################## start server ########################

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)