from flask import Flask, url_for, render_template, redirect, request, flash
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

    conn = get_database_connection()
    cur = conn.execute("SELECT * FROM inventory WHERE Barcode IS NOT NULL AND Barcode != ''")
    inventory = cur.fetchall()
    inventory_count = len(inventory)
    conn.close()

    if not inventory:
        return "Inventory not found", 404

    return render_template('inventory.html', inventory=inventory, inventory_count=inventory_count)

@app.route('/search')
def search():
    query = request.args.get('query', '')

    conn = get_database_connection()

    if query:
        # Use parameterized query to prevent SQL injection
        cur = conn.execute("""
            SELECT * FROM inventory
            WHERE Barcode IS NOT NULL AND Barcode != ''
            AND (
                Model LIKE ? OR
                Brand LIKE ? OR
                Item LIKE ? OR
                Type LIKE ? OR
                Barcode LIKE ?
            )
        """, [f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'])
    else:
        cur = conn.execute("SELECT * FROM inventory WHERE Barcode IS NOT NULL AND Barcode != ''")

    inventory = cur.fetchall()
    inventory_count = len(inventory)
    conn.close()

    return render_template('inventory.html', inventory=inventory, inventory_count=inventory_count)


# add item page
@app.route('/add-item', methods=["GET"])
def add_item_page():
    return render_template('add-item.html')


# add item logic
@app.route('/add-item', methods=["POST"])
def add_item():

    # get input data from html
    item = request.form['Item']
    item_type = request.form['Type']
    brand = request.form['Brand']
    model = request.form['Model']
    colour = request.form['Colour']
    connectivity = request.form['Connectivity']
    strings = request.form['Strings']
    handedness = request.form['Handedness']
    barcode = request.form['Barcode']

    # get db connection
    conn = get_database_connection()
    cursor = conn.cursor()

    # check if barcode already
    cursor.execute("SELECT 1 FROM inventory WHERE Barcode = ?", (barcode,))
    if cursor.fetchone():
        print("An item with this barcode already exists.")
        return redirect(url_for('add_item'))
    
    # insert new item
    cursor.execute("""
    INSERT INTO inventory (Item, Type, Brand, Model, Colour, Connectivity, Strings, Handedness, Barcode)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (item, item_type, brand, model, colour, connectivity, strings, handedness, barcode))

    conn.commit()
    conn.close()

    print("Item successfully added!")

    return redirect(url_for('inventory'))


@app.route('/delete_items', methods=['POST'])
def delete_items():
    
    selected_ids = request.form.getlist('selected_items')  # retrieved as string ids

    # test to print selected ids
    if selected_ids:
        print("Deleting selected IDs:", selected_ids)

        conn = get_database_connection()
        cursor = conn.cursor()

        # Manual string join (not recommended in production)
        id_list = ','.join(selected_ids)  # Unsafe if IDs aren't sanitized
        query = f"DELETE FROM inventory WHERE id IN ({id_list})"
        cursor.execute(query)

        conn.commit()
        conn.close()
    
    return redirect(url_for('inventory'))


@app.route('/lend_return')
def lend_return_page():
    return render_template("lend-return.html")

@app.route('/lend_return')
def lend_return():
    barcode = request.form['barcode']

    # looks to see if barcode is already in current loans table

    # if it is, marks item as returned and available, renders page that says successfully returned

    # if not, renders page to make new loan

 

# current loans page
@app.route('/current')
def current():
    return render_template('current-loans.html')



app.run(debug=True)