from flask import Flask, url_for, render_template, redirect

app = Flask(__name__)


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
    return render_template('inventory.html')


# current loans page
@app.route('/current')
def current():
    return render_template('current-loans.html')



app.run(debug=True)