import os
import random
from flask import Flask, render_template, jsonify, request, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')

ANIMALS = [
    {"animal": "Лев", "habitat": "Саванна", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Lion_waiting_in_Namibia.jpg/800px-Lion_waiting_in_Namibia.jpg"},
    {"animal": "Пингвин", "habitat": "Антарктида", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Emperor_Penguin_Manchot_empereur.jpg/800px-Emperor_Penguin_Manchot_empereur.jpg"},
    {"animal": "Бурый медведь", "habitat": "Тайга", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Kamchatka_Brown_Bear_near_Dvuhyurtochnoy_on_2015-07-23.jpg/800px-Kamchatka_Brown_Bear_near_Dvuhyurtochnoy_on_2015-07-23.jpg"},
    {"animal": "Кенгуру", "habitat": "Австралия", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Kangaroo_and_joey03.jpg/800px-Kangaroo_and_joey03.jpg"},
    {"animal": "Верблюд", "habitat": "Пустыня", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/DromedaryCamel.JPG/800px-DromedaryCamel.JPG"},
    {"animal": "Дельфин", "habitat": "Океан", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Tursiops_truncatus_01.jpg/800px-Tursiops_truncatus_01.jpg"},
    {"animal": "Горилла", "habitat": "Тропический лес", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Mountain_gorilla_%28Gorilla_beringei_beringei%29.jpg/800px-Mountain_gorilla_%28Gorilla_beringei_beringei%29.jpg"},
    {"animal": "Полярная сова", "habitat": "Тундра", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Bubo_scandiacus_2_%28Martin_Mecnarowski%29.jpg/800px-Bubo_scandiacus_2_%28Martin_Mecnarowski%29.jpg"},
    {"animal": "Жираф", "habitat": "Саванна", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Giraffe_Mikumi_National_Park.jpg/800px-Giraffe_Mikumi_National_Park.jpg"},
    {"animal": "Крокодил", "habitat": "Реки и болота", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Crocodylus_niloticus-Luambe_National_Park-Zambia-8.jpg/800px-Crocodylus_niloticus-Luambe_National_Park-Zambia-8.jpg"},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    session.clear()
    session['score'] = 0
    session['total'] = 0
    session['current'] = 0
    session['questions'] = random.sample(ANIMALS, min(5, len(ANIMALS)))
    return jsonify({"status": "started"})

@app.route('/question')
def get_question():
    idx = session.get('current', 0)
    questions = session.get('questions', [])
    if idx >= len(questions):
        return jsonify({
            "finished": True,
            "score": session.get('score', 0),
            "total": session.get('total', 0)
        })

    q = questions[idx]
    correct = q['habitat']
    others = [a['habitat'] for a in ANIMALS if a['habitat'] != correct]
    options = [correct] + random.sample(others, min(3, len(others)))
    random.shuffle(options)

    return jsonify({
        "animal": q['animal'],
        "image_url": q['image'],
        "options": options,
        "index": idx
    })

@app.route('/check', methods=['POST'])
def check_answer():
    data = request.get_json()
    selected = data.get('answer')
    idx = session.get('current', 0)
    questions = session.get('questions', [])

    if not questions or idx >= len(questions):
        return jsonify({"error": "Вопрос не найден"}), 400

    correct = questions[idx]['habitat']
    is_correct = selected == correct

    session['score'] = session.get('score', 0) + (1 if is_correct else 0)
    session['total'] = session.get('total', 0) + 1
    session['current'] += 1

    return jsonify({
        "correct": is_correct,
        "correct_answer": correct
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)