# create category
def create(conn, data):
    print("ere")
    try:
        sql = "INSERT INTO Categories (Name) VALUES (?)"
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        print("success")
        return 1
    except:
        print("fail")
        return 0

# read category
def get_data(conn):
    try:
        sql = "SELECT CategoryID, Name FROM Categories"
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        return 0

# update category
def update(conn, data):
    try:
        sql = "UPDATE Categories SET Name = ? WHERE CategoryID = ?"
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        return 1
    except:
        return 0

# destory product
def destroy(conn, data):
    try:
        sql = "DELETE FROM Categories WHERE CategoryID = ?"
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        return 1
    except:
        return 0