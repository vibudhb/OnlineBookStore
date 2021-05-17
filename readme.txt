HOW TO DEPLOY

First Install the following packages using pip
pip install flask
pip install mysql-connector-python
pip install flask-mysqldb

Make sure you have MySQL installed
Open database.py
change host to your local host
change user to your user in mysql
change password to your mysql password

create a database using cursor.execute("CREATE DATABASE bookstore")

then in connection select database to be the database you created

Now Run all the commented database.py commands

After successfully Creating databases from database.py

run main.py

Go to http://127.0.0.1:5000/bookstorelogin in your web browser

**1) For registering you have to use an email address there's a regex which specially checks if the user who's trying to register is using an email or not
**2) ISBN has to be All numbers
**3) Publication Date (mentioned as Publication in books table) in books has to be in YYYY-MM-DD format otherwise it would fail
**4)Customer can only add comments on the books which they have ordered
**5) Rating in add a comment section of customer has to be between 1-10 would display "invalid rating" message if entered random number
**6) Customers can view all registeres customers except him/her in the profile page after clicking All registered customers button
**7) Clicking the ISBN button of respective books in home page leads to comments on made on that book
**8) Similarly clicking button under add to cart label in home page adds that particular book to cart, clicking again for same book would result in quantity being increased in cart
**9) Checkout works for different books as well, as soon as clicking checkout stock level of the books ordered will go down by desired amount and consequently number of copies sold would go up. Furthermore, the cart will be cleared
**10) Successful addition of manager from manager dashboard would lead back to login page
**11) You have to enter a super-user i.e a manager beforehand to access manager dashboard (is_manager = 1 for manager in user table)
**12) ORDER BY only works for "ISBN","Authors","Title","Publisher","Language","Subject","Publication" for customer and all attribute in books table for manager (same for search)


