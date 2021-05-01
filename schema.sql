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

DROP TABLE IF EXISTS formations;

CREATE TABLE formations (
  id INTEGER,
  titre TEXT NOT NULL,
  url_formation TEXT NOT NULL,
  description_formation TEXT NOT NULL,
  id_utilisateur INTEGER not null,
  id_sous_formation INTEGER,
  type_formation TEXT NOT NULL
);


DROP TABLE IF EXISTS sous_formations;

CREATE TABLE sous_formations (
  id INTEGER,
  titre TEXT NOT NULL,
  url_formation TEXT NOT NULL,
  description_formation TEXT NOT NULL,
  id_utilisateur INTEGER not null,
  active boolean not null,
  id_formation INTEGER not null,
  type_sous_formation TEXT NOT NULL
);
