import sqlite3

conn = sqlite3.connect("todos.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE todo (
    id integer PRIMARY KEY,
    title text NOT NULL,
    status text NOT NULL
)"""
cursor.execute(sql_query)