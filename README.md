# Verwendung von Datasette in GitHub Codespaces

GitHub Codespaces ist ein kostenloses Tool von GitHub, das dir eine vollständige Linux-Entwicklungsumgebung in der Cloud bereitstellt – vollständig im Browser.

Es eignet sich hervorragend, um mit Datasette zu starten, insbesondere als private Instanz zum Erkunden und Analysieren eigener Daten.

Bitte beachte: Codespaces ist **nicht** dafür gedacht, öffentliche Websites zu hosten. Alle in einem Codespace gestarteten Datasette-Instanzen sind ausschliesslich privat zugänglich.

Dieses Tutorial zeigt, wie du Datasette in einem Codespace installierst und ausführst.

---

## Schritt 1: Codespace erstellen

Jeder Codespace muss mit einem GitHub-Repository verknüpft sein.

Du kannst den Codespace dieser Repository `DCC-BS/codespaces-datasette` nutzen oder diese Repository gleich forken, um mit eigenen Daten zu arbeiten.

Klicke anschliessend auf **Code → Codespaces → Create codespace on main**, um einen neuen Codespace zu starten.

<img src="https://github.com/DCC-BS/codespaces-datasette/blob/main/get-started.jpg?raw=true" alt="Codespace öffnen" width=30% height=30%>

Nach kurzer Wartezeit erscheint die Codespaces-Umgebung – wir arbeiten ausschliesslich im Terminal-Bereich unten auf der Seite.

<img src="https://github.com/DCC-BS/codespaces-datasette/blob/main/codespaces-ui.jpg?raw=true" alt="Codespaces UI" width=50% height=50%>

---

## Schritt 2: Datasette installieren

Zuerst installieren wir Datasette:

```bash
pipx install datasette
```

Prüfe die Installation:

```bash
datasette --version
```

Installiere anschliessend das Codespaces-Plugin:

```bash
datasette install datasette-codespaces
```
Das Plugin datasette-codespaces nimmt einige kleine Änderungen an Datasette vor, damit es in der Codespaces-Umgebung besser läuft. Sie können Datasette auch ohne dieses Plugin ausführen, aber dabei können frustrierende Probleme auftreten, z. B. dass interne Links nicht richtig funktionieren.

---

## Schritt 3: Datasette starten

Starte Datasette mit:

```bash
datasette data.db --create
```

Falls die Datenbank `data.db` noch nicht existiert, wird sie automatisch angelegt.

<img src="https://github.com/DCC-BS/codespaces-datasette/blob/main/start-datasette.jpg?raw=true" alt="Datasette in neuem Tab öffnen" width=70% height=70%>

Codespaces zeigt dir einen Hinweis an, dass eine Anwendung auf Port 8001 läuft – klicke auf **Open in Browser**.

Falls kein Button sichtbar ist, nutze den Tab **Ports** in der Codespaces-Ansicht.

---

## Schritt 4: Daten importieren

Datasette startet mit einer leeren Datenbank – also fügen wir Daten hinzu.

Wir wollen folgende Daten in unsere sqlite-Datenbank bekommen: [swissNAMES3D](https://www.swisstopo.admin.ch/de/landschaftsmodell-swissnames3d). 

Wir haben vorher lediglich die Daten von Semikolon-separiert zu Komma-separiert geändert.

Wir haben auch die Koordinaten vom schweizerisch-liechtensteinischen Georeferenzsystem (EPSG:2056) auf das globale Koordinatensystem (EPSG:4326) übersetzt, damit die Karte nachher auch funktioniert. Auch dies können wir mit `sqlite-utils`, aber leider nicht hier auf Codespaces.

Beende die laufende Datasette-Instanz mit der leeren Datenbank, indem du die Tastenkombination **Ctrl+C** im laufenden Terminal betätigst.

Installiere `sqlite-utils`:

```bash
pipx install sqlite-utils
```

Bestätige die Installation:

```bash
sqlite-utils --version
```

Importiere die bereitgestellten Daten in die vorher erstellte Datenbank:

```bash
sqlite-utils insert data.db linien \
    swissNAMES3D_LIN.csv \
    --csv -d
```

Dies erzeugt eine Tabelle `linien` mit allen Liniengeometrien des swissNAMES3D-Datensatzes. Dies beinhaltet unter anderem:

* Namen von Verkehrsbauten (Brücken, Tunnels, Seilbahnen, usw.)
* Namen von Sportanlagen
* Namen von Fliessgewässern

See for yourself

```bash
datasette data.db
```

Nun kannst du auch schon mit Facetten spielen. Was passiert zum Beispiel, wenn du bei **Suggested facets** auf `OBJEKTART` klickst?

Wenn gewünscht und Zeit, können auch die anderen beiden Tabellen noch hinzugefügt werden. Bennene die beiden anderen Tabellen `punkte` & `polygone`.

---

## Schritt 5: Plugins installieren

Stoppe den Datasette-Server mit **Ctrl+C** im entsprechenden Terminal, wenn er noch läuft.

Leider sind die Koordinaten (in den Spalten `E` und `N`) noch nicht nutzbar für Datasette, um sie toll auf einer Karte darzustellen. 
Deswegen wollen wir noch folgende Plugins installieren:

```bash
datasette install datasette-edit-schema
```
um die Spaltennamen zu ändern

```bash
datasette install datasette-cluster-map
```
um Karten anzuzeigen.

Installiere weitere gewünschten [Plugins](https://datasette.io/plugins), falls die Zeit es erlaubt.

---

## Schritt 6: Daten auf einer Karte anzeigen

Starte Datasette erneut. Dieses Mal aber als `root`:

```bash
datasette data.db --root
```

Öffne in Datasette die Tabelle **linien**.

Sie enthält Spalten **E** und **N**, die Längen- und Breitengradwerte darstellen – der Cluster-Map-Renderer benötigt jedoch **longitude** und **latitude**.

Nutze das Schema-Editor-Plugin, um die Spalten umzubenennen:

* `E` → `longitude`
* `N` → `latitude`

Klicke auf das Zahnrad-Symbol → *Edit table schema* → Änderungen übernehmen.

<img src="https://github.com/DCC-BS/codespaces-datasette/blob/main/edit_schema.png?raw=true" alt="Tabellenschema ändern" width=50% height=50%>

Wenn das geklappt hat, kannst du gleich nochmal den Datasette-Server mit **Ctrl+C** im entsprechenden Terminal stoppen.

Nun wollen wir die Koordinaten vom schweizerisch-liechtensteinischen Georeferenzsystem (EPSG:2056) auf das globale Koordinatensystem (EPSG:4326) übersetzen, damit die Karte nachher auch funktioniert. Auch dies können wir mit `sqlite-utils`

```bash
sqlite-utils query data.db "SELECT InitSpatialMetaData(1);" --load-extension=mod_spatialite.dll 
```

und dann

```bash
sqlite-utils query data.db "UPDATE linien SET longitude = X(ST_Transform(MakePoint(longitude, latitude, 2056), 4326)), latitude = Y(ST_Transform(MakePoint(longitude, latitude, 2056), 4326));" --load-extension=mod_spatialite.dll 
```

Dann kannst du `datasette` wieder starten. Dann aber mit folgender Flag:

```bash
datasette data.db --load-extension=mod_spatialite.dll 
```

Zurück in der Tabellenansicht solltest du nun eine Karte der Schweiz sehen, mit allen Koordinaten der Linien.

---

Dieses Tutorial basiert auf folgendem Tutorial: [Using Datasette in GitHub Codespaces](https://datasette.io/tutorials/codespaces).