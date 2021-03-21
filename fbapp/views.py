import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    return render_template('index.html')
    
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
    return render_template('user.html', post=post)


@app.route('/inscription', methods=('GET', 'POST'))
def inscription():
    if request.method == 'POST':
        mail = request.form['mail']
        mot_de_passe = request.form['mot_de_passe']
        nom = request.form['nom']
        prenom = request.form['prenom']
        nationnalite = request.form['nationnalite']
        date_naiss = request.form['date_naiss']
        pays = request.form['pays']
        ville = request.form['ville']
        niveau_d_etude = request.form['niveau_d_etude']
        domaine_d_etude = request.form['domaine_d_etude']
        if not mail:
            flash('mail is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO utilisateurs (mail, mot_de_passe,nom, prenom, date_naiss,nationnalite, pays, ville, domaine_d_etude, niveau_d_etude) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)',
                         (mail, mot_de_passe,nom, prenom, date_naiss,nationnalite, pays, ville, domaine_d_etude, niveau_d_etude))
            conn.commit()
            conn.close()
            return redirect(url_for('connexion'))

    return render_template('inscription.html')