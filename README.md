# Verwendung von Datasette in GitHub Codespaces

GitHub Codespaces bietet dir eine vollwertige Linux-Entwicklungsumgebung direkt im Browser – ideal, um mit Datasette zu starten und eigene Daten privat zu erkunden.
**Wichtig:** Codespaces ist **nicht** zum Hosten öffentlicher Websites gedacht. Jede gestartete Datasette-Instanz bleibt privat.

Dieses Tutorial zeigt dir, wie du Datasette in einem Codespace installierst, Daten importierst und auf einer Karte visualisierst.
**Voraussetzung**: Eine Voraussetzung für das Ausführen des Tutorials in Codespaces ist ein Github-Login.

**Für die ganz Mutigen (ohne zu restriktive Laptops): Versucht es gerne direkt lokal auf dem Computer (ohne Codespaces).**

---

## 🏁 Schritt 1: Codespace erstellen

Jeder Codespace ist an ein GitHub-Repository gebunden.

Du kannst direkt dieses Repository `DCC-BS/codespaces-datasette` nutzen oder es forken, wenn du deinen Fortschritt bewahren willst. 
Falls du einen Fork des Repositories erstellen möchtest, kannst du auf den Button **Fork** oben rechts klicken und dann auf den Button **Create Fork**.

<img width="420" height="76" alt="image" src="https://github.com/user-attachments/assets/c4a65918-1608-457a-b0e5-9741c5da82a7">

<br>
<br>

Klicke nun auf **Code → Codespaces → Create codespace on main**.

<img src="https://github.com/DCC-BS/codespaces-datasette/blob/main/get-started.jpg?raw=true" alt="Codespace oeffnen" width=30% height=30%>

Nach wenigen Momenten erscheint die Codespaces-Umgebung.
Wir arbeiten ausschliesslich im Terminal-Bereich.

<img src="https://github.com/DCC-BS/codespaces-datasette/blob/main/codespaces-ui.jpg?raw=true" alt="Codespaces UI" width=50% height=50%>

---

## 📦 Schritt 2: Datasette installieren

Installiere zuerst Datasette:

```bash
pipx install datasette
```

Prüfe die Installation:

```bash
datasette --version
```

Installiere danach das Codespaces-Plugin:

```bash
datasette install datasette-codespaces
```

💡 *Das Plugin verbessert interne Links in Codespaces. Ohne dieses Plugin kann es zu kleinen Stolpersteinen kommen.*

---

## 🚀 Schritt 3: Datasette starten

Starte Datasette:

```bash
datasette data.db --create
```

Falls `data.db` noch nicht existiert, wird die Datei automatisch erstellt.

<img src="https://github.com/DCC-BS/codespaces-datasette/blob/main/start-datasette.jpg?raw=true" alt="Datasette starten" width=70% height=70%>

Codespaces zeigt nun an, dass Port 8001 aktiv ist – klicke auf **Open in Browser**.
Falls kein Button erscheint: nutze den Tab **Ports** im Terminal-Bereich.

---

## 📥 Schritt 4: Daten importieren

Datasette startet mit einer leeren [sqlite](https://sqlite.org/index.html)-Datenbank – also fügen wir Daten hinzu.

Wir wollen folgende Daten in unsere sqlite-Datenbank laden: [swissNAMES3D](https://www.swisstopo.admin.ch/de/landschaftsmodell-swissnames3d). 

Die vorhandenen csv-Dateien wurden in Vorbereitung auf dieses Tutorial von Semikolon-separiert zu Komma-separiert geändert. Zudem wurden die Koordinaten in den Dateien vom schweizerisch-liechtensteinischen Georeferenzsystem (EPSG:2056) auf das globale Koordinatensystem (EPSG:4326) übersetzt, damit die Karte nachher auch funktioniert.

Beende die laufende Datasette-Instanz mit der leeren Datenbank, indem du die Tastenkombination **Ctrl+C** im laufenden Terminal betätigst.

Installiere `sqlite-utils`:

```bash
pipx install sqlite-utils
```

Prüfe:

```bash
sqlite-utils --version
```

Importiere die vorbereiteten swissNAMES3D-Liniendaten:

```bash
sqlite-utils insert data.db linien \
    swissNAMES3D_LIN.csv \
    --csv -d
```

Damit entsteht eine Tabelle `linien` mit allen Liniengeometrien:
Brücken, Tunnel, Seilbahnen, Sportanlagen, Fliessgewässer und mehr.

**See for yourself!**

```bash
datasette data.db
```

Dann auf **data (Datenbank) -> linien (Tabelle)** klicken, um zur Tabelle zu gelangen.

<img width="479" height="374" alt="image" src="https://github.com/user-attachments/assets/e20b8741-a3da-473b-8c98-7fa13488743a" />

---

## 🔌 Schritt 5: Plugins installieren

Stoppe Datasette bei Bedarf, falls die Instanz noch läuft, mit **Ctrl+C**.

Installiere zwei benötigte Plugins:

**1. Schema-Editor (zum Spalten umbenennen)**

```bash
datasette install datasette-edit-schema
```

**2. Cluster-Map (für Kartenansicht)**

```bash
datasette install datasette-cluster-map
```

---

## 🗺️ Schritt 6: Daten auf einer Karte anzeigen

Starte Datasette erneut:

```bash
datasette data.db
```

Öffne die Tabelle **linien**.

Die Spalten heissen aktuell **E** (Längengrad) und **N** (Breitengrad).
Für die Kartenansicht benötigt Datasette jedoch **longitude** und **latitude**.

Benenne die Spalten um:

* `E` → `longitude`
* `N` → `latitude`

Vorgehen: Zahnrad anklicken → *Edit table schema* → speichern.

<img src="https://github.com/DCC-BS/codespaces-datasette/blob/main/edit_schema.png?raw=true" alt="Schema aendern" width=50% height=50%>

💡 Falls Datasette lokal ausgeführt wird, kann es notwendig sein, die Applikation als root zu starten:

```bash
datasette data.db --root
```

Sobald die Spalten umbenannt sind, sollte die Karte der Schweiz mit allen Linien erscheinen.

---

## 🎉 Schritt 7: Explore!

Probiere die **Facetten** aus.
Was passiert, wenn du unter *Suggested facets* auf `OBJEKTART` klickst?

💡 Was sind Facetten? Einfach gesagt, kann man auch von Filtern sprechen.

Wenn Zeit ist, kannst du auch die beiden anderen Tabellen importieren und sie `punkte` und `polygone` nennen – ganz analog zu Schritt 4. Du findest die Namen der entsprechenden csv-Dateien in der Seitenleiste am linken Bildrand.

Und falls du mehr brauchst: Entdecke weitere Plugins hier:
[https://datasette.io/plugins](https://datasette.io/plugins)

---

## Schritt 8: Schlussbemerkungen

**Warum werden nicht alle Datenpunkte in der Karte gezeigt?** Datasette hat als Standardeinstellung eine Zeilenbeschränkung auf 101 Zeilen. Diese kann bei der SQL-Query (View and Edit SQL) angepasst werden.

<img width="1505" height="117" alt="image" src="https://github.com/user-attachments/assets/f5f87074-e7b1-4027-b064-74ecb303a3f7" />

<br>
<br>

**Wie kann die Arbeit in Codespaces gespeichert werden?** Falls das Repository am Anfang geforked wurde, kann am linken Seitenrand auf das Icon für die Quellcodeverwaltung geklickt werden. Danach können die Änderungen gestaged, commited und gepushed werden.

<img width="343" height="187" alt="image" src="https://github.com/user-attachments/assets/3df1d5a6-2aa5-4f17-add7-a9488330caa2" />

<br>
<br>

**Können auch eigene csv-Dateien in diesen Codespace geladen und betrachtet werden?** Ja, indem lokal gespeicherte csv-Dateien in die Seitenleiste am linken Bildrand gezogen wird. Diese können dann analog zu den vorbereiteten Dateien in Datasette geladen werden. Es ist wichtig, dass die csv-Dateien Komma-separiert sind. Für Kartendaten braucht es Koordinaten im globalen System mit den Spaltennamen `longitude` und `latitude`.

---
Dieses Tutorial basiert auf folgendem Tutorial: [Using Datasette in GitHub Codespaces](https://datasette.io/tutorials/codespaces).
