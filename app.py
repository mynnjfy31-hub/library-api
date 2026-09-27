from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, author TEXT NOT NULL, year INTEGER, category TEXT, total_copies INTEGER DEFAULT 1, available_copies INTEGER DEFAULT 1)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, phone TEXT, joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS loans (id INTEGER PRIMARY KEY AUTOINCREMENT, book_id INTEGER NOT NULL, member_id INTEGER NOT NULL, loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, due_date TIMESTAMP NOT NULL, return_date TIMESTAMP, status TEXT DEFAULT 'active', FOREIGN KEY (book_id) REFERENCES books(id), FOREIGN KEY (member_id) REFERENCES members(id))''')
    conn.commit()
    conn.close()

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO books (title, author, year, category, total_copies, available_copies) VALUES (?, ?, ?, ?, ?, ?)',
                (data['title'], data['author'], data.get('year'), data.get('category'), data.get('total_copies', 1), data.get('total_copies', 1)))
    db.commit()
    book_id = cur.lastrowid
    db.close()
    return jsonify({"id": book_id, "message": "کتاب اضافه شد"}), 201

@app.route('/api/books', methods=['GET'])
def get_books():
    db = get_db()
    books = db.execute('SELECT * FROM books').fetchall()
    db.close()
    return jsonify([dict(b) for b in books])

@app.route('/api/loans', methods=['POST'])
def create_loan():
    data = request.get_json()
    db = get_db()
    due_date = datetime.datetime.now() + datetime.timedelta(days=data.get('days', 7))
    cur = db.cursor()
    cur.execute('INSERT INTO loans (book_id, member_id, due_date) VALUES (?, ?, ?)',
                (data['book_id'], data['member_id'], due_date))
    db.commit()
    db.close()
    return jsonify({"message": "امانت ثبت شد"}), 201

@app.route('/', methods=['GET'])
def home():
    return 'سلام! API کتابخانه فعال است.'

if __name__ == '__main__':
    create_db()
    app.run(host='0.0.0.0', port=5000)