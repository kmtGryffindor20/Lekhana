import json
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


app = Flask(__name__)  # This creates a Flask Application with file __name__

app.secret_key = "abcd"

# creating the DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres", "postgresql")


# Login Manager

login_manger = LoginManager()
login_manger.init_app(app)
login_manger.login_view = 'login'


    # initializing DB

db = SQLAlchemy(app)  # Creating an SQL database in the app


# This is to Model the database according to the data required to be filled in
class Users(db.Model, UserMixin):
        '''User Model for database'''
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(250), nullable = False)
        email = db.Column(db.String(250), nullable=False, unique=True)
        password = db.Column(db.String(250), nullable = False)
        genres = db.Column(db.String(250), nullable=True)
        authors = db.Column(db.String(250), nullable=True)
        #create a string

        def __repr__(self):
            return '<Name %r>' % self.name


# The database of a Flask app can only be created for the first time within the app's context
with app.app_context():
        
    db.create_all()


# On successful login fetches the user with the given user id and returns as the current user
@login_manger.user_loader
def load_user(user_id : int):
    '''Loads the user with the given id'''
    return Users.query.get(int(user_id))


def validate_password(password : str):  
    '''Validates the password entered by the user'''
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


# Application's function when the /signup page is opened
@app.route('/signup', methods=['GET', 'POST'])  # Has both Get and Post methods
def sign_up():
    '''For the signup page. Checks if user already exists or not and saves the user.'''
    if request.method == "POST":  # If the request is for post we retrieve the user filled data
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
                # This creates a new user with the given details
                user = Users(username=username, email=email, password=password)
                db.session.add(user)  # Adds the user to the sql database
                db.session.commit()  # Commiting the changes to the database 
                flash("User Added")
            except:
                flash("User Already Exists. Login Instead")

            return redirect('/login')


    return render_template('sign_up.html')


# Application's function for the /login page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":  # When the user fills in the form
        user = Users.query.filter_by(username=request.form['username']).first()  # Get the first occuremce of the given username
        if user:
            if user.password == request.form['password']:  # If the Input password is same as stored password 
                login_user(user)  # We login the current user
                flash("Login Successful")
                return redirect('/')
            else:
                flash("Wrong Password - Try Again")
        else:
            flash("User does not exists. Register Now")
    return render_template('login.html')


# Applications's Function to get to logout the user
@app.route("/logout", methods=["GET", "POST"])
@login_required  # This function requires the user to be logged in already to execute
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect("/login")


# Function that validates the search field, 50 characters or less ( Unnecessary Addition )
def validate_search(form, field):
        '''Function that validates the search field, 50 characters or less'''
        if len(field.data) > 60:
            raise ValidationErr('Name must be less than 50 characters')
        


# A class for the SearchForm of the FlaskForm. Makes it easier to get the data from any post request
class SearchForm(FlaskForm):
    search = StringField(validators=[validate_search])
    # submit = SubmitField(label="")


# Constants of Google Books API Key and the Google Books API Endpoint
GOOGLE_BOOKS_ENDPOINT = "https://www.googleapis.com/books/v1/volumes"
GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")


def search_query(query : str, number_of_results : int):
    '''Searches for a list of books with the given query and the for the number_of_results'''
    response = {'items':[]}
    if number_of_results <= 40:
        params = {
            "q": query,
            "maxResults": number_of_results,
            "langRestrict": "en",
            "key": GOOGLE_BOOKS_API_KEY
        }
        response = requests.get(url=GOOGLE_BOOKS_ENDPOINT, params=params)
        print(response.url)
        response = response.json()
    else:
        # As the API limits at 40 books at a time this causes us to get all the books needed
        index = 0
        while index < number_of_results:
            params = {
                "q": query,
                "maxResults": 40,
                "startIndex": index,
                'langRestrict': "en",
                "key": GOOGLE_BOOKS_API_KEY
            }
            index += 40
            new_response = requests.get(url=GOOGLE_BOOKS_ENDPOINT, params=params)
            print(new_response.url)
            items = new_response.json()['items']
            for item in items:
                response['items'].append(item)

    
    return response


def search_book(id : str):
    '''Searches a specific book with a given id'''
    BOOKS_ENDPOINT = GOOGLE_BOOKS_ENDPOINT + f"/{id}"
    params = {
        'key': GOOGLE_BOOKS_API_KEY
    }
    response = requests.get(BOOKS_ENDPOINT, params=params)
    print(response.url)
    return response.json()


def get_trending():
    '''Returns the this week's New York Times Bestsellers of all categories'''

    # The NYT API Endpoint and Key
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


# Application's function for the landing page
@app.route("/", methods=["GET", "POST"])
def home():
    try:
        form = SearchForm()  # Creates a Flask Form that is used in the main area search field
        trending_data = get_trending()
    except:
        return render_template('error.html')
    else:
        return render_template('index.html', form=form, books=trending_data)  # The variables required in the index.html are sent through here


# Application's function for the search query
@app.route("/data", methods=["GET","POST"])
def get_data():

    # If the search has been made through the nav bar
    if request.method == "POST":
        query = request.form['search']

    # If the search has been made through the main search area
    form = SearchForm()
    if form.validate_on_submit():  # When the form is validated by submition
        query = form.search.data  # We get the query from the form field
        validate_search(form, form)

    if query != "":  # If the search field was not empty
        data = search_query(query, 160)  # 160 books are being searched for it
        volumeInfos = []
        for item in data['items']:

            # If book does not have a rating, rating is given to it
            if 'averageRating' not in item['volumeInfo']:
                item['volumeInfo']['averageRating'] = 0
            else:
                item['volumeInfo']['averageRating'] = float(item['volumeInfo']['averageRating'])
            volumeInfos.append(item['volumeInfo'])

        # The books are sorted as per their rating using the lamda function in the sorted: key parameter
        data = sorted(volumeInfos, key=lambda d: d['averageRating'], reverse=True) 

        return render_template('search.html', search = query, data = data, len = 160)
    else:
        # If the search was empty we do reload the page
        return render_template('index.html', form=form)


# Application's function for the specific book page
@app.route("/<book_name>/<id>", methods=["GET", "POST"])
def get_book(book_name, id):
    '''Gets all the data of the given book id'''

    # Search for the book id
    book = search_book(id)

    # Check if the books has a thumbnail or not
    try:
        image = book['volumeInfo']['imageLinks']['thumbnail']
    except KeyError:
        book['volumeInfo']['imageLinks'] = "#"

    # Adding of the this book to the database of the current user
    genres = ""
    if 'categories' in book['volumeInfo']:
        genres = book['volumeInfo']['categories'][0]
    authors = ""
    if 'authors' in book['volumeInfo']:
        authors = book['volumeInfo']['authors'][0]

    try:
        id = current_user.id  # Get the id of the current user
        user_to_update = Users.query.get_or_404(id)  # Get the reference to the current user
        user_genres = user_to_update.genres  # Get the already stored data in user's genre data
        if user_genres == None:
            user_genres = genres
        else:
            if len(user_genres) < 230:
                user_genres += f"-{genres}"
        user_to_update.genres = user_genres  # Add the new data to the already existing data

        # Similarly with the new author data
        user_authors = user_to_update.authors
        if user_authors == None:
            user_authors = authors
        else:
            if len(user_authors) < 230:
                user_authors += f"-{authors}"
        user_to_update.authors = user_authors

        db.session.commit()  # Commit the database changes
    
    except:  # If no user has logged in nothing needs to be done
        pass

    finally:
        
        # Finally the book's data needs to be verified

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


        # Search links for Amazon and Flipkart
        flipkart = f"https://www.flipkart.com/search?q={book_name}+{book['volumeInfo']['authors'][0]}"
        amazon = f"https://www.amazon.in/s?k={book_name}+{book['volumeInfo']['authors'][0]}"


        # Gets data for 15 more books of the same author
        similar_books_data = search_query(f"author:{authors}", 15)

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
                            id = id,
                            similar = similar_books_data['items'])


# Application's function for the recommendation system
@app.route("/recommend")
def recommend():
    '''Recommends a total of 40 books as per the user's viewing history.'''
    id = current_user.id
    user_data = Users.query.get_or_404(id)

    try:
        genre_data = user_data.genres.split('-')
        author_data = user_data.authors.split('-')

    except:  # When the user has not visited even a single book

        # Random authors and fiction genre is suggested
        authors = ["JK Rowling", "Stephen King", "Paulo Coelho",
                    "Suzanne Collins", "Rick Riordan", "Chetan Bhagat",
                   "Amish Tripathi", "Ernest Hemingway", "Agatha Christie"]
        data_genre = search_query("fiction", 10)
        data_author = search_query(f"author:{random.choice(authors)}", 10)
        data_author2 = search_query(f"author:{random.choice(authors)}", 10)

    else:
        # Else the top two most viwed author and the most viewed genre are selected
        most_common_author = max(set(author_data), key=author_data.count)
        for author in author_data:
            if author == most_common_author:
                author_data.remove(author)
        if len(author_data) > 0:
            most_common_author2 = max(set(author_data), key=author_data.count)
        else:
            most_common_author2 = ""

        most_common_genre = max(set(genre_data), key=genre_data.count)

        data_genre = search_query(f"subject:{most_common_genre}", 20)
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
    
    # Sorting of the recommendations according to the rating
    data = sorted(volumeInfos, key=lambda d: d['averageRating'], reverse=True) 

    return render_template('search.html', search = "Recommendation", data = data, len = len(volumeInfos))


# The app runs only if the program name is __main__ and not when this program is imported in anywhere else
if __name__ == "__main__":
    app.run(debug=True)

