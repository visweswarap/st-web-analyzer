import json
from flask import Flask, render_template, redirect, url_for, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mutualfunds.db')

def get_db_data(category=None, limit=None, offset=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        query = 'SELECT * FROM stocks_by_fund '
        params = []
        if category:
            query += ' WHERE category=?'
            params.append(category)
        query += ' ORDER BY fund_name'
        if limit is not None and offset is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])
        cur.execute(query, params)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        rows = []
    except Exception as e:
        print(f"General error: {e}")
        rows = []
    finally:
        conn.close()
    if rows:
        result = [dict(row) for row in rows]
    return result

def get_total_count(category=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if category:
        cur.execute('SELECT COUNT(*) FROM stocks_by_fund WHERE category=?', (category,))
    else:
        cur.execute('SELECT COUNT(*) FROM stocks_by_fund')
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_all_fund_names():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT fund_name FROM stocks_by_fund ORDER BY fund_name')
    fund_names = [row[0].strip() for row in cur.fetchall()]
    conn.close()
    return fund_names

def get_fund_names_by_category(category=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if category:
        cur.execute('SELECT DISTINCT fund_name FROM stocks_by_fund WHERE category=? ORDER BY fund_name', (category,))
    else:
        cur.execute('SELECT DISTINCT fund_name FROM stocks_by_fund ORDER BY fund_name')
    fund_names = [row[0].strip() for row in cur.fetchall()]
    conn.close()
    return fund_names

def get_sector_names_by_category(category=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if category:
        cur.execute('SELECT DISTINCT sector FROM stocks_by_fund WHERE category=? ORDER BY sector', (category,))
    else:
        cur.execute('SELECT DISTINCT sector FROM stocks_by_fund ORDER BY sector')
    sector_names = [row[0].strip() for row in cur.fetchall() if row[0]]
    conn.close()
    return sector_names

def get_stock_names_by_category(category=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if category:
        cur.execute('SELECT DISTINCT stock_invested_in FROM stocks_by_fund WHERE category=? ORDER BY stock_invested_in', (category,))
    else:
        cur.execute('SELECT DISTINCT stock_invested_in FROM stocks_by_fund ORDER BY stock_invested_in')
    stock_names = [row[0].strip() for row in cur.fetchall() if row[0]]
    conn.close()
    return stock_names

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/all-funds')
def all_funds():
    # Your data - could come from database, API, CSV, etc.
    portfolio_data = [
        {
            "id": 3841,
            "fund_name": "HDFC Mid-Cap Opportunities Fund - Direct Plan - Growth",
            "stock_invested_in": "Max Financial Services Ltd.",
            "sector": "Life insurance",
            "one_m_change": 0.41,
            "quantity": 25500000.00,
            "one_m_change_in_qty": 0.0,
            "portfolio_date": "2025-04-30"
        },
        # ... more data
    ]
    result = []
    for item in get_db_data():
        result.append({
            "id": item["id"],
            "fund_name": item["fund_name"],
            "stock_invested_in": item["Stock_Invested_in"],
            "sector": item["Sector"],
            "one_m_change": item["one_m_change"],
            "quantity": item["Quantity"],
            "one_m_change_in_qty": item["one_m_change_in_qty"],
            "portfolio_date": item["portfolio_date"],
            "category": item["category"]
        })
    portfolio_data = result
    
    return render_template('master2.html', title='All Funds', 
                         portfolio_data=json.dumps(portfolio_data),
                         total_records=len(portfolio_data))

@app.route('/small-cap')
def small_cap():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    data = get_db_data(category='small-cap', limit=per_page, offset=offset)
    columns = data[0].keys() if data else []
    total = get_total_count(category='small-cap')
    has_prev = page > 1
    has_next = offset + per_page < total
    fund_names = get_fund_names_by_category('small-cap')
    sector_names = get_sector_names_by_category('small-cap')
    stock_names = get_stock_names_by_category('small-cap')
    return render_template('index.html', data=data, columns=columns, title='Small Cap', page=page, has_prev=has_prev, has_next=has_next, fund_names=fund_names, sector_names=sector_names, stock_names=stock_names)

@app.route('/mid-cap')
def mid_cap():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    data = get_db_data(category='mid-cap', limit=per_page, offset=offset)
    columns = data[0].keys() if data else []
    total = get_total_count(category='mid-cap')
    has_prev = page > 1
    has_next = offset + per_page < total
    fund_names = get_fund_names_by_category('mid-cap')
    sector_names = get_sector_names_by_category('mid-cap')
    stock_names = get_stock_names_by_category('mid-cap')
    return render_template('index.html', data=data, columns=columns, title='Mid Cap', page=page, has_prev=has_prev, has_next=has_next, fund_names=fund_names, sector_names=sector_names, stock_names=stock_names)

@app.route('/midcap-table')
def midcap_table():
    data = get_db_data(category='mid-cap')
    return render_template('midcap.html', data=data, title='Mid Cap Funds')

@app.route('/query-pannel')
def query_pannel():
    result = []
    for item in get_db_data():
        result.append({
            "id": item["id"],
            "fund_name": item["fund_name"],
            "stock_invested_in": item["Stock_Invested_in"],
            "sector": item["Sector"],
            "one_m_change": item["one_m_change"],
            "quantity": item["Quantity"],
            "one_m_change_in_qty": item["one_m_change_in_qty"],
            "portfolio_date": item["portfolio_date"],
            "category": item["category"]
        })
    portfolio_data = result
    return render_template('querypannel.html', title='Query Panel', portfolio_data=json.dumps(portfolio_data), total_records=len(portfolio_data))

@app.route('/run-sql-query', methods=['POST'])
def run_sql_query():
    data = request.get_json()
    query = data.get('query', '').strip()
    if not query.lower().startswith('select'):
        return jsonify({'success': False, 'error': 'Only SELECT queries are allowed.'})
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        result_rows = [dict(row) for row in rows]
        return jsonify({'success': True, 'columns': columns, 'rows': result_rows})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(port=5001, debug=True)
