from flask import Flask, g, render_template, request, redirect, url_for , session , flash
import sqlite3
from flask_session import Session

app = Flask(__name__)

app.secret_key = "Sandeepbay@9"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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

@app.route('/edit/<int:id>' , methods=["GET" , "POST"])
def edit_expense(id):
    db = get_db()
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]

        db.execute(
            'UPDATE Expenses SET amount = ? , category = ?, date = ? where id = ?',
            (amount , category , date , id)
        )
        db.commit()
        return redirect(url_for('view_expenses'))
    expense = db.execute(
        'SELECT * FROM Expenses where id = ?',
        (id,)
    ).fetchone()
    return render_template('edit_expenses.html' , expense = expense)

@app.route('/delete/<int:id>' , methods=["GET"])
def delete_expense(id):
    db = get_db()
    db.execute('DELETE FROM Expenses where id = ?' , (id,))
    db.commit()
    return redirect(url_for('view_expenses'))

@app.route('/register' , methods=["GET" , "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            db.execute('INSERT INTO Users (username , password) VALUES (? , ?)' , (username , password))
            db.commit()
            flash("Registraion successfull! Please Log in" , "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists! Please choose another!' , 'danger')
    return render_template('register.html')

@app.route('/login' , methods=["GET" , "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM Users where username = ? AND password = ?' , (username , password)).fetchone()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash("Login Successful" , "success")
            return redirect(url_for('view_expenses'))
        else:
            flash("Invalid username or password" , 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been successfully logged out" , 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)