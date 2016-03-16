drop schema if exists arcadeclub cascade;

create schema arcadeclub;

set search_path to arcadeclub;

create domain condition as varchar CHECK (value = 'sealed' OR value = 'completo' OR value = 'loose'OR value = 'nol' );

create table utente
(
	id SERIAL UNIQUE primary key,
	username varchar NOT NULL,
	pwd varchar,
	device varchar,
	UNIQUE(username,pwd,device)
);

create table magazzino
(
	id_item SERIAL UNIQUE primary key,
	upc varchar,
	nome varchar NOT NULL,
	anno numeric,
	console varchar NOT NULL,
	stato condition NOT NULL,
	quality numeric CHECK (quality > 0 AND quality < 6),
	prezzo_acquisto numeric,
	data_acquisto DATE,
	note varchar
);

create table gioco
(
	id_gioco SERIAL UNIQUE primary key,
	upc varchar,
	nome varchar NOT NULL,
	anno varchar,
	console varchar NOT NULL,
	immagine varchar
);

create table venduti
(
	id_item SERIAL UNIQUE primary key,
	upc varchar, 
	nome varchar NOT NULL,
	anno numeric,
	console varchar NOT NULL,
	stato condition NOT NULL,
	quality numeric CHECK (quality > 0 AND quality < 6),
	prezzo_acquisto numeric,
	prezzo_vendita numeric,
	data_acquisto DATE,
	data_vendita DATE,
	note varchar
);

INSERT INTO utente (username,pwd,device) VALUES ('pippo','cane','idtel');
INSERT INTO gioco (upc,nome,anno,console,immagine) VALUES ('3286010000057','nome prova','1999','xbox one',NULL);
INSERT INTO gioco (upc,nome,anno,console,immagine) VALUES ('4286010000057','nome prova','1998','xbox one',NULL);
INSERT INTO gioco (upc,nome,anno,console,immagine) VALUES ('5286010000057','nome prova','2000','xbox one',NULL);

INSERT INTO magazzino (upc,nome,anno,console,stato,quality,prezzo_acquisto,data_acquisto,note) VALUES ('3286010000057','nome prova','1999','xbox one','sealed','4','10','12-7-21015',NULL);
INSERT INTO magazzino (upc,nome,anno,console,stato,quality,prezzo_acquisto,data_acquisto,note) VALUES ('3286010000057','nome prova','1998','xbox one','completo','5','10','12-7-21015',NULL);
INSERT INTO magazzino (upc,nome,anno,console,stato,quality,prezzo_acquisto,data_acquisto,note) VALUES ('4286010000057','nome prova','1998','xbox one','sealed','4','10','12-7-21015',NULL);
INSERT INTO magazzino (upc,nome,anno,console,stato,quality,prezzo_acquisto,data_acquisto,note) VALUES ('5286010000057','nome prova','2000','xbox one','sealed','4','10','12-7-21015',NULL);