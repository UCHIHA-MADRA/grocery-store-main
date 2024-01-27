# OrderID INT(6) UNSIGNED AUTO INCREMENT (PRIMARY KEY)
# UserID INT(6) FOREIGN KEY REFERENCES User Table

sql = """

CREATE TABLE Orders (
	OrderID	    INTEGER,
	UserID 	    INTEGER NOT NULL,
	Quantity	INTEGER NOT NULL,
	Date	    TEXT NOT NULL,
	ProductID	INTEGER NOT NULL,
	Status"	    INTEGER NOT NULL,
	PRIMARY     KEY("OrderID" AUTOINCREMENT)
);

"""

# create
def create(conn, data):
    try:
        sql = "INSERT INTO Orders (UserID, ProductID, Quantity, Date, Status) VALUE (?, ?, ?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        print("Success")
        return 1
    except:
        print("Fail")
        return 0

# read
def get_data(conn):
    try:
        sql = """
        SELECT Users.Name, Products.Name, Categories.Name, Orders.Quantity, Orders.Date
        FROM Orders
        INNER JOIN Users
        ON Users.UserID = Orders.UserID
        INNER JOIN Products
        ON Products.ProductID = Orders.ProductID
        INNER JOIN Categories
        ON Products.CategoryID = Categories.CategoryID
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        print('success')
        return results

    except:
        print('fail')
        return 0

def get_data_user(conn, data):
    try:
        sql = """
        SELECT Users.Name, Products.Name, Categories.Name, Orders.Quantity, Orders.Date
        FROM Orders
        INNER JOIN Users
        ON Users.UserID = Orders.UserID
        INNER JOIN Products
        ON Products.ProductID = Orders.ProductID
        INNER JOIN Categories
        ON Products.CategoryID = Categories.CategoryID
        WHERE Orders.UserID = ?
        """
        cursor = conn.cursor()
        cursor.execute(sql, data)
        results = cursor.fetchall()
        print('success')
        return results
    except:
        print('fail')
        return 0

#update
def update(conn, data):
    try:
        sql = "UPDATE Orders SET Status = 1 WHERE UserID = ?"
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        print("Success")
        return 1
    except:
        print("Fail")
        return 0

# delete
def destroy(conn, data):
    try:
        sql = "DELETE FROM Orders WHERE OrderID = ?"
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        print("Success")
        return 1
    except:
        print("Fail")
        return 0

