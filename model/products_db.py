
# get product
def get_data(conn):
    sql = "SELECT ProductID, Products.Name, Quantity, Categories.Name FROM Products INNER JOIN Categories ON Products.CategoryID=Categories.CategoryID"
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

# create product
def create(conn, data):
    try:
        sql = "INSERT INTO Products (Name, Quantity, CategoryID) VALUES (?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        print("Success")
        return 1
    except:
        print("Fail")
        return 0

# destory product
def destroy(conn, data):
    try:
        sql = "DELETE FROM Products WHERE ProductID = ?"
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        return 1
    except:
        return 0