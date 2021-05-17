import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "xxxx",
    database = "bookstore"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE bookstore")

#mycursor.execute("CREATE TABLE User(id VARCHAR(20) NOT NULL PRIMARY KEY, password VARCHAR(20), full_name VARCHAR(40) NOT NULL, phone_number INTEGER(10) NOT NULL, is_manager INT DEFAULT 0)")
#mycursor.execute("CREATE TABLE books(ISBN VARCHAR(10) NOT NULL PRIMARY KEY, Title VARCHAR(30) NOT NULL, Authors VARCHAR(40) NOT NULL, Publisher VARCHAR(40) NOT NULL, Language VARCHAR(10) NOT NULL, Subject VARCHAR(10) NOT NULL, copies_sold INTEGER, Publication DATE NOT NULL, Pages INTEGER NOT NULL, Stock INTEGER NOT NULL, Price DECIMAL(6,2) NOT NULL) ")
#mycursor.execute("CREATE TABLE comments(commentID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,ISBN VARCHAR(10) NOT NULL , id VARCHAR(20) NOT NULL,description VARCHAR(10000), rating INTEGER NOT NULL, FOREIGN KEY (ISBN) REFERENCES books(ISBN) ON DELETE CASCADE, FOREIGN KEY (id) REFERENCES User(id) ON DELETE CASCADE)")
#mycursor.execute("CREATE TABLE cart(ISBN VARCHAR(10) NOT NULL, id VARCHAR(20) NOT NULL, Quantity INTEGER DEFAULT 1 NOT NULL, FOREIGN KEY (ISBN) REFERENCES books(ISBN), FOREIGN KEY (id) REFERENCES User(id)) ")
#mycursor.execute("CREATE TABLE Orders(orderId INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, ISBN VARCHAR(10) NOT NULL, id VARCHAR(20) NOT NULL, Paid DECIMAL(10,2) NOT NULL, Items INTEGER NOT NULL, FOREIGN KEY (ISBN) REFERENCES books(ISBN), FOREIGN KEY (id) REFERENCES User(id))")

mycursor.execute("Show Tables")

for x in mycursor:
    print(x)

