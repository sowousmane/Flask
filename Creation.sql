
DROP TABLE IF EXISTS utilisateurs;

CREATE TABLE utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mail TEXT NOT NULL,
    mot_de_passe TEXT NOT NULL,
    nom TEXT,
    prenom TEXT ,
    date_naiss TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
    nationnalite TEXT ,
    pays TEXT,
    ville TEXT,
    domaine_d_etude TEXT ,
    niveau_d_etude TEXT 
);
