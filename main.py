import json
import random
from xml.dom import ValidationErr
import requests
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
import os


def validate_search(form, field):
        if len(field.data) > 60:
            raise ValidationErr('Name must be less than 50 characters')
        
class SearchForm(FlaskForm):
    search = StringField(validators=[validate_search])
    # submit = SubmitField(label="")

def search_query(query, number_of_results):

    GOOGLE_BOOKS_ENDPOINT = "https://www.googleapis.com/books/v1/volumes"

    # GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")
    GOOGLE_BOOKS_API_KEY = "AIzaSyARgjRo6TXZl3Vk-yznmmwNHnOL3-0aS4c"
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
    # BESTSELLER_API_KEY = os.environ.get("BESTSELLER_API_KEY")
    BESTSELLER_API_KEY = "3RXXHOv35rDc4uoDVYHVOBnryX0r3f4V"

    params = {
        "api-key": BESTSELLER_API_KEY,
    }
    data = []
    response = requests.get(BESTSELLER_API_ENDPOINT, params=params)
    response.raise_for_status()
    data = response.json()['results']['lists']
    print(response.url)
    return data

app = Flask(__name__)

app.secret_key = "abcd"




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
            all_books = []
            for item in data['items']:
                all_books.append(item['volumeInfo']['title'])
                if 'imageLinks' not in item['volumeInfo']:
                    item['volumeInfo']['imageLinks'] = '#'
                if 'authors' not in item['volumeInfo']:
                    item['volumeInfo']['authors'] = '#'
            return render_template('search.html', search = query, data = data)
        else:
            return render_template('index.html', form=form)

@app.route("/<book_name>/<id>", methods=["GET"])
def get_book(book_name, id):
    data = search_query(id, 40)
    # try:
    #     image = data['items'][0]['volumeInfo']['imageLinks']['thumbnail']
    # except KeyError:
    #     data['items'][0]['volumeInfo']['imageLinks'] = "#"
    book = {}
    for item in data['items']:
        if item['volumeInfo']['title'] == book_name:
            book = item
            break
    try:
        image = book['volumeInfo']['imageLinks']['thumbnail']
    except KeyError:
        book['volumeInfo']['imageLinks'] = "#"

    authors=book['volumeInfo']['authors']

    try:
        genres = {"genre":book['volumeInfo']['categories'], "author":authors}
    except KeyError:
        genres = {'genre':""}

    try:
        with open("genres.json", "r") as file:
            genre_data = json.load(file)
    except FileNotFoundError:
        with open("genres.json", "w") as file:
            json.dump(genres, file, indent=4)
    else:
        for genre in genres['genre']:
            genre_data['genre'].append(genre)

    if 'author' in genres:
        for author in genres['author']:
            genre_data['author'].append(author)



        with open("genres.json", "w") as file:
            json.dump(genre_data, file, indent=4)

    hasAverageRating='averageRating' in book['volumeInfo']
    if not hasAverageRating:
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


    flipkart = f"https://www.flipkart.com/search?q={book_name}+{book['volumeInfo']['authors'][0]}"
    amazon = f"https://www.amazon.in/s?k={book_name}+{book['volumeInfo']['authors'][0]}"
    return render_template('book.html', 
                           book_name=book_name,  
                           amazon_link = amazon, 
                           flipkart_link=flipkart,
                           info=book['volumeInfo']['infoLink'],
                           thumbnail=thumbnail,
                           author=book['volumeInfo']['authors'][0],
                           year=book['volumeInfo']['publishedDate'].split('-')[0],
                           rating=book['volumeInfo']['averageRating'],
                           description=description )



@app.route("/recommend")
def recommend():
    try:
        with open("genres.json", "r") as file:
            genre_data = json.load(file)
            author_data = genre_data['author']
            genre_data = genre_data['genre']
           
    except FileNotFoundError:
        authors = ["JK Rowling", "Stephen King", "Paulo Coelho", "Suzanne Collins", "Rick Riordan", "Chetan Bhagat",
                   "Amish Tripathi", "Ernest Hemingway", "Agatha Christie"]
        data_genre = search_query("fiction", 10)
        data_author = search_query(f"author:{random.choice(authors)}", 10)
        data_author2 = search_query(f"author:{random.choice(authors)}", 10)

    else:
        most_common_authors = max(set(author_data), key=author_data.count)
        for author in author_data:
            if author == most_common_authors:
                author_data.remove(author)
        if len(author_data) > 0:
            most_common_author2 = max(set(author_data), key=author_data.count)
        else:
            most_common_author2 = ""

        most_common_genre = max(set(genre_data), key=genre_data.count)
        data_genre = search_query(f"subject:{most_common_genre}", 10)
        data_author = search_query(f"author:{most_common_authors}", 10)
        data_author2 = search_query(f"author:{most_common_author2}", 10)
    data = data_genre
    for item in data_author['items']:
        data['items'].append(item)
    for item in data_author2['items']:
        data['items'].append(item)
    random.shuffle(data['items'])
    return render_template('search.html', search = "Recommendation", data = data)


if __name__ == "__main__":
    app.run(debug=True)

