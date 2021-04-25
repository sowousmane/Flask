from flask import Flask, g, render_template, request, flash, url_for
import sqlite3

from werkzeug.utils import redirect

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('database.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    #Check if DB is there
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db

#close the connection to the database automatically
@app.teardown_appcontext
def close_db(error):
    #if global object has a sqlite database then close it. If u leave it open noone can access it and gets lost in memory causing leaks.
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connexion',methods=('GET', 'POST'))
def connexion():
    if request.method == 'POST' and request.form.get('essai') != 'update':

        email = request.form.get('email')
        mot_de_passe = request.form.get('pwd')
        db = get_db()
        cursor = db.execute('select id,mail, mot_de_passe, nom from utilisateurs')
        results = cursor.fetchall()
        for x in results:
            if x['mail'] == email and x['mot_de_passe'] == mot_de_passe:
                iduser=x['id']
                theUser=x['nom']
                #récuperer sa liste de sous formation et formation
                cursor = db.execute('select * from sous_formations where id_utilisateur=1 and id_formation =1')
                sous_formations1 = cursor.fetchall()

                # récuperer sa liste de sous formation et formation
                cursor = db.execute('select * from sous_formations where id_utilisateur=1 and id_formation =2')
                sous_formations2 = cursor.fetchall()

                cursor = db.execute('select * from formations where id_utilisateur=1')
                formations = cursor.fetchall()
                return render_template('user.html', user= theUser, sous_formations1=sous_formations1,sous_formations2=sous_formations2,
                                       formations=formations)

    if request.method == 'POST' and request.form.get('essai') == 'update':
        id_formation = request.form.get('id_formation')
        id_sous_formation = request.form.get('id_sous_formation')
        print(id_formation,id_sous_formation)
        db = get_db()
        theUser = 'Djanét'

        #mettre a jour la formation et la sous formation
        db.execute('update sous_formations set active = true where id=? and id_formation=?',(id_sous_formation,id_formation))
        db.commit()

        # récuperer sa liste de sous formation et formation
        cursor = db.execute('select * from sous_formations where id_utilisateur=1 and id_formation =1')
        sous_formations1 = cursor.fetchall()

        # récuperer sa liste de sous formation et formation
        cursor = db.execute('select * from sous_formations where id_utilisateur=1 and id_formation =2')
        sous_formations2 = cursor.fetchall()

        cursor = db.execute('select * from formations where id_utilisateur=1')
        formations = cursor.fetchall()
        return render_template('user.html', user=theUser, sous_formations1=sous_formations1,
                               sous_formations2=sous_formations2,
                               formations=formations)

    return render_template('connection.html')

@app.route('/users')
def viewusers():
    db = get_db()
    cursor = db.execute('select mail, mot_de_passe, nom from utilisateurs')
    results = cursor.fetchall()
    return f"<h1>The email is {results[0]['mail']}.<br> The password is {results[0]['mot_de_passe']}.<br> The name is {results[0]['nom']}.<br> size {len(results)} </h1>"

@app.route('/add')
def addusers():
    db = get_db()
    name = "test"
    age = 5
    db.execute('insert into people (name, age) values (?,?)',(name, age) )
    db.commit()
    db.close()

@app.route('/inscription', methods=('GET', 'POST'))
def inscription():
    if request.method == 'POST':
        email = request.form.get('email')
        mot_de_passe = request.form.get('pwd')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        nationnalite = request.form.get('nationnalite')
        date_naiss = request.form.get('date_naiss')
        pays = request.form.get('pays')
        ville = request.form.get('ville')
        niveau_d_etude = request.form.get('niveau_d_etude')
        domaine_d_etude = request.form.get('domaine_d_etude')
        print(email, mot_de_passe,nom, prenom, date_naiss,nationnalite, pays, ville, domaine_d_etude, niveau_d_etude)
        if not email:
            flash('mail is required!')
        else:
            conn = get_db()
            conn.execute('insert into utilisateurs ( mail, mot_de_passe,nom, prenom, date_naiss,nationnalite, pays, '
                         'ville, domaine_d_etude, niveau_d_etude) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)',
                         (email, mot_de_passe,nom, prenom, date_naiss,nationnalite, pays, ville, domaine_d_etude, niveau_d_etude))
            conn.commit()
            db = get_db()
            cursor = db.execute('select id,mail,nom,domaine_d_etude from utilisateurs')
            results = cursor.fetchall()
            for x in results:
                if x['mail'] == email and x['nom'] == nom:
                    userid = x['id']
                    if x['domaine_d_etude']=='Informatique':
                        # récuperer sa liste de sous formation et formation

                    # on ajoute les sous_formations pour cet utilisateur
                        conn.execute(
                        'insert into sous_formations ( titre, url_formation, description_formation, id_utilisateur, active, id_formation) VALUES (?,?,?,?,?,?)',
                        ('JAVA niveau 2 - intermédiaire',
                         'https://www.youtube.com/watch?v=2vvuGUxPv30&list=PLlxQJeQRaKDTCU85T7MTT8_YVfzLMtCKH&ab_channel=LESTEACHERSDUNET',
                         'Cette formation a pour but d avoir des competences java plus poussées', userid, False, 1))

                        conn.commit()

                        conn.execute(
                            'insert into sous_formations ( titre, url_formation, description_formation, id_utilisateur, active, id_formation) VALUES (?,?,?,?,?,?)',
                            ('PYTHON niveau 2 - intermédiaire',
                            'https://www.youtube.com/watch?v=LiBsVCXAgXI&ab_channel=FormationVid%C3%A9o',
                            'Cette formation a pour but d avoir des competences python plus poussées', userid, False, 2))
                        conn.commit()

                        # on ajoute les sous_formations pour cet utilisateur
                        conn.execute(
                            'insert into formations (titre, url_formation, description_formation, id_utilisateur, id_sous_formation) VALUES (?,?,?,?,?)',
                            ('JAVA niveau 1 - débutant',
                            'https://www.youtube.com/watch?v=fmJsqBWkXm4&list=PLlxQJeQRaKDRnvgIvfHTV6ZY8M2eurH95&ab_channel=LESTEACHERSDUNET',
                            'Cette formation a pour but d avoir des competences basiques en java', userid, 1))
                        conn.commit()


                        conn.execute(
                             'insert into formations (titre, url_formation, description_formation, id_utilisateur, id_sous_formation) VALUES (?,?,?,?,?)',
                            ('PYTHON niveau 1 - débutant',
                            'https://www.youtube.com/watch?v=oUJolR5bX6g&ab_channel=CodeAvecJonathan',
                            'Cette formation a pour but d avoir des competences basiques en python', userid, 2))
                        conn.commit()
                    if x['domaine_d_etude'] == 'Mathématiques':
                        # récuperer sa liste de sous formation et formation

                    # on ajoute les sous_formations pour cet utilisateur
                        conn.execute(
                                'insert into sous_formations ( titre, url_formation, description_formation, id_utilisateur, active, id_formation) VALUES (?,?,?,?,?,?)',
                                 ('Réussis ton bac de maths (édition Bac 2021)',
                                'https://www.udemy.com/course/reussis-ton-bac-de-maths-en-2-jours-edition-bac-s-2019/',
                                 'Plus de 120 questions corrigées (4 réponses possibles par question) pour réussir l épreuve !', userid, False, 3))

                        conn.commit()

                        conn.execute(
                                'insert into sous_formations ( titre, url_formation, description_formation, id_utilisateur, active, id_formation) VALUES (?,?,?,?,?,?)',
                                ('Cours de maths - Comprenez vraiment la trigonométrie !',
                                 'https://www.udemy.com/course/cours-de-maths-comprenez-vraiment-la-trigonometrie',
                                 'Comprenez en profondeur les maths avec la trigonométrie ! Entraînez-vous avec plus de 80 exercices.', userid, False, 4))
                        conn.commit()

                        conn.execute(
                            'insert into sous_formations ( titre, url_formation, description_formation, id_utilisateur, active, id_formation) VALUES (?,?,?,?,?,?)',
                            ('Cours de maths - Maîtrisez les bases de l analyse !',
                             'https://www.udemy.com/course/cours-de-maths-maitrisez-les-bases-de-lanalyse/',
                             'Comprenez en profondeur les fonctions en mathématiques ! Entraînez-vous avec plus de 60 exercices.',
                             userid, False, 4))
                        conn.commit()

                            # on ajoute les sous_formations pour cet utilisateur
                        conn.execute(
                                'insert into formations (titre, url_formation, description_formation, id_utilisateur, id_sous_formation) VALUES (?,?,?,?,?)',
                                ('Réussis ton bac de maths (édition Bac 2021)',
                                 'https://www.udemy.com/course/reussis-ton-bac-de-maths-en-2-jours-edition-bac-s-2019',
                                 'Plus de 120 questions corrigées (4 réponses possibles par question) pour réussir l épreuve !', userid, 3))
                        conn.commit()

                        conn.execute(
                                'insert into formations (titre, url_formation, description_formation, id_utilisateur, id_sous_formation) VALUES (?,?,?,?,?)',
                                ('Maîtrisez les bases des mathématiques !',
                                 'https://www.udemy.com/course/maitrisez-les-bases-des-mathematiques/',
                                 'Apprenez ou revisitez en profondeur les bases des maths et testez vous avec plus de 80 exercices corrigés.', userid, 4))
                        conn.commit()



            conn.close()
            return redirect(url_for('connexion'))

    return render_template('inscription.html')

if __name__ == '__main__':
    app.run(debug = True)