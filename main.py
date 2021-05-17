from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import random

app = Flask(__name__)


app.secret_key = 'abcd1234'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Avitanay213'
app.config['MYSQL_DB'] = 'bookstore'

# Intialize MySQL
mysql = MySQL(app)


@app.route('/bookstorelogin',methods=['GET', 'POST'])
def login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['id']
            session['manager'] = account['is_manager']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


@app.route('/bookstorelogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/bookstorelogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'name' in request.form and 'phone' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        phone = request.form['phone']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', username):
            msg = 'Invalid username!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not name or not phone:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user VALUES (%s, %s, %s, %s,0)', (username, password, name,phone))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))


    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/bookstorelogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session and session['manager'] == 0:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT ISBN,Title,Authors,Publisher,Language,Subject,Publication,Price FROM books')
        all = cursor.fetchall()
        return render_template('home.html', username=session['username'], all = all)

    if 'loggedin' in session and session['manager'] == 1:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM books')
        all = cursor.fetchall()
        return render_template('manager.html', username=session['username'], all = all)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/bookstorelogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = %s', (session['username'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/bookstorelogin/home/add', methods=['GET', 'POST'])
def Add():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'name' in request.form and 'phone' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        phone = request.form['phone']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', username):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not name or not phone:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            
            cursor.execute('INSERT INTO user VALUES (%s, %s, %s, %s,1)', (username, password, name,phone))
            mysql.connection.commit()
            msg = 'You have successfully added a manager!'
            return redirect(url_for('login'))
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('Add.html', msg=msg)

@app.route('/bookstorelogin/home/modify', methods=['GET', 'POST'])
def Modify():
    # Output message if something goes wrong...
    msg = ''
    # Check if "bookISBN" and "stock change" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'name' in request.form:

        msg = ''
        
        ISBN = request.form['username']
        Stock = request.form['name']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM books WHERE ISBN = %s ', (ISBN,))
        book = cursor.fetchone()

        if book:
            if not re.match(r'[0-9]+', Stock):
                msg = 'Stock level must contain only numbers!'

            if not re.match(r'[0-9]+', ISBN):
                msg = 'ISBN must contain only numbers!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE books SET Stock = %s WHERE ISBN = %s', (Stock,ISBN))
                mysql.connection.commit()
                msg = 'Successfully changed stock level'
                return render_template("modify.html",msg = msg)
        
        else:
            msg = 'No book with given ISBN'
        return render_template("modify.html",msg = msg)


        
        
        




        

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('modify.html', msg=msg)

@app.route('/bookstorelogin/Order',methods=['GET', 'POST'])
def Order():
    # Check if user is loggedin
    if 'loggedin' in session and session['manager'] == 0:
        # User is loggedin show them the home page
        if request.method == 'POST' and 'username' in request.form:
            Order_by = request.form['username']
            if( Order_by == 'ISBN'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT ISBN,Title,Authors,Publisher,Language,Subject,Publication,Price FROM books ORDER BY ISBN")
                all = cursor.fetchall()
                return render_template('Order.html', username=session['username'], all = all,  msg = 'Ordered by ISBN')
            elif ( Order_by == 'Title'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT ISBN,Title,Authors,Publisher,Language,Subject,Publication,Price FROM books ORDER BY Title")
                all = cursor.fetchall()
                return render_template('Order.html', username=session['username'], all = all,  msg = 'Ordered by Title')
            
            elif ( Order_by == 'Authors'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT ISBN,Title,Authors,Publisher,Language,Subject,Publication,Price FROM books ORDER BY Authors")
                all = cursor.fetchall()
                return render_template('Order.html', username=session['username'], all = all,  msg = 'Ordered by Authors')
            
            elif ( Order_by == 'Publisher'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT ISBN,Title,Authors,Publisher,Language,Subject,Publication,Price FROM books ORDER BY Publisher")
                all = cursor.fetchall()
                return render_template('Order.html', username=session['username'], all = all,  msg = 'Ordered by Publisher')
            
            elif ( Order_by == 'Language'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT ISBN,Title,Authors,Publisher,Language,Subject,Publication,Price FROM books ORDER BY Language")
                all = cursor.fetchall()
                return render_template('Order.html', username=session['username'], all = all,  msg = 'Ordered by Language')
            
            elif ( Order_by == 'Subject'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT ISBN,Title,Authors,Publisher,Language,Subject,Publication,Price FROM books ORDER BY Subject")
                all = cursor.fetchall()
                return render_template('Order.html', username=session['username'], all = all,  msg = 'Ordered by Subject')
            
            elif ( Order_by == 'Publication'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT ISBN,Title,Authors,Publisher,Language,Subject,Publication,Price FROM books ORDER BY Publication")
                all = cursor.fetchall()
                return render_template('Order.html', username=session['username'], all = all,  msg = 'Ordered by Publication')

            elif ( Order_by == 'Price'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT ISBN,Title,Authors,Publisher,Language,Subject,Publication,Price FROM books ORDER BY Price")
                all = cursor.fetchall()
                return render_template('Order.html', username=session['username'], all = all, msg = 'Ordered by Price')
            
            else:
                msg = 'Unsupported Order type'
                return render_template('Order.html', msg=msg)

    if 'loggedin' in session and session['manager'] == 1:
        if request.method == 'POST' and 'username' in request.form:

            Order_by = request.form['username']

            if( Order_by == 'ISBN'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM books ORDER BY ISBN")
                all = cursor.fetchall()
                return render_template('OrderM.html', username=session['username'], all = all,  msg = 'Ordered by ISBN')
            elif ( Order_by == 'Title'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM books ORDER BY Title")
                all = cursor.fetchall()
                return render_template('OrderM.html', username=session['username'], all = all,  msg = 'Ordered by Title')
            
            elif ( Order_by == 'Authors'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM books ORDER BY Authors")
                all = cursor.fetchall()
                return render_template('OrderM.html', username=session['username'], all = all,  msg = 'Ordered by Authors')
            
            elif ( Order_by == 'Publisher'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM books ORDER BY Publisher")
                all = cursor.fetchall()
                return render_template('OrderM.html', username=session['username'], all = all,  msg = 'Ordered by Publisher')
            
            elif ( Order_by == 'Language'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM books ORDER BY Language")
                all = cursor.fetchall()
                return render_template('OrderM.html', username=session['username'], all = all,  msg = 'Ordered by Language')
            
            elif ( Order_by == 'Subject'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM books ORDER BY Subject")
                all = cursor.fetchall()
                return render_template('OrderM.html', username=session['username'], all = all,  msg = 'Ordered by Subject')
            
            elif ( Order_by == 'Publication'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM books ORDER BY Publication")
                all = cursor.fetchall()
                return render_template('OrderM.html', username=session['username'], all = all,  msg = 'Ordered by Publication')

            elif ( Order_by == 'Price'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM books ORDER BY Price")
                all = cursor.fetchall()
                return render_template('OrderM.html', username=session['username'], all = all, msg = 'Ordered by Price')
            
            elif ( Order_by == 'Stock'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM books ORDER BY Stock")
                all = cursor.fetchall()
                return render_template('OrderM.html', username=session['username'], all = all, msg = 'Ordered by Stock')

            elif ( Order_by == 'copies_sold'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM books ORDER BY copies_sold")
                all = cursor.fetchall()
                return render_template('OrderM.html', username=session['username'], all = all, msg = 'Ordered by Copies sold')

            elif ( Order_by == 'Pages'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM books ORDER BY Pages")
                all = cursor.fetchall()
                return render_template('OrderM.html', username=session['username'], all = all, msg = 'Ordered by Pages')

            else:
                msg = 'Unsupported Order type'
                return render_template('OrderM.html', msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/bookstorelogin/home/addBooks', methods=['GET', 'POST'])
def addBooks():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'ISBN' in request.form and 'Title' in request.form and 'Author' in request.form and 'Publisher' in request.form and 'Language' in request.form and 'Subject' in request.form and 'Publication' in request.form and 'Stock' in request.form and 'Pages' in request.form and 'Price' in request.form:
        # Create variables for easy access
        ISBN = request.form['ISBN']
        Title = request.form['Title']
        Author = request.form['Author']
        Publisher = request.form['Publisher']
        Language = request.form['Language']
        Subject = request.form['Subject']
        Date = request.form['Publication']
        Stock = request.form['Stock']
        Pages = request.form['Pages']
        Price = request.form['Price']
        copies = 0

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM books WHERE ISBN = %s', (ISBN,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Book already exists!'
        elif not re.match(r'[0-9]+', ISBN):
            msg = 'Invalid ISBN!'
        elif not re.match(r'[A-Za-z]+', Language):
            msg = 'Language must contain letters only!'
        elif not re.match(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))',Date):
            msg = 'Date must be in YYYY-MM-DD format!'
        elif not re.match(r'[0-9]+', Stock):
            msg = 'Invalid Entry for stock level!'
        elif not re.match(r'[0-9]+', Pages):
            msg = 'Invalid Entry for Pages!'
        elif not re.match(r'^\s*(?=.*[1-9])\d*(?:\.\d{1,2})?\s*$', Price):
            msg = 'Invalid Entry for Price!'
        
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            
            cursor.execute('INSERT INTO books VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)', (ISBN, Title, Author,Publisher, Language, Subject, copies,Date,Pages,Stock,Price))
            mysql.connection.commit()
            msg = 'You have successfully added a Book!'
            return render_template('AddBooks.html', msg=msg)
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('AddBooks.html', msg=msg)


@app.route('/bookstorelogin/search',methods=['GET', 'POST'])
def Search():
    # Check if user is loggedin
    if 'loggedin' in session and session['manager'] == 0:
        # User is loggedin show them the home page
        if request.method == 'POST' and 'search' in request.form:

            name = request.form['search']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT ISBN,Title,Authors,Publisher,Language,Subject,Publication,Price FROM books WHERE Title LIKE %s OR Authors LIKE %s OR Publisher LIKE %s OR Language LIKE %s",('{}%'.format(name),'{}%'.format(name),'{}%'.format(name),'{}%'.format(name)))
            all = cursor.fetchall()
            return render_template('search.html', username=session['username'], all = all)
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please type book name to search'
            # Show registration form with message (if any)
            return render_template('home.html', msg=msg)

    if 'loggedin' in session and session['manager'] == 1:
        # User is loggedin show them the home page
        if request.method == 'POST' and 'search' in request.form:

            name = request.form['search']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM books WHERE Title LIKE %s OR Authors LIKE %s OR Publisher LIKE %s OR Language LIKE %s",('{}%'.format(name),'{}%'.format(name),'{}%'.format(name),'{}%'.format(name)))
            all = cursor.fetchall()
            return render_template('searchM.html', username=session['username'], all = all)
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please type anything to search'
            # Show registration form with message (if any)
            return render_template('manager.html', msg=msg)
    return redirect(url_for('login'))

@app.route('/bookstorelogin/comments',methods = ['POST','GET'])
def AddComment():
    if 'loggedin' in session and session['manager'] == 0:
        username = session['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT DISTINCT books.ISBN,Title FROM Orders,books WHERE books.ISBN = Orders.ISBN and  id = %s",(username,))
        all = cursor.fetchall()
        return render_template('comment.html',all = all)
    return redirect(url_for('login'))

@app.route('/bookstorelogin/commentcommit',methods = ['POST','GET'])
def commitComments():
    msg = ''
    if request.method == 'POST' and 'ISBN' in request.form and 'Rating' in request.form:
        username = session['username']
        ISBN = request.form['ISBN']
        description = request.form['Description']
        rating = request.form['Rating']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM comments WHERE ISBN = %s and id = %s', (ISBN,username))
        account = cursor.fetchone()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM books WHERE ISBN = %s ', (ISBN,))
        book = cursor.fetchone()

        if  book:
            if account:

                msg = 'You have already commented on this book'
            elif not re.match(r'[0-9]+', ISBN):
                msg = 'Invalid ISBN!'
            elif not re.match(r'^(?:[1-9]|0[1-9]|10)$', rating):
                msg = 'Invalid rating!'
            else:
                cursor.execute('INSERT INTO comments(ISBN,id,description,rating) VALUES (%s,%s,%s,%s)',(ISBN,username,description,rating))
                mysql.connection.commit()
                msg = 'You have successfully added a Comment!'
                return render_template('comment.html', msg=msg)
        else:
            msg = 'book with given ISBN does not exist'

        
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('comment.html', msg=msg)
        
@app.route('/bookstorelogin/showcomments',methods = ['POST','GET'])
def showComments():
    msg = ''
    if request.method == 'POST' and 'booksISBN' in request.form:

        commentISBN = request.form['booksISBN']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT Title,Authors,Publisher,description,rating,User.id FROM books,comments,User WHERE books.ISBN = comments.ISBN and User.id = comments.id and comments.ISBN = %s",(commentISBN,))
        all = cursor.fetchall()

        if all:
            return render_template('showComments.html', all =all)
        else:
            msg = 'No comments made by any user on this book'
    
    return render_template('showComments.html', msg=msg)

@app.route('/bookstorelogin/allusers', methods=['GET', 'POST'])
def showOtherUsers():
    msg = ''
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id,full_name FROM user Where is_manager = 0 and id != %s",(session['username'],))
        all = cursor.fetchall()

        if all:
            return render_template('Allusers.html',all = all)
        else:
            msg = 'No other users'

    return render_template('Allusers.html', msg=msg)

@app.route('/bookstorelogin/cart',methods = ['POST','GET'])
def addtocart():
    msg = ''
    if request.method == 'POST':
        ISBN = request.form['booksISBN']
        user = session['username']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM books WHERE ISBN = %s",(ISBN,))
        result = cursor.fetchone()

        if result['Stock'] == 0:
            msg = 'Out of Stock'
        elif result['Stock'] != 0:

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM cart WHERE ISBN = %s and id = %s",(ISBN,user))
            cartItem = cursor.fetchone()

            if cartItem:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("UPDATE cart SET Quantity = Quantity+1 WHERE ISBN = %s and id = %s",(ISBN,user))
                mysql.connection.commit()
                msg = 'Cart Updated'
                return render_template('cart.html',msg = msg)

            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("INSERT INTO cart(ISBN,id) VALUES(%s,%s)",(ISBN,user))
                mysql.connection.commit()
                msg = 'Added to Cart'
                return render_template('cart.html',msg = msg)

    return render_template("cart.html",msg = msg)

@app.route('/bookstorelogin/showcart',methods = ['POST','GET'])
def Cart():
    msg = ''
    user = session['username']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT books.ISBN,Title,Authors,Publisher,Quantity,Price FROM cart,books WHERE books.ISBN = cart.ISBN and id = %s",(user,))
    result = cursor.fetchall()

    if result:
        return render_template("cart.html", all = result)
    else:
        msg = "Cart is Empty"

    return render_template("cart.html", msg = msg)

@app.route('/bookstorelogin/deleteitem',methods = ['POST','GET'])
def deleteItem():

    user = session['username']
    ISBN = request.form['booksISBN']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM cart WHERE ISBN = %s and id = %s",(ISBN,user))
    mysql.connection.commit()
    msg = 'removed from cart'
    return render_template('cart.html',msg=msg)

@app.route('/bookstorelogin/checkout',methods = ['POST','GET'])
def checkout():
    msg = ''
    user = session['username']
    

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT books.ISBN,Quantity,Price FROM cart,books WHERE books.ISBN = cart.ISBN and id = %s",(user,))
    result = cursor.fetchall()

    length = len(result)
    
    if result:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO orders(ISBN,id,Paid,Items) SELECT books.ISBN,id,Price,Quantity FROM cart,books WHERE books.ISBN = cart.ISBN and id = %s ",(user,))
        mysql.connection.commit()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM cart WHERE id = %s",(user,))
        mysql.connection.commit()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT Items,ISBN FROM Orders Where id = %s ORDER BY orderId DESC LIMIT %s",(user,length))
        for row in cursor:
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE books SET Stock = Stock - %s ,copies_sold = copies_sold + %s WHERE ISBN = %s",(row['Items'],row['Items'],row['ISBN']))
            mysql.connection.commit()


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Orders WHERE id = %s ORDER BY orderId DESC",(user,))
        all = cursor.fetchall()

        return render_template('checkout.html',all = all)
    
    else:
        msg = 'Cart is empty'
    return render_template('cart.html',msg = msg)

@app.route('/bookstorelogin/Summary',methods = ['POST','GET'])
def Summary():
    msg = ''
    user = session['username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Orders WHERE id = %s ORDER BY orderId DESC",(user,))
    all = cursor.fetchall()

    if all:
        return render_template('Summary.html', all = all)
    else:
        msg = "No orders"
    return render_template('Summary.html',msg = msg)



        


if __name__ == '__main__':
    app.debug = True
    app.run()

