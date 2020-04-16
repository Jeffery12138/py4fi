import sqlite3 as sq3
import os
import datetime
import numpy as np
# One SQL or relational database that is delivede with Python by default is SQLite3. With it,
# the basic Python approach to SQL databases can be easily illustrated

path = 'data/'
if not os.path.exists(path):
    os.makedirs(path)
query = 'CREATE TABLE numbs (Date date, No1 real, No2 real)'
# A SQL query that creates a table with three columns

con = sq3.connect(path+'numbs.db')
# Open a database connection; a file is created if it is not exist
con.execute(query)  # Execute the query
con.commit()  # ... and commits the changes.
q = con.execute  # Defines a short alias for the con.execute() method.
q('SELECT * FROM sqlite_master').fetchall()  # Fetches meta information about the database.
print(q('SELECT * FROM sqlite_master').fetchall())

#  Now that there is a database file with a table, this table can be populated with data.
#  Each row consists of a datetime object and two float objects

now = datetime.datetime.now()
q('INSERT INTO numbs VALUES(?, ?, ?)', (now, 0.12, 7.3))  # Writes a single row (or record) to the numbs table

np.random.seed(100)
data = np.random.standard_normal((10000, 2)).round(4)
print(data[:5])
for row in data:
    now = datetime.datetime.now()
    q('INSERT INTO numbs VALUES(?, ?, ?)', (now, row[0], row[1]))
con.commit()

q('SELECT * FROM numbs').fetchmany(4)
print(q('SELECT * FROM numbs').fetchmany(4))
print(q('SELECT * FROM numbs WHERE No1 > 0.5').fetchmany(4))
pointer = q('SELECT * FROM numbs')  # Defines a pointer object...
for i in range(3):
    print(pointer.fetchone())

rows = pointer.fetchall()
print(rows[:3])  # Retrieves all the remaining rows 抓取所有还没抓过的行
q('DROP TABLE IF EXISTS numbs')  # Removes the table from the database.
print(q('SELECT * FROM sqlite_master').fetchall())

con.close()