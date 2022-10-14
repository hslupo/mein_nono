# mein_nono
 mein zweiter Versuch

angeregt durch @MountyRox im Kanal von @Gravitar64 haben wir uns mit dem Lösen von Nonogrammen versucht, 
mein Ansatz war das Lösen des Rätsel auch zu visualisieren. Mein erster Versuch hat funktioniert,
dauerte aber bei Dimensionen über 20x20 zu lang, so habe ich mich mit Hilfe einer anderen fremden Solver versucht
eine bessere Lösung zu finden. Der Artikel von Hennie de Harder und ihren Ansatz 
(https://towardsdatascience.com/solving-nonograms-with-120-lines-of-code-a7c6e0f627e4) habe ich als Ausgangspunkt genommen
und um meine Visualisierung erweitert.

nono.py
Das Programm lässt mich ein Beispiel-Rätsel auswählen (Ordner raetsel) und versucht es zu lösen,
wenn das klappt zeigt es mir das Ergebnis auf dem Bildschirm. Die Entstehung der Lösung
kann ich mir dann animiert anzeigen lassen.
Nach dem schließen des Rätsels bin ich wieder im Dateiauswahl-Dialog, solange ich Dateien auswähle geht das so weiter

Datenformat Beispiel:

4, 2 1, 1 1,2 ,2<br/>
4, 2 2,1, 1, 3

zuerst der Spaltenkopf, dann Zeilenkopf
<img width="184" alt="image" src="https://user-images.githubusercontent.com/77671905/195946376-975dcfbe-3040-4910-8437-c10160131889.png">


Taste | Funktion
---|---
a| Animation starten
Leertaste | Pause an/aus
Pfeil hoch ↑ | Animation schneller
Pfeil runter ↓ | Animation langsamer
'+' oder '-' | Darstellung größer / kleiner


nicht eindeutig lösbare Rätsel werden mit rotem Hintergrund gezeigt.
Leider sind große Rätsel immer noch sehr zeitaufwändig
