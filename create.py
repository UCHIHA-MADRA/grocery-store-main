import sqlite3

sql = """
CREATE TABLE Orders (
	OrderID	    INTEGER,
	UserID 	    INTEGER NOT NULL,
	Quantity	INTEGER NOT NULL,
	Date	    TEXT NOT NULL,
	ProductID	INTEGER NOT NULL,
	Status	    INTEGER NOT NULL,
	PRIMARY KEY (OrderID)
)
"""


conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute(sql)
conn.commit()
cursor.close()