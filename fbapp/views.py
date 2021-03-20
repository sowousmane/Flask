import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/inscription')    
def inscription():
    return render_template('inscription.html')

@app.route('/connexion')    
def connexion():
    return render_template('connection.html')

@app.route('/user')    
def user(): 
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM utilisateurs').fetchall()
    conn.close()
    return render_template('user.html', posts=posts)



def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM utilisateurs WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('inscription.html')
