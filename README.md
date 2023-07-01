# Lekhana
A web application that uses Google Books API to form a huge collection of books and recommendations similar to the user

## #--- DebugIT 2023 ---#

# Introduction: 

      A book recommendation platform that tracks the user's viewing history and recommends similar books to the user.
      This website creates a database of users and their preferences for books and accordingly recommends similar books to them.
      It also has a book-searching facility.
      

# Tech-Stack Used:

      -Python to create the functionality of the site including API requests, Database Management, and Flask Framework.
      
      -Flask(Python) to build up a framework to dynamically create pages for the website. Flask-Login is used for facilitating user management.
      
      -Google Books API & Books API(New York Times) to get data on the books searched and the books to be recommended. Also gets New York Times Bestsellers.
      
      -SQLAlchemy(Python-Flask) to create a database system to store the user's login details and also their book preferences.
      
      -HTML to build the templates which Flask uses for building up sites.
      
      -CSS/Bootstrap to give styling to the HTML framework and give the site a visual appeal.
      
      -JavaScript to control the simple events on the HTML webpage.
      
      -Render.com to deploy the web application.
      
# Features:

### Responsive
            The complete website is responsive, i.e., changes visuals as per the screen size of the user.
   ![Screenshot 2023-07-01 214723](https://github.com/kmtGryffindor20/Lekhana/assets/129510465/26e181d1-3268-431e-84fa-9182a478c896)


            
      
### Navigation Bar
            The navigation bar provides a quick way to move through different sections of the website.
         
### Book Searching
            The website uses Google Books API to search for the query entered in the search box provided.
            The search results are listed in descending order of their ratings on the Google Books API.
![Screenshot 2023-07-01 214850](https://github.com/kmtGryffindor20/Lekhana/assets/129510465/b4f7590e-1870-4b4f-856f-5a0858ac122d)

![Screenshot 2023-07-01 214952](https://github.com/kmtGryffindor20/Lekhana/assets/129510465/692ce798-9396-4970-a8cf-482c4493387b)

          
### Book Details
            Each book has a dynamically created details page that lists important details of the book.
            It also provides links to Amazon, Flipkart, and Google Books for the book.
            



https://github.com/kmtGryffindor20/Lekhana/assets/129510465/e0ffc761-3cca-49e1-9653-f1f839389b8a

            
            
            
            
### Trending Books
            The New York Times Books API gives the Latest Bestsellers of all categories.
            They are shown on the homepage as a slider giving slight details about them.
            The titles redirect to their Amazon buying link.
![Screenshot 2023-07-01 215925](https://github.com/kmtGryffindor20/Lekhana/assets/129510465/5f6dfd71-2831-4133-b995-a823afca6727)

            
### Recommendation System
            The recommendation system works by getting hold of the most viewed genre and the user's top two most regarded authors.
            It then gets the books for all these constraints, merges them together, and shows them in descending order of their rating.
             
![Screenshot 2023-07-01 220352](https://github.com/kmtGryffindor20/Lekhana/assets/129510465/035609b2-b7b9-460e-a5d4-be6b61a1e780)

            
            
### User Login System
            The website uses Flask-Login and SQLAlchemy to create a simple yet effective login system.
            It allows login for only registered users and users can sign up on the sign up page.
            The password also has constraints so that users don't enter an easily guessable password.
            
![Screenshot 2023-07-01 220517](https://github.com/kmtGryffindor20/Lekhana/assets/129510465/66c96e0a-bb51-4bb9-9945-a41b959ec607)
![Screenshot 2023-07-01 220651](https://github.com/kmtGryffindor20/Lekhana/assets/129510465/0b921885-e1ec-406a-a6be-92514b4de11f)

### Dark-Light Themes
            The Website has dark and light modes implemented.
            
![Screenshot 2023-07-01 220815](https://github.com/kmtGryffindor20/Lekhana/assets/129510465/1db354ef-75dd-454e-b1cd-e343fb1df0dc)




# Scopes and Improvements
      
      -The Recommendation System can be improved by applying better algorithms.
      
      -The user login system can be improved by making it more secure.
      
      -The design of the webpage can be worked upon to give it a more professional look.
      
      
# Video Demonstration
The Video Demo is of a previous version of the website. The website has been updated considerably since then.
[Video Demo](https://drive.google.com/file/d/1CtOfhOdtGUhZS130hzlSVk2444mobzn9/view?usp=share_link)
      

# Deployment Link
 

[Lekhana](https://lekhana.onrender.com/) 





      
