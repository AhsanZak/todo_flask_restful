from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("todos.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/todos", methods=["GET", "POST"])
def todos():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM todo")
        todos = [
            dict(id=row[0], title=row[1], status=row[2])
            for row in cursor.fetchall()
        ]
        if todos is not None:
            return jsonify(todos)

    if request.method == "POST":
        new_title = request.form["title"]
        new_status = request.form["status"]
        sql = """INSERT INTO todo (title, status)
                 VALUES (?, ?)"""
        cursor = cursor.execute(sql, (new_title, new_status))
        conn.commit()
        return f"Todo with the id: 0 created successfully", 201


@app.route("/todo/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_todo(id):
    conn = db_connection()
    cursor = conn.cursor()
    todo = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM todo WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            todo = r
        if todo is not None:
            return jsonify(todo), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        sql = """UPDATE todo
                SET title=?,
                    status=?,
                WHERE id=? """

        title = request.form["title"]
        status = request.form["status"]
        updated_todo = {
            "id": id,
            "title": title,
            "status": status,
        }
        conn.execute(sql, (title, status, id))
        conn.commit()
        return jsonify(updated_todo)

    if request.method == "DELETE":
        sql = """ DELETE FROM todo WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The todo with id: {} has been deleted.".format(id), 200


if __name__ == "__main__":
    app.run(debug=True)