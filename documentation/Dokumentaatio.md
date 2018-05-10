## Dokumentaatio

### Kirjautuminen Herokuun

Pääkäyttäjän tunnus: _hello_, salasana: _world_
Normaalikäyttäjän tunnus: _gandalf_, salasana: _klonkku_

### Tietokantakaavio

![Tietokantakaavio](https://github.com/maarila/keskustelufoorumi/blob/master/documentation/img/Tietokantakaavio.png)

### Tietokannan luominen

*Käyttäjät:*

```
CREATE TABLE account (
  id INTEGER NOT NULL, 
  date_created DATETIME, 
  date_modified DATETIME, 
  name VARCHAR(64) NOT NULL, 
  username VARCHAR(32) NOT NULL, 
  password VARCHAR(256) NOT NULL, 
  admin BOOLEAN NOT NULL, 
  PRIMARY KEY (id), 
  CHECK (admin IN (0, 1))
);
```

*Aihealueet:*

```
CREATE TABLE topic (
  id INTEGER NOT NULL, 
  date_created DATETIME, 
  date_modified DATETIME, 
  title VARCHAR(64) NOT NULL, 
  creator VARCHAR(64) NOT NULL, 
  PRIMARY KEY (id)
);
```

*Viestit:*

```
CREATE TABLE message (
  id INTEGER NOT NULL, 
  date_created DATETIME, 
  date_modified DATETIME, 
  author VARCHAR(64), 
  content VARCHAR(2048) NOT NULL, 
  account_id INTEGER NOT NULL, 
  topic_id INTEGER NOT NULL, 
  reply_id INTEGER, 
  PRIMARY KEY (id), 
  FOREIGN KEY(account_id) REFERENCES account (id), 
  FOREIGN KEY(topic_id) REFERENCES topic (id), 
  FOREIGN KEY(reply_id) REFERENCES message (id)
);
```

*Käyttäjien ja viestien välinen liitostaulu:*

```
CREATE TABLE views (
  account_id INTEGER NOT NULL, 
  message_id INTEGER NOT NULL, 
  PRIMARY KEY (account_id, message_id), 
  FOREIGN KEY(account_id) REFERENCES account (id), 
  FOREIGN KEY(message_id) REFERENCES message (id)
);
```

### Käyttötapaukset / käyttäjätarinat

*Tavallinen käyttäjä:*

- [x] Käyttäjänä voin luoda itselleni käyttäjätunnukset.

```
INSERT INTO Account (name, username, password, admin) 
VALUES ("Etunimi Sukunimi", "tunnus", "salasana", 0 tai 1);`
```
- [x] Käyttäjänä voin kirjautua keskustelualustalle.

```
SELECT * FROM Account WHERE Account.name = kirjautuvan_käyttäjän_nimi 
AND Account.password = kirjautuvan_käyttäjän_salasana;`
```

- [x] Käyttäjänä voin lisätä aihealueelle viestin.

```
INSERT INTO Message (author, content, topic_id, account_id) 
VALUES ("kirjoittajan nimi", "viestin sisältö", aihealueen_id, kirjoittajan_id);`
```

- [x] Käyttäjänä voin vastata aihealueella olevaan viestiin.

```
INSERT INTO Message (author, content, topic_id, reply_id, account_id) 
VALUES ("kirjoittajan nimi", "viestin sisältö", aihealueen_id, 
vastattavan_viestin_id, kirjoittajan_id);
```

- [x] Käyttäjänä voin muokata lähettämiäni viestejä.

```
UPDATE Message SET content="uusi viesti" 
WHERE Message.id=muokattavan_viestin_id;
```

- [x] Käyttäjänä voin nähdä kaikki vastaukset viestiin.

`SELECT * FROM Message WHERE Message.reply_id = halutun_viestin_id;`

- [x] Käyttäjänä voin lukea minkä tahansa viestin mistä tahansa aihealueesta.

```
SELECT * FROM Message WHERE Topic.id = halutun_viestin_topic_id
AND Message.id = halutun_viestin_id;
```

- [x] Käyttäjänä voin nähdä, ketkä kaikki ovat lukeneet minkä tahansa viestin.

```
SELECT Account.name FROM Account
INNER JOIN Views ON Views.message_id = halutun_viestin_id
WHERE Account.id = Views.account_id;
```

- [x] Käyttäjänä voin selailla viestejä aihealueen, kirjoittajan tai viestin iän perusteella.

Viisi suosituinta aihealuetta vastausten määrän perusteella mitattuna:

```
SELECT Topic.id, Topic.title, COUNT(Message.id) as msgs FROM Topic
INNER JOIN Message ON Topic.id = Message.topic_id
GROUP BY Topic.id
ORDER BY msgs DESC
LIMIT 5
```

Haku aihealueen nimestä:

```
SELECT * FROM Topic WHERE Topic.title LIKE "%hakusana%"
ORDER BY Topic.date_created DESC 
```

Haku kirjoittajan nimestä tai viestin sisällöstä:

```
SELECT * FROM Message WHERE Message.author LIKE "%hakusana%"
OR Message.content LIKE "%hakusana%"
ORDER BY Message.date_created DESC 
```

Haku kirjoitusajankohdan perusteella:

```
SELECT * FROM Message
WHERE date_created BETWEEN haun_aloituskohta AND haun_päättymiskohta;
```

Viestin iän perusteella ts. uusimmat viisi viestiä viidestä eri aihealueesta (huom! haku ei ole toiminnassa sovelluksessa, tarkempi selvitys kohdassa "Työn ja sovelluksen rajoitteet"):

Kysely SQLitelle kelpaavassa muodossa:

```
SELECT Topic.id, Topic.title, Message.id, Message.content, Message.date_created 
FROM Topic
INNER JOIN Message ON Topic.id = Message.topic_id
GROUP BY Topic.id
ORDER BY Message.date_created DESC
LIMIT 5
```

Sama kysely PostgreSQL:lle:

```
SELECT Topic.id, Topic.title, x.id AS msg_id, x.content, x.date_created FROM
(SELECT DISTINCT ON(Message.topic_id) Message.id, Message.content,
Message.date_created, Message.topic_id FROM Message
ORDER BY Message.topic_id, Message.date_created DESC
LIMIT 5) AS x
INNER JOIN Topic ON Topic.id = x.topic_id
ORDER BY x.date_created DESC
```

- [x] Käyttäjänä voin nähdä tietoja itsestäni ja muista käyttäjistä.

Käyttäjän viimeisin viesti:

```
SELECT m.id, m.date_created, m.content, m.topic_id, Topic.title FROM Message AS m
INNER JOIN Topic ON m.topic_id = topic.id
WHERE m.account_id = halutun_käyttäjän_id
ORDER BY m.date_created DESC
LIMIT 1
```

Käyttäjän viestimäärä:

```
SELECT COUNT(*) AS messages FROM Message 
WHERE Message.account_id = halutun_käyttäjän_id;
```

*Ylläpitäjä:*

Kaikkien edellämainittujen lisäksi:

- [x] Ylläpitäjänä voin luoda uusia käyttäjiä.

```
INSERT INTO Account (name, username, password, admin) 
VALUES ("Etunimi Sukunimi", "tunnus", "salasana", 0);
```

- [x] Ylläpitäjänä voin perustaa uusia aihealueita.

`INSERT INTO Topic (title) VALUES ("Haluttu otsikko");`

- [x] Ylläpitäjänä voin muokata aihealueita.

```
UPDATE Topic SET title="uusi aihealueen nimi" 
WHERE Topic.id=muokattavan_aihealueen_id;
```

- [x] Ylläpitäjänä voin poistaa aihealueita.

`DELETE FROM Topic WHERE Topic.id = poistettavan_aihealueen_id;`

Jos samassa yhteydessä poistaa myös aihealueeseen kuuluneet viestit, niin ennen edellistä pitää suorittaa:

`DELETE FROM Message WHERE Message.topic_id = poistettavan_aihealueen_id;`

- [x] Ylläpitäjänä voin poistaa viestejä.

`DELETE FROM Message WHERE Message.id = poistettavan_viestin_id;`

- [x] Ylläpitäjänä voin lisätä käyttäjän ryhmään.

- [x] Ylläpitäjänä voin muokata käyttäjien ryhmästatusta.

- [x] Ylläpitäjänä voin poistaa käyttäjän ryhmästä.

Kolmeen edelliseen kohtaan:

```
UPDATE Account SET admin=joko_nolla_tai_yksi
WHERE Account.id = muokattavan_käyttäjän_id;
```

### Käyttöohje

*Tavallisen käyttäjän ohjeet*

Sovelluksen etusivulla näkyvät viisi viimeisintä keskustelun aihetta uusimmasta vanhimpaan. Valitse ylävalikon oikeasta yläkulmasta *Register* ja kirjaudu järjestelmään haluamallasi nimellä, käyttäjätunnuksella ja salasanalla. Nimessä on oltava 4-48 merkkiä, käyttäjätunnuksessa 4-24 merkkiä ja salasanassa 6-255 merkkiä. Valitse tämän jälken *Login* ja kirjaudu sovellukseen luomillasi tunnuksilla.

Voit nyt selata viestejä pääsivulla aihealueittain joko uusimpien tai suosituimpien viestien listauksen kautta tai kaikki viestit listaamalla. Aihealueen avattuasi voit kirjoittaa aihealueeseen uuden vastineen tai selata muihin vastineisiin tulleita viestien perässä olevien _Replies_-listauksen tai _View all replies_-toiminnon kautta. Mikäli haluat vastata johonkin tiettyyn vastineeseen, valitse tällöinkin _View all replies_. Omien vastaustesi perästä löydät *Edit*-napin, jolla voit muokata kirjoittamiasi viestejä.

Viestin lopusta näet myös käyttäjät, jotka ovat viestin jo lukeneet.

Sivuston ylävalikon *Search*-toiminnon valitsemalla voi etsiä viestejä otsikon, viestin kirjoittajan tai sekä kirjoittajan että viestin sisällön perusteella. Hakusivulla on myös etsiä viestejä tietyltä ajanjaksolta.

*Pääkäyttäjän ohjeet*

Voit myös kirjautua sovellukseen pääkäyttäjän ns. admin-tunnuksilla. Valitse tällöin sivuston ylävalikosta *Login* ja syötä pääkäyttäjän tunnukset. Mikäli käytät sovellusta Herokussa, syötä  käyttäjätunnukseksi _hello_ sekä salasanaksi _world_. Pääkäyttäjän tunnuksilla voit käyttää kaikkia samoja toiminnallisuuksia kuin tavallisetkin käyttäjät, mutta niiden lisäksi pääkäyttäjä voi lisätä, muokata ja poistaa aiheita, lisätä ja poistaa käyttäjiä, myöntää muille käyttäjille pääkäyttäjäoikeudet sekä poistaa yksittäisiä viestejä.

Pääkäyttäjän toiminnallisuuksista aihealueiden muokkaaminen ja poistaminen tapahtuu sovelluksen pääsivun kautta. Muut toiminnallisuudet ovat tarjolla sivuston ylävalikossa. *Add user*-toiminnallisuudella voi lisätä uusia käyttäjiä, *Create topic*-toiminnallisuudella voi luoda uusia aihealueita, *Show all messages*-toiminto listaa kaikki viestit ja mahdollistaa niiden poistamisen, *Show all users* puolestaan listaa kaikki järjestelmän käyttäjät, mahdollistaa näiden poistamisen sekä antaa mahdollisuuden lisätä käyttäjälle pääkäyttäjän oikeudet tai poistaa ne.

### Asennusohje

Avaa terminaali ja siirry hakemistoon, johon haluat asentaa sovelluksen. Lataa sovellus koneellesi gitin kloonina:

`git clone git@github.com:maarila/keskustelufoorumi.git`

Koska kyseessä on Python3-ohjelmisto, sovelluksen kloonaamisen jälkeen on asennettava sen tarvitsema virtuaaliympäristö:

`python3 -m venv venv`

Tämän jälkeen on asennettava sovelluksen vaatimat riippuvuudet:

`pip install -r requirements.txt`

Seuraavaksi on aktivoitava virtuaaliympäristö:

`source venv/bin/activate`

Nyt sovelluksen voi käynnistää sen juurihakemistosta:

`python3 run.py`

Käynnistämisen yhteydessä ohjelma luo application-hakemistoon SQLite3-tietokannan messages.db. Ensimmäinen pääkäyttäjäoikeuksilla varustettu käyttäjä on lisättävä suoraan tietokantaan:

```
cd application/
sqlite3 messages.db
INSERT INTO Account (name, username, password admin) VALUES ('Haluttu nimi', 'käyttäjätunnus', 'salasana', 1);
```

Ohjelmistoa voi nyt käyttää. Avaa haluamallasi selaimella (ohjelmiston toimivuus on testattu Google Chromella) osoite http://localhost:5000.

### Työn ja sovelluksen rajoitteet



### Puuttuvat ominaisuudet



### Dokumentaation vastaavuus toteutettuun työhön

Tietokannassa käyttäjä-, aihealue- ja viestitauluilla on sarake "date_modified", mutta sitä ei ole implementoitu itse sovellukseen. En kuitenkaan poistanut sitä tietokannan luomisesta, koska muokkaustieto on tarpeellinen sovelluksen jatkokehityksen kannalta.

### Omat kokemukset

Valitsin esimerkkiaiheista kiinnostavalta ja selkeältä tuntuneen keskustelufoorumin. En muokannut määrittelytekstiä juurikaan, jolloin siihen jäi myös lause "lukija voi seurata vastinepolkua" kirjoitusten lukemisen suhteen. Näin jälkiviisaana voin todeta, että kyseisen lauseen poisjättäminen tai sen muokkaaminen olisi ollut järkevä ratkaisu, koska se määritti sovelluksen toiminnallisuutta ja viestien esittämistä sekä käsittelyä lopulta kohtuuttoman paljon. 
