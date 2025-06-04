from flask import Flask, url_for, render_template, redirect
import sqlite3
import os

app = Flask(__name__)


# connects to database
def get_database_connection():
    # use app.instance_path to make path to database folder (very secure probably)
    db_path = os.path.join(app.instance_path, 'database.db')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # accesses rows by column name
    return conn


# landing page, currently redirects to inventory
@app.route('/')
def index():
    return redirect(url_for('inventory'))


# dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# lend / return page
@app.route('/lend')
def lend():
    return render_template('lend-return.html')


# inventory page
@app.route('/inventory')
def inventory():

    db = get_database_connection()
    cur = db.execute("SELECT * FROM inventory WHERE Barcode IS NOT NULL AND Barcode != ''")
    inventory = cur.fetchall()
    db.close()

    if not inventory:
        return "Inventory not found", 404

    return render_template('inventory.html', inventory=inventory)


# add item page
@app.route('/add-item')
def add_item():
    return render_template('add-item.html')


# current loans page
@app.route('/current')
def current():
    return render_template('current-loans.html')



app.run(debug=True)