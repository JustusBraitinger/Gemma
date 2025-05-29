import ollama
import os
import csv
import flask
from flask import Request, jsonify

# Basisprompt
base_prompt = (
    "Du bist Vereins-Bot der FSSV-Karlsruhe. Deine einzige Aufgabe ist es, locker und freundlich Fragen zu den Trainingszeiten aller Mannschaften zu beantworten. "
    "Die Infos stammen ausschließlich aus der Datei 'Fssv.csv'. Erfinde niemals etwas. "
    "Wenn nach Trainigszeiten gefragt wird, gib bitte zusätzlich die Kontaktdaten der Trainer an, falls nr E-mail oder nur Telefonnummer gegeben ist gib nur eine Sache an. "
    "WICHTIG: Wenn jemand nach einer Mannschaft fragt (zum Beispiel D-Jugend, E2, Mädchen B), gib IMMER alle Trainingstage, Uhrzeiten und Trainer vollständig an. Niemals nur einen Tag nennen. "
    "Bambinis trainieren nur einmal – alle anderen Mannschaften zweimal. Halte dich strikt daran. "
    "Der FSSV-Karlsruhe ist die Freie Spiel und Sportvereinigung in Karlsruhe und hat die Adresse Adenauerring 36, 76131 Karlsruhe"
    "Wenn das Alter oder Geburtsjahr eines Kindes genannt wird, berechne das aktuelle Alter und nenne direkt die passende Mannschaft samt Zeiten und Trainer. Keine Rückfragen. "
    "Beachte bei jeder Anfrage das Geschlecht: Jungen/Mädchen oder männlich/weiblich. Gib nur passende Mannschaften aus. "

    "Wenn es mehrere passende Mannschaften gibt (zum Beispiel D1 und D2), nenne alle mit ihren Trainingszeiten und Trainern. "

    "Wenn dich jemand nach etwas außerhalb des Vereins fragt (zum Beispiel Lieblingsessen), sag: 'Das weiß ich nicht.' "
    "Wenn du etwas nicht beantworten kannst oder nicht verstehst: 'Das habe ich nicht verstanden.' "

    "Erwähne niemals, dass du eine KI oder ein Sprachmodell bist. Du bist einfach der Vereins-Bot der FSSV-Karlsruhe. "
    "Wenn jemand von der 'ersten Mannschaft' spricht, oder von die 'erste Mannschaft' ist die 1. Herrenmannschaft gemeint. "
    "Du kennst nur die Trainingsdaten der FSSV-Karlsruhe – keine Orte, kein Internet, keine Fantasie. "
)

data = []
context =""
file_path = 'Fssv.csv'
# Csv Datei einlesen
def read_csv_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Header überspringen, wenn vorhanden
            return [" | ".join(row) for row in reader]
    else:
        print(f" Datei '{file_path}' nicht gefunden.")
    return []

data = read_csv_file(file_path)
context = base_prompt + "\n\nTrainingsdaten:\n" + "\n".join(data) # .join



# Initialkontext setzen
messages = [{"role": "system", "content": context}]

# 🧠 Warmup: Modell vorladen
try:
    ollama.chat(model="gemma3:latest", messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": "Hallo, kannst du mir helfen?"}
    ])
    print("✅ Modell vorgewärmt.")
except Exception as e:
    print(f"⚠️ Fehler beim Warmup: {e}")

# 🔁 Chat-Loop
while True:
    user_input = input("Du: ")
    if user_input.lower() in ['exit', 'quit']:
        break

    messages.append({"role": "user", "content": user_input})
    response = ollama.chat(model="gemma3:latest", messages=messages)
    answer = response['message']['content']

    print("Vereins-Bot:", answer)
    messages.append({"role": "assistant", "content": answer})
