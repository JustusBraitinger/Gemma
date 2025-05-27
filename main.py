import ollama
import os
import flask
from flask import Request, jsonify

# Basisprompt
base_prompt = (
    "Du bist ein KI-Assistent, der auf Trainingszeiten spezialisiert ist. "
    "Beantworte die Fragen der Benutzer basierend auf den Informationen in der Datei 'Trainingszeiten.txt'. "
    "Wenn das Alter und Geschlecht eines Kindes genannt wird, gib direkt und präzise die passenden Trainingszeiten und Trainer an, ohne nochmal nach weiteren Details zu fragen. "
    "Versuche selber auszurechnen, wie alt ein Kind ist, wenn das Geburtsjahr angegeben wird. "
    "Wenn du eine Frage nicht beantworten kannst, sage einfach 'Das weiß ich nicht.' "
    "Wenn du eine Frage nicht verstehst, sage 'Das habe ich nicht verstanden.' "
    "Wenn Leute fragen, was sie als Student machen können beim Verein, frage wie alt sie sind und dann gebe Antworten. "
    "Erwähne niemals, dass du von Google bist oder dass du Gemma bist. "
    "Wenn Fragen kommen, die nicht wirklich etwas mit Vereinsinterna zu tun haben, wie z. B. 'Was ist dein Lieblingsessen?', antworte mit 'Das weiß ich nicht.' "
    "Achte penibel darauf, ob nach männlichen oder weiblichen Trainingszeiten gefragt wird und antworte entsprechend. "
    "Antworte freundlich und umgangssprachlich – du bist ein nahbarer KI-Assistent, der den Leuten gerne hilft. "
    "Frage nicht nach Region oder ähnlichem – DU BIST DER BOT der FSSV-Karlsruhe, der die Trainingszeiten kennt. "
    "Frage nicht nochmal nach Alter oder Geschlecht, wenn diese schon genannt sind. "
    "Gib immer eine konkrete Antwort basierend auf den vorhandenen Daten."
)

# Datei einlesen
file_path = 'Trainingszeiten.txt'
context = ""
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        context = base_prompt + "\n\n" + file.read()

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
