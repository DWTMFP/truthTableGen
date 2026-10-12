# Wahrheitstabellengenerierer

## AI

ChatGPT wurde benutzt. Die KI hat einiges von dem Code alleine geschrieben,
wobei er von mir jedoch angepasst wurde, sowohl mit Kommentaren versehen, als
auch Umbennenung und oftmals im Nachhinein angepasst.

## Installation

Python ist benötigt. Download nur von der Offiziellen [python.org](https://www.python.org)

Ebenfalls wird PyYaml benötigt. Installation z. B. über pip:

```python
pip install PyYaml
```

Ich empfehle cmd als Administrator zu starten beim Installierenm, dass das Packet für alle Benutzer Installiert wird,
ist aber nicht notwendig.

## Benutzung

Lade den src Ordner herunter. Öffne den Ordner in der Kommandozeile
und starte truthTableGen.py über python wie folgt:

```python
python truthTableGen.py "AvB" "BvA" "(AvB) <=> (BvA)"
```

Natürlich lassen sich auch andere Verknüpfungen darstellen:

| Name           | Symbol |
|:--------------:|:------:|
| Logisches Und  | v      |
| Logisches Oder | ^      |
| Negation       | !      |
| Äquivalenz     | <=>    |
| Implikation    | =>     |

Nicht vorhandene Operatoren funktionieren auch.
Hierbei gilt nur zu beachten, dass vor und nach ihnen zwingend ein Leerzeichen stehen muss.

Das Verbinden von Argumenten z. B. "A v (B ^ C)" ist ebenfalls erlaubt.

Sollte eine Automatisierte Ausfüllung folgen, so wird diese nur über ein Befehlszeilenargument verfügbar
sein und dort werden die Einschränkungen zu den Operatoren greifen.
Jedoch werden nicht erkannte Operatoren einfach Leergelassen, anstelle von Fehlern zu werfen.
Evtl. gibt es eine kurze Log Nachricht.

### Kommandozeilenargumente

Mit ``python truthTableGen.py -h`` erhält man die Hilfe.

Mit ``python truthTableGen --tex``
IN KOMBINATION MIT EINEM ARGUMENT erhält man die LaTeX Tabelle vor dem Kommandozeilenoutput.

Mit ``python truthTableGen --tex --noCLI`` erhält man die LaTeX Tabelle ohne den Kommandozeilenoutput.

Verwendet man jedoch ``--noCLI`` ohne ``--tex`` so erscheint die Tabelle trotzdem in der Kommandozeile.
