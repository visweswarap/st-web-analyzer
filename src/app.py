from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mutualfunds.db')

def get_db_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM stocks_by_fund')
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    data = get_db_data()
    columns = data[0].keys() if data else []
    return render_template('index.html', data=data, columns=columns)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
