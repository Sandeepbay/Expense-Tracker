import sqlite3

connection = sqlite3.connect('expenses.db')

cursor = connection.cursor()

# Creating the Users Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users     (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL         
    )
''')

# Creating the Expense Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(id)
    )
''')

connection.commit()
connection.close()

print("Database and tables created successfully")