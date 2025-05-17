from flask import Flask, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mutualfunds.db')

def get_db_data(category=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if category:
        cur.execute('SELECT * FROM stocks_by_fund WHERE category=?', (category,))
    else:
        cur.execute('SELECT * FROM stocks_by_fund')
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/small-cap')
def small_cap():
    data = get_db_data(category='small-cap')
    columns = data[0].keys() if data else []
    return render_template('index.html', data=data, columns=columns, title='Small Cap')

@app.route('/mid-cap')
def mid_cap():
    data = get_db_data(category='mid-cap')
    columns = data[0].keys() if data else []
    return render_template('index.html', data=data, columns=columns, title='Mid Cap')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
