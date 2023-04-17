import re
import random
from xml.dom import ValidationErr
import requests
from flask import Flask, flash, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
import os


app = Flask(__name__)

app.secret_key = "abcd"

# creating the DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'



# Login Manager

login_manger = LoginManager()
login_manger.init_app(app)
login_manger.login_view = 'login'


    # initializing DB

db = SQLAlchemy(app)

class Users(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(250), nullable = False)
        email = db.Column(db.String(250), nullable=False, unique=True)
        password = db.Column(db.String(250), nullable = False)
        genres = db.Column(db.String(250), nullable=True)
        authors = db.Column(db.String(250), nullable=True)
        #create a string

        def __repr__(self):
            return '<Name %r>' % self.name

with app.app_context():
        
    db.create_all()


@login_manger.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



def validate_password(password):  
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if(regex.search(password) == None):
        return False
    if len(password) < 8:  
        return False  
    if not re.search("[a-z]", password):  
        return False  
    if not re.search("[A-Z]", password):  
        return False  
    if not re.search("[0-9]", password):  
        return False  
    return True 


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['rep-pass']

        if repeat_password != password:
            flash("Passwords don't match")
        
        elif not validate_password(password):
            flash("Password must be of atleast 8 characters long and must contain 1) A lower case letter 2) An upper case letter 3) A digit 4) A special character like @_!#$%^&*()<>?/\|}{~:")
        else:
            user = Users.query.filter_by(email=email)

            try:
                user = Users(username=username, email=email, password=password)
                db.session.add(user)
                db.session.commit()
                flash("User Added")
            except:
                flash("User Already Exists. Login Instead")

            return redirect('/login')


    return render_template('sign_up.html')



@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form['username']).first()
        if user:
            #check pass
            if user.password == request.form['password']:
                login_user(user)
                flash("Login Successful")
                form = SearchForm()
                return redirect('/')
            else:
                flash("Wrong Password - Try Again")
        else:
            flash("User does not exists. Register Now")
    return render_template('login.html')


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect("/login")



def validate_search(form, field):
        if len(field.data) > 60:
            raise ValidationErr('Name must be less than 50 characters')
        
class SearchForm(FlaskForm):
    search = StringField(validators=[validate_search])
    # submit = SubmitField(label="")

def search_query(query, number_of_results):

    GOOGLE_BOOKS_ENDPOINT = "https://www.googleapis.com/books/v1/volumes"

    GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")
    params = {
        "q": query,
        "maxResults": number_of_results,
        "langRestrict": "en",
        "key": GOOGLE_BOOKS_API_KEY
    }

    response = requests.get(url=GOOGLE_BOOKS_ENDPOINT, params=params)
    print(response.url)
    return response.json()


def get_trending():
    BESTSELLER_API_ENDPOINT = "https://api.nytimes.com/svc/books/v3/lists/overview.json"
    BESTSELLER_API_KEY = os.environ.get("BESTSELLER_API_KEY")


    params = {
        "api-key": BESTSELLER_API_KEY,
    }
    data = []
    response = requests.get(BESTSELLER_API_ENDPOINT, params=params)
    response.raise_for_status()
    data = response.json()['results']['lists']
    print(response.url)
    return data




@app.route("/", methods=["GET", "POST"])
def home():
    try:
        form = SearchForm()
        trending_data = get_trending()
    except:
        return render_template('error.html')
    else:
        return render_template('index.html', form=form, books=trending_data)

@app.route("/data", methods=["GET","POST"])
def get_data():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.search.data
        validate_search(form, form)
        if query != "":
            data = search_query(query, 40)
            volumeInfos = []
            for item in data['items']:
                if 'averageRating' not in item['volumeInfo']:
                    item['volumeInfo']['averageRating'] = 0
                volumeInfos.append(item['volumeInfo'])
    
            data = sorted(volumeInfos, key=lambda d: d['averageRating'], reverse=True) 

            return render_template('search.html', search = query, data = data)
        else:
            return render_template('index.html', form=form)

@app.route("/<book_name>/<id>", methods=["GET", "POST"])
def get_book(book_name, id):
    data = search_query(id, 40)
    book = {}
    for item in data['items']:
        if item['volumeInfo']['title'] == book_name:
            book = item
            break

    


    try:
        image = book['volumeInfo']['imageLinks']['thumbnail']
    except KeyError:
        book['volumeInfo']['imageLinks'] = "#"
    try:
        genres = ""
        if 'categories' in book['volumeInfo']:
            genres = book['volumeInfo']['categories'][0]
        authors = ""
        if 'authors' in book['volumeInfo']:
            authors = book['volumeInfo']['authors'][0]

    
        id = current_user.id
        user_to_update = Users.query.get_or_404(id)
        user_genres = user_to_update.genres
        if user_genres == None:
            user_genres = genres
        else:
            if len(user_genres) < 230:
                user_genres += f" {genres}"
        user_to_update.genres = user_genres

        user_authors = user_to_update.authors
        if user_authors == None:
            user_authors = authors
        else:
            if len(user_authors) < 230:
                user_authors += f" {authors}"
        user_to_update.authors = user_authors

        db.session.commit()
    

    # hasAverageRating='averageRating' in book['volumeInfo']
    # if not hasAverageRating:
    #     book['volumeInfo']['averageRating'] = ""

    if 'averageRating' not in book['volumeInfo']:
        book['volumeInfo']['averageRating'] = ""

    if 'imageLinks' in book['volumeInfo']:
        if 'thumbnail' in book['volumeInfo']['imageLinks']:
            thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
        else:
            thumbnail = ""
    else:
        thumbnail = ""
    

    if 'description' not in book['volumeInfo']:
        description = ""
    else:
        description = book['volumeInfo']['description']

    if 'publishedDate' in book['volumeInfo']:
        year = book['volumeInfo']['publishedDate'].split('-')[0]
    else:
        year = ""

    flipkart = f"https://www.flipkart.com/search?q={book_name}+{book['volumeInfo']['authors'][0]}"
    amazon = f"https://www.amazon.in/s?k={book_name}+{book['volumeInfo']['authors'][0]}"

    return render_template('book.html', 
                           book_name=book_name,  
                           amazon_link = amazon, 
                           flipkart_link=flipkart,
                           info=book['volumeInfo']['infoLink'],
                           thumbnail=thumbnail,
                           author=book['volumeInfo']['authors'][0],
                           year=year,
                           rating=book['volumeInfo']['averageRating'],
                           description=description,
                           id = id)



@app.route("/recommend")
def recommend():
    id = current_user.id
    user_data = Users.query.get_or_404(id)
    try:
        genre_data = user_data.genres.split()
        author_data = user_data.genres.split()

    except:
        authors = ["JK Rowling", "Stephen King", "Paulo Coelho", "Suzanne Collins", "Rick Riordan", "Chetan Bhagat",
                   "Amish Tripathi", "Ernest Hemingway", "Agatha Christie"]
        data_genre = search_query("fiction", 10)
        data_author = search_query(f"author:{random.choice(authors)}", 10)
        data_author2 = search_query(f"author:{random.choice(authors)}", 10)

    else:
        most_common_author = max(set(author_data), key=author_data.count)
        for author in author_data:
            if author == most_common_author:
                author_data.remove(author)
        if len(author_data) > 0:
            most_common_author2 = max(set(author_data), key=author_data.count)
        else:
            most_common_author2 = ""

        most_common_genre = max(set(genre_data), key=genre_data.count)

        data_genre = search_query(f"subject:{most_common_genre}", 10)
        data_author = search_query(f"author:{most_common_author}", 10)
        data_author2 = search_query(f"author:{most_common_author2}", 10)

    data = data_genre
    for item in data_author['items']:
        data['items'].append(item)
    for item in data_author2['items']:
        data['items'].append(item)

    volumeInfos = []
    for item in data['items']:
        if 'averageRating' not in item['volumeInfo']:
            item['volumeInfo']['averageRating'] = 0
        volumeInfos.append(item['volumeInfo'])
    
    data = sorted(volumeInfos, key=lambda d: d['averageRating'], reverse=True) 

    return render_template('search.html', search = "Recommendation", data = data)


if __name__ == "__main__":
    app.run(debug=True)

