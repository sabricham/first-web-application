PICTURIST - Applicazione web e server per l'esame 'Fotografie' del 12/06/2023

Introduzione:
Il sito web è costituito da questi componenti:

login.html: per il login e avvio della sessione
register.html: per la registrazione

home.html: per la visualizzazione degli album pubblici
home-view-album.html: per la visualizzazione delle foto pubbliche dell'album pubblico scelto
home-view-photo.html: per la visualizzazione in dettaglio della singola foto di un album pubblico

[accessibili solo con login]
personal-area.html: per la visualizzazione degli album personali e creazione nuovi album personali
personal-view-album.html: per la visualizzazione delle foto contenute nell'album personale e aggiunta di foto ad esso
personal-view-photo.html: per la visualizzazione in dettaglio della singola foto di un album personale
personal-add-photo.html: per la definizione e aggiunta di una foto all'album personale scelto

ogni file .html possiede per semplicità organizzativa e di modifica un suo proprio file .css

app.py: gestisce tutto il lato server dell'applicazione
dao.py: permette al lato server di comunicare con il database ed effettuare le query SQL necessarie
app.js: gestisce solo ed esclusivamente la ricerca per nome (anche parziale) di foto in un album

-------------------------------------------------------------------
Sezione #1 - Target dell'applicazione:
Sezione #2 - Come sono gestiti i dati nell'applicazione
Sezione #3 - Dati contenuti nel database (utenti, album, foto)
Sezione #4 - Esecuzione dell'applicazione

-------------------------------------------------------------------
Sezione #1 - Target dell'applicazione:
- L'applicazione e' progettata principalmente per dispositivi desktop (essenzialmente chrome per windows) su schermo con rapporto 16:9
- Le foto utilizzate dal sito sono esclusivamente in rapporto 1:1 e di formato .jpg

-------------------------------------------------------------------
Sezione #2 - Come sono gestiti i dati nell'applicazione:

Cartella 'database': contiene il database sqlite, uno solo che possiede al suo interno 3 tabelle: users, albums, photos
Cartella 'static': contiene i file .css dell'applicazione, il file javascript, varie icone .png utilizzate nell'applicazione
	denominate icon-....png, tutte le foto degli utenti conservate come 'uploaded-photo-<photo_id>.jpg'
Cartella principale: contiene tutte le sottocartelle e i file .html

-------------------------------------------------------------------
Sezione #3 - Dati contenuti nel database secondo il formato:

-users[nome, cognome, email, password]
		-albums(titolo)
				-photos(titolo)

Dati contenuti nel database:

-[Vanessa, Sarcina, vanessa@email.it, vanessa]
		-Tokyo Tango: Danze tra tradizione e modernità
				-Car Spotting a Tokyo (PUBBLICA)
				-La quiete sussurrante delle periferie giapponesi (PUBBLICA)

-[Andrea, Romano, andrea@email.it, andrea]
		-Concrete Jungle: New York in Frames
				-Verdi Orizzonti: Il Maestoso Central Park (PRIVATA)
				-Statue of Liberty's Majesty (PUBBLICA)
				-Skyscrapers in Symphony (PUBBLICA)

-[Luigi, Mancini, luigi@email.it, luigi]
		-Esplorando il Nepal: un viaggio in terre sacre
				-L'armonia dei templi di Kathmandu (PRIVATA)
		-Vette di Bellezza e Serenità giapponesi
				-L'eterno Maestro: Il Monte Fuji (PUBBLICA)

-------------------------------------------------------------------
Sezione #4 - Esecuzione dell'applicazione:

- Procedura regolare di avvio:
Attivare la modalità venv con il comando 'venv/Scripts/activate'
Tramite terminale flask di Visual Studio Code eseguire il comando 'flask run' ed accedere come di consueto
all'indirizzo 127.0.0.1:5000

- Durante la navigazione:
Per effettuare login e accedere a profili che contengono già album e foto pubblicate attenersi alle credenziali
nella sezione precedente

- Per i test:
Per inserire nuove foto utilizzare le foto contenute nella cartella 'TEST', sono verificate in ogni parte
