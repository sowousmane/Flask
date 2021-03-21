import sqlite3

connection = sqlite3.connect('database.db')


with open('Creation.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO utilisateurs (mail, mot_de_passe) VALUES (?, ?)",
            ('ousmane@gmail.com', 'ousmane')
            )

cur.execute("INSERT INTO utilisateurs (mail, mot_de_passe,nom, prenom, date_naiss,nationnalite, pays, ville, domaine_d_etude, niveau_d_etude) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('Nada@gmail.com', 'Nada', 'Zerrga', 'Nada', '2000-01-20', 'Algérienne', 'Informatique', 'M1')
            )

connection.commit()
connection.close()