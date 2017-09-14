from flask import Flask, render_template, redirect, request, g
import sqlite3
import uuid

# database info

DATABASE = 'data.db'

# our queries
SELECT_TABLE_LISTINGS = """select * from listings;"""
CREATE_TABLE_LISTINGS = """create table listings (title text, description text,
                            lid varchar(20), primary key (lid));"""
INSERT_TABLE_LISTINGS = """insert into listings values (?, ?, ?)"""

def query_db(query, one=False):
    cur = get_db().cursor.execute(query)
    cur.close()
    return cur.fetchall()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = DBManager()
        setattr(g, '_database', db)
    return db

class DBManager(object):
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()

    def close(self):
        # cursor clean? TODO
        self.conn.close()

    def get_listings(self):
        res = []
        # replace w/ query_db? TODO
        for row in self.conn.execute(SELECT_TABLE_LISTINGS):
            res.append(row)
        return res

    def create_listing(self, l):
        # where l is a dict
        title = l['title']
        desc = l['desc']
        self.cursor.execute('insert into listings values (?, ?, ?)', (title, desc, str(uuid.uuid4())))
        self.conn.commit()

    def delete_listing(self, lid):
        pass

    def update_listing(self):
        pass

# ----

app = Flask(__name__)

# our DB

@app.teardown_appcontext
def close_connection(exception):
    db = get_db()
    db.close()

# our routing

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# password only from now on

@app.route('/listings')
def read():
    # check if there's a session in place
    db = get_db()
    listings = db.get_listings()
    return render_template('read.html', listings=listings)

@app.route('/listings/create')
def create():
    return render_template('create.html')

@app.route('/listings/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        db = get_db()
        db.create_listing({'title': title, 'desc': desc})
    return render_template('success.html')

@app.route('/listings/edit/<listing_id>')
def edit(listing_id):
    return render_template('edit.html')

@app.route('/listings/view/<listing_id>')
def read_item(listing_id):
    return render_template('read_item.html')
