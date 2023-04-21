# Lekhana
A web application that uses Google Books API to form a huge collection of books and recommends similar to the user

## #--- DebugIT 2023 ---#

# Introduction: 

      A book recommnedation platform that tracks the user's viewing history and recommends similar books to the user.
      This website creates a database of users and their preferences of books and accordingly recommends similar books to them.
      It also has a book searching facility.
      

# Tech-Stack Used:

      -Python to create the functionality of the site including API requests, Database Management, and Flask Framework.
      
      -Flask(Python) to build up a framework to dynamically create pages for the website. Flask-Login is used for facilitating user management.
      
      -Google Books API & Books API(New York Times) to get data of the books searched and the books to be recommended. Also gets New York Times Bestsellers.
      
      -SQLAlchemy(Python-Flask) to create a database system to store the user's login details and also their book preferences.
      
      -HTML to build the templates which Flask uses for building up sites.
      
      -CSS to give styling to the HTML framework and give the site a visual appeal.
      
      -JavaScript to control the simple events on the HTML webpage.
      
      -Render.com to deploy the web application.
      
# Features:

### Responsive
            The complete website is responsive, i.e, changes visuals as per the screen size of the user.
   ![Screenshot 2023-04-17 015802](https://user-images.githubusercontent.com/129510465/232340302-935305fb-4c77-4d44-9b32-d38a176627ff.png)

            
      
### Navigation Bar
            The navigation bar provides a quick way to move through different sections of the website.
         
### Book Searching
            The website uses Google Books API to search for the query entered in the search box provided.
            The search results are listed in descending order of their ratings on the Google Books API.
![1](https://user-images.githubusercontent.com/129510465/232381382-2cd316ac-9b25-49de-a86a-00929ee185d0.png)
![2](https://user-images.githubusercontent.com/129510465/232339734-7313a8c5-7fb3-4af1-a910-ffe6f115a797.png)

          
### Book Details
            Each book has a dynamically created details page which lists important details of the book.
            It also provides links to Amazon, Flipkart and Google Books for the book.
            
   ![Screenshot 2023-04-17 015601](https://user-images.githubusercontent.com/129510465/232340209-b3f1e300-648b-49d2-9a4e-e5482bdbaed1.png)

            
            
            
            
### Trending Books
            The New York Times Books API gives the Latest Bestsellers of all categories.
            They are shown at the homepage as a slider giving slight details about them.
            The titles redirect to their Amazon buying link.
   ![](https://user-images.githubusercontent.com/129510465/232339741-d3d03dcf-9cf5-4838-b76d-c0f883cc633f.png)

            
### Recommendation System
            The recommendation system works by getting hold of the most viewed genre and the top two most viewed authors by the user.
            It then gets the books for all these constraints, merges them together and shows them in descending order of their rating.
             
   ![Screenshot 2023-04-17 015457](https://user-images.githubusercontent.com/129510465/232340141-3fbd7fbf-3a4b-44c6-bbb6-e0d39ddc1769.png)

            
            
### User Login System
            The website uses Flask-Login and SQLAlchemy together to create a simple yet effective login system.
            It allows login for only registered users and users can sign up on the sign up page.
            The password also has constraints so that users don't enter easily guessable password.
            Since the website is deployed on a free plan on Render.com, the server restarts the app
            clearing all details after some time of inactivity. So the user will face problem in 
            Logging in. 
            
   ![Screenshot 2023-04-17 014944](https://user-images.githubusercontent.com/129510465/232339884-83a12200-ec28-4319-9503-212833fc320f.png)            

![Screenshot 2023-04-17 015320](https://user-images.githubusercontent.com/129510465/232340073-74067f31-a8cd-4736-8b16-f9cb4f2d4a34.png)



# Scopes and Improvements
      
      -The Recommendation System can be improved by applying better algorithms.
      
      -The user login system can be improved by making it more secure.
      
      -The design of the webpage can be worked upon to give it a more proffessional look.
      
      
# Video Demonstration
[Video Demo](https://drive.google.com/file/d/1CtOfhOdtGUhZS130hzlSVk2444mobzn9/view?usp=share_link)
      

# Deployment Link


Since the website is deployed on a free plan on Render.com, the server restarts the app clearing all details after some time of inactivity. It may also sometimes get server error on the hosting site. 

[Lekhana](https://lekhana.onrender.com/) 





      
