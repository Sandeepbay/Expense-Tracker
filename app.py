from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'expenses.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # To return rows as dictionaries
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return redirect(url_for('add_expense'))

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        # Get form data
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']

        # Insert into database
        db = get_db()
        db.execute(
            'INSERT INTO Expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)',
            (1, amount, category, date)  # Assuming user_id=1 for now
        )
        db.commit()

        return redirect(url_for('view_expenses'))

    return render_template('add_expense.html')

@app.route('/view')
def view_expenses():
    db = get_db()
    expenses = db.execute(
        'SELECT * FROM Expenses WHERE user_id = ?',
        (1,)  # Assuming user_id=1 for now
    ).fetchall()
    return render_template('view_expenses.html', expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)