# read operation
def exists(conn, data):
    # check if user exists
    sql = "SELECT UserID FROM Users WHERE Username = ? AND Password = ?"
    cursor = conn.cursor()
    cursor.execute(sql, data)
    record = cursor.fetchone()
    cursor.close()
    print(record)
    return record

# create operation for user table (insert record)
def register(conn, data):
    try:
        sql = "INSERT INTO Users (Name, Username, Password, AccountType) VALUES(?,?,?,?)"
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        sql = "SELECT last_insert_rowid()"
        cur.execute(sql)
        result = cur.fetchone()
        return result[0]
    except:
        return 0

def get_data(conn, uid):
    sql = "SELECT Name, Username, Password, AccountType FROM Users WHERE UserID = ?"
    cursor = conn.cursor()
    cursor.execute(sql, (uid,))
    record = cursor.fetchone()
    cursor.close()
    print("rec:", record)
    return record