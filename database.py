import sqlite3

def connect_db():
    connection = sqlite3.connect("crest_bank.db")
    return connection

def create_table():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_transaction(day, amount, transaction_type):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions (day, amount, type)
        VALUES (?, ?, ?)
    """, (day, amount, transaction_type))

    connection.commit()
    connection.close()

def get_transactions():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM transactions")

    transactions = cursor.fetchall()

    connection.close()

    return transactions

