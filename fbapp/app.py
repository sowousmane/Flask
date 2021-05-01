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
        print("nbr user : ", len(results))
        for x in results:
            if x['mail'] == email and x['mot_de_passe'] == mot_de_passe:
                print("USER CURRENT : ",x['mail'])
                iduser=x['id']
                theUser=x['nom']
                print('ID USER', iduser)
                #récuperer sa liste de sous formation et formation
                cursor = db.execute('select * from sous_formations where id_utilisateur=? and type_sous_formation=?', (iduser,'soft'))
                sous_formations = cursor.fetchall()

                cursor = db.execute('select * from sous_formations where id_utilisateur=? and type_sous_formation=?',
                                    (iduser, 'hard'))
                sous_formations_hard = cursor.fetchall()
                print("nbr sous formation de user 2 : ", len(sous_formations))
                cursor = db.execute('select * from formations where id_utilisateur=? and type_formation=?',(iduser,'soft'))
                formations = cursor.fetchall()
                cursor = db.execute('select * from formations where id_utilisateur=? and type_formation=?',
                                    (iduser, 'hard'))
                formations_hard = cursor.fetchall()
                return render_template('user.html', user= theUser, sous_formations=sous_formations,formations_hard = formations_hard,
                                       formations=formations, iduser=iduser, sous_formations_hard = sous_formations_hard)

    if request.method == 'POST' and request.form.get('essai') == 'update':
        id_formation = request.form.get('id_formation')
        id_sous_formation = request.form.get('id_sous_formation')
        id_formation_hard = request.form.get('id_formation_hard')
        id_sous_formation_hard = request.form.get('id_sous_formation_hard')
        id_user = request.form.get('id_user')
        theUser = request.form.get('theUser')
        type_sous_formations = request.form.get('type_sous_formations')
        print("id formation et sous formation et id",id_formation,id_sous_formation,id_user,type_sous_formations)
        db = get_db()

        if type_sous_formations == 'soft':
            #mettre a jour la formation et la sous formation
            db.execute('update sous_formations set active = true where id=? and id_formation=? and type_sous_formation=?',(id_sous_formation,id_formation,type_sous_formations))
            db.commit()

        if type_sous_formations == 'hard':
            #mettre a jour la formation et la sous formation
            db.execute('update sous_formations set active = true where id=? and id_formation=? and type_sous_formation=?',(id_sous_formation_hard,id_formation_hard,type_sous_formations))
            db.commit()

        # récuperer sa liste de sous formation et formation
        cursor = db.execute('select * from sous_formations where id_utilisateur=? and type_sous_formation=?', (id_user,'soft'))
        sous_formations = cursor.fetchall()
        cursor = db.execute('select * from sous_formations where id_utilisateur=? and type_sous_formation=?',
                            (id_user, 'hard'))
        sous_formations_hard = cursor.fetchall()
        print('taille sous formation : ', len(sous_formations))
        cursor = db.execute('select * from formations where id_utilisateur=? and type_formation=?', (id_user,'soft'))
        formations = cursor.fetchall()
        cursor = db.execute('select * from formations where id_utilisateur=? and type_formation=?',
                            (id_user, 'hard'))
        formations_hard = cursor.fetchall()
        return render_template('user.html', user=theUser, sous_formations=sous_formations,formations_hard=formations_hard,
                               formations=formations, iduser=id_user,sous_formations_hard=sous_formations_hard)

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
            print("nombre users : ", len(results))
            for x in results:
                if x['mail'] == email and x['nom'] == nom:
                    print("USERS EMAILS: ",x["mail"])
                    userid = x['id']

                    if x['domaine_d_etude']=='Informatique':
                        formationid = userid + 1
                        sous_formationid = userid + 1
                        formationid_hard = userid + 3
                        sous_formationid_hard = userid + 3
                        # récuperer sa liste de sous formation et formation

                    # on ajoute les formations pour cet utilisateur
                        conn.execute(
                            'insert into formations (id,titre, url_formation, description_formation, id_utilisateur,id_sous_formation, type_formation) VALUES (?,?,?,?,?,?,?)',
                            (formationid,'JAVA niveau 1 - débutant',
                             'https://www.youtube.com/watch?v=fmJsqBWkXm4&list=PLlxQJeQRaKDRnvgIvfHTV6ZY8M2eurH95&ab_channel=LESTEACHERSDUNET',
                             'Cette formation a pour but d avoir des competences basiques en java', userid,sous_formationid,'soft'))
                        conn.commit()

                        # on ajoute les formations pour cet utilisateur
                        conn.execute(
                            'insert into formations (id,titre, url_formation, description_formation, id_utilisateur,id_sous_formation, type_formation) VALUES (?,?,?,?,?,?,?)',
                            (formationid_hard, 'Master Java Multithreading Programming from Zero (Modern)',
                             'https://www.udemy.com/course/java-multi-threading-programming/',
                             'Learn Java threading programming using modern java techniques   (Lambdas & Streams). Hands-on Step by Step approache', userid,
                             sous_formationid_hard, 'hard'))
                        conn.commit()

                    #on jaoute les sous formations
                        conn.execute(
                        'insert into sous_formations (id, titre, url_formation, description_formation, id_utilisateur, active, id_formation, type_sous_formation) VALUES (?,?,?,?,?,?,?,?)',
                        (sous_formationid,'JAVA niveau 2 - intermédiaire',
                         'https://www.youtube.com/watch?v=2vvuGUxPv30&list=PLlxQJeQRaKDTCU85T7MTT8_YVfzLMtCKH&ab_channel=LESTEACHERSDUNET',
                         'Cette formation a pour but d avoir des competences java plus poussées', userid, False, formationid,'soft'))

                        conn.commit()

                        conn.execute(
                            'insert into sous_formations (id, titre, url_formation, description_formation, id_utilisateur, active, id_formation, type_sous_formation) VALUES (?,?,?,?,?,?,?,?)',
                            (sous_formationid_hard, 'Java: Socket Programming Simplified',
                             'https://www.udemy.com/course/java-socket-programming-by-sagar/',
                             'Build the foundations for server side programming, a MUST learn for server side application developers/aspirants.', userid, False,
                             formationid_hard, 'hard'))

                        conn.commit()

                        formationid = userid+2
                        sous_formationid = userid+2
                        formationid_hard = userid + 4
                        sous_formationid_hard = userid + 4

                        conn.execute(
                            'insert into formations (id,titre, url_formation, description_formation, id_utilisateur, id_sous_formation, type_formation) VALUES (?,?,?,?,?,?,?)',
                            (formationid,'PYTHON niveau 1 - débutant',
                             'https://www.youtube.com/watch?v=oUJolR5bX6g&ab_channel=CodeAvecJonathan',
                             'Cette formation a pour but d avoir des competences basiques en python', userid, sous_formationid,'soft'))
                        conn.commit()

                        conn.execute(
                            'insert into formations (id,titre, url_formation, description_formation, id_utilisateur, id_sous_formation, type_formation) VALUES (?,?,?,?,?,?,?)',
                            (formationid_hard, 'Prérequis MACHINE LEARNING — Python | Numpy | Mathématiques',
                             'https://www.udemy.com/course/prerequis-ml-dl-indispensables/',
                             'Apprenez, en moins d une journée, les concepts indispensables de Mathématiques, Python et Numpy pour le Machine Learning', userid,
                             sous_formationid_hard, 'hard'))
                        conn.commit()

                        conn.execute(
                            'insert into sous_formations ( id,titre, url_formation, description_formation, id_utilisateur, active, id_formation, type_sous_formation) VALUES (?,?,?,?,?,?,?,?)',
                            (sous_formationid,'PYTHON niveau 2 - intermédiaire',
                            'https://www.youtube.com/watch?v=LiBsVCXAgXI&ab_channel=FormationVid%C3%A9o',
                            'Cette formation a pour but d avoir des competences python plus poussées', userid, False, formationid,'soft'))
                        conn.commit()

                        conn.execute(
                            'insert into sous_formations ( id,titre, url_formation, description_formation, id_utilisateur, active, id_formation, type_sous_formation) VALUES (?,?,?,?,?,?,?,?)',
                            (sous_formationid_hard, 'Advanced AI: Deep Reinforcement Learning in Python',
                             'https://www.udemy.com/course/deep-reinforcement-learning-in-python/',
                             'The Complete Guide to Mastering Artificial Intelligence using Deep Learning and Neural Networks', userid, False,
                             formationid_hard, 'hard'))
                        conn.commit()

                    if x['domaine_d_etude'] == 'Mathématiques':
                        formationid_m = userid + 1
                        sous_formationid_m = userid + 1
                        formationid_hard_m = userid + 3
                        sous_formationid_hard_m = userid + 3
                        # récuperer sa liste de sous formation et formation

                        # on ajoute les sous_formations pour cet utilisateur
                        conn.execute(
                            'insert into formations (id,titre, url_formation, description_formation, id_utilisateur,id_sous_formation, type_formation) VALUES (?,?,?,?,?,?,?)',
                            (formationid_m,'Réussis ton bac de maths (édition Bac 2021)',
                             'https://www.udemy.com/course/reussis-ton-bac-de-maths-en-2-jours-edition-bac-s-2019/',
                             'Plus de 120 questions corrigées (4 réponses possibles par question) pour réussir l épreuve !',
                             userid, sous_formationid_m,'soft'))

                        conn.commit()

                        conn.execute(
                            'insert into formations (id,titre, url_formation, description_formation, id_utilisateur,id_sous_formation, type_formation) VALUES (?,?,?,?,?,?,?)',
                            (formationid_hard_m, 'Calculus 3 with the Math Sorcerer',
                             'https://www.udemy.com/course/calculus-3-with-the-math-sorcerer/',
                             'Learn Calculus 3 with the Math Sorcerer:)',
                             userid, sous_formationid_hard_m, 'hard'))

                        conn.commit()

                        conn.execute(
                            'insert into sous_formations (id, titre, url_formation, description_formation, id_utilisateur, active, id_formation, type_sous_formation) VALUES (?,?,?,?,?,?,?,?)',
                            (sous_formationid_m, 'Réussis ton bac de maths (édition Bac 2021)',
                                'https://www.udemy.com/course/reussis-ton-bac-de-maths-en-2-jours-edition-bac-s-2019/',
                                 'Plus de 120 questions corrigées (4 réponses possibles par question) pour réussir l épreuve !', userid, False,
                             formationid_m,'soft'))

                        conn.commit()

                        conn.execute(
                            'insert into sous_formations (id, titre, url_formation, description_formation, id_utilisateur, active, id_formation, type_sous_formation) VALUES (?,?,?,?,?,?,?,?)',
                            (sous_formationid_hard_m, 'Advanced Calculus/Real Analysis with the Math Sorcerer',
                             'https://www.udemy.com/course/advanced-calculusreal-analysis-with-the-math-sorcerer/',
                             'Selected Topics in Advanced Calculus/Real Analysis with tons of Beautiful Proofs:)',
                             userid, False,
                             formationid_hard_m, 'hard'))

                        conn.commit()

                        formationid_m = userid + 2
                        sous_formationid_m = userid + 2
                        formationid_hard_m = userid + 4
                        sous_formationid_hard_m = userid + 4
                        # on ajoute les sous_formations pour cet utilisateur
                        conn.execute(
                            'insert into formations (id,titre, url_formation, description_formation, id_utilisateur, id_sous_formation, type_formation) VALUES (?,?,?,?,?,?,?)',
                            (formationid_m,'Maîtrisez les bases des mathématiques !',
                                 'https://www.udemy.com/course/maitrisez-les-bases-des-mathematiques/',
                                 'Apprenez ou revisitez en profondeur les bases des maths et testez vous avec plus de 80 exercices corrigés.',
                             userid, sous_formationid_m,'soft'))
                        conn.commit()

                        conn.execute(
                            'insert into formations (id,titre, url_formation, description_formation, id_utilisateur, id_sous_formation, type_formation) VALUES (?,?,?,?,?,?,?)',
                            (formationid_hard_m, 'Become an Algebra Master',
                             'https://www.udemy.com/course/integralcalc-algebra/',
                             'Learn everything from Algebra 1 and Algebra 2, then test your knowledge with 1,300+ practice questions',
                             userid, sous_formationid_hard_m, 'hard'))
                        conn.commit()

                        conn.execute(
                            'insert into sous_formations ( id,titre, url_formation, description_formation, id_utilisateur, active, id_formation, type_sous_formation) VALUES (?,?,?,?,?,?,?,?)',
                            (sous_formationid_m, 'Cours de maths - Maîtrisez les bases de l analyse !',
                             'https://www.udemy.com/course/cours-de-maths-maitrisez-les-bases-de-lanalyse/',
                             'Comprenez en profondeur les fonctions en mathématiques ! Entraînez-vous avec plus de 60 exercices.',
                             userid, False,formationid_m,'soft'))
                        conn.commit()

                        conn.execute(
                            'insert into sous_formations ( id,titre, url_formation, description_formation, id_utilisateur, active, id_formation, type_sous_formation) VALUES (?,?,?,?,?,?,?,?)',
                            (sous_formationid_hard_m, 'Become a Linear Algebra Master',
                             'https://www.udemy.com/course/linear-algebra-course/',
                             'Learn everything from Linear Algebra, then test your knowledge with 400+ practice questions',
                             userid, False, formationid_hard_m, 'hard'))
                        conn.commit()



                    conn.close()
                    return redirect(url_for('connexion'))




    return render_template('inscription.html')

if __name__ == '__main__':
    app.run(debug = True)