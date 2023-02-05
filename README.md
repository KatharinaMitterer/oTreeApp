# Gruppe 3

Willkommen zur Abgabe für die Bonuspunkte von Gruppe3!

## Gruppe 3

Gruppe 3 besteht aus Daniel Hamm, Katharina Mitterer und Emil Stefko

## Git-Repository

Unser Projekt ist in Gitlab unter https://git.scc.kit.edu/ws2022-ewf-bonus/gruppe03.git abgespeichert

## Thema

Wir haben eine Umfrage zum Thema "Confirmation Bias" erstellt. Unser Experiment befindet sich im Ordner 
<i>Experiment</i>. In diesem Ordner wird auch noch einmal genau der Aufbau des Experiments erklärt. Viel Spaß!

## Erste Schritte

In requirements.txt stehen alle benötigten Python-Bibliotheken. 
Der devserver wird gestartet mit:

```
cd <Pfad zu settings.py>
otree devserver
```

## Struktureller Aufbau und Hintergrund zum Experiment

Dieses Experiment zielt darauf ab, 
den Confirmation Bias zu verstehen. 
Es umfasst 4 Fragen zu den Themen Klimawandel und Atomenergie. <br>
<br>
<i>Anweisung.html</i> dient als 1. Seite des Experiments als Einführung und Anweisung für einen Spieler. <br>
In den ersten beiden Fragen wird jeweils gefragt, wie jemand zu dem Thema eingestellt ist (<i>Vorab_Fragen.html</i>).
Dann folgen 2 Schätzfragen (<i>Schaetzfrage1.html</i> und <i>Schaetzfrage2.html</i>), bei denen man die CO2-Emissionen 
seit 1990 und den Anteil des Stromes, 
der durch Atomkraftwerke gewonnen wird, schätzen soll. Anschließend werden die Ergebnisse der Schätzfragen 
in einem Histogramm dargestellt, ebenso kann man seine eigene Positionierung zu den Themen einsehen
(<i>Ergebnisse1.html</i> und <i>Ergebnisse2.html</i>). 
Die Mediane der gruppierten Daten von den vorherigen Teilnehmern werden ebenfalls aufgeteilt 
nach ihrer Positionierung dargestellt. 
Das Ziel ist es, den Einfluss der eigenen Einstellung auf die Schätzungen zu veranschaulichen, 
was ein Beispiel für den Confirmation Bias ist. <br>
Am Ende (<i>Ende.html</i>) wird den Teilnehmern für die Teilnahme am Experiment gedankt und ein Link zur Registrierung 
fürs KD<sup>2</sup>lab bereitgestellt. <br>
<br>
Bilder von den Histogrammen (mit Matplotlib geplottet) für die Ergebnisse aller bisherigen Spieler befinden sich im 
Ordner <i>_static</i>. <br>
Daten aller bisherigen Spieler befinden sich im Ordner <i>_rooms</i> in der Datei: <i>gruppe3_room.txt</i> 


