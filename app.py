from flask import Flask, render_template, request, redirect
import sqlite3
from db import init_db

app = Flask(__name__)
init_db()

def get_db():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    expenses = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("index.html", expenses=expenses)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]

        conn = get_db()
        conn.execute("INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)",
                     (title, amount, category))
        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("add.html")

@app.route("/dashboard")
def dashboard():
    conn = get_db()

    total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0

    category_data = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        GROUP BY category
    """).fetchall()

    conn.close()

    return render_template("dashboard.html", total=total, category_data=category_data)

if __name__ == "__main__":
    app.run(debug=True)