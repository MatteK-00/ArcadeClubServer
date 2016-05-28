drop schema if exists arcadeclub cascade;

create schema arcadeclub;

set search_path to arcadeclub;

create domain condition as varchar CHECK (value = 'Sealed' OR value = 'Completo' OR value = 'Loose'OR value = 'Nol' );

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
	anno varchar,
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
	anno varchar,
	console varchar NOT NULL,
	stato condition NOT NULL,
	quality numeric CHECK (quality > 0 AND quality < 6),
	prezzo_acquisto numeric,
	prezzo_vendita numeric,
	data_acquisto DATE,
	data_vendita DATE,
	note varchar
);

INSERT INTO utente (username,pwd,device) VALUES ('pippo','cane','9c52e085b2ea7cab');
INSERT INTO gioco (upc,nome,anno,console,immagine) VALUES ('3286010000057','nome prova','1999','xbox one',NULL);
INSERT INTO gioco (upc,nome,anno,console,immagine) VALUES ('4286010000057','nome prova','1998','xbox one',NULL);
INSERT INTO gioco (upc,nome,anno,console,immagine) VALUES ('5286010000057','nome prova','2000','xbox one',NULL);

INSERT INTO magazzino (upc,nome,anno,console,stato,quality,prezzo_acquisto,data_acquisto,note) VALUES ('3286010000057','nome prova','1999','xbox one','Sealed','4','10','12-7-21015',NULL);
INSERT INTO magazzino (upc,nome,anno,console,stato,quality,prezzo_acquisto,data_acquisto,note) VALUES ('3286010000057','nome prova','1998','xbox one','Completo','5','10','12-7-21015',NULL);
INSERT INTO magazzino (upc,nome,anno,console,stato,quality,prezzo_acquisto,data_acquisto,note) VALUES ('4286010000057','nome prova','1998','xbox one','Sealed','4','10','12-7-21015',NULL);
INSERT INTO magazzino (upc,nome,anno,console,stato,quality,prezzo_acquisto,data_acquisto,note) VALUES ('5286010000057','nome prova','2000','xbox one','Sealed','4','10','12-7-21015',NULL);
