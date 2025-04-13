import sqlite3
import json

def get_connection():
    return sqlite3.connect("french_bot.db")

def get_task_by_day(day_number):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, task_text, resource_links FROM daily_tasks WHERE day_number = ?", (day_number,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "task_id": row[0],
            "task_text": row[1],
            "resource_links": row[2]
        }
    return None

def get_quizzes_by_task_id(task_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT question, options, correct_option_id FROM quizzes WHERE task_id = ?", (task_id,))
    rows = c.fetchall()
    conn.close()
    quizzes = []
    for row in rows:
        quizzes.append({
            "question": row[0],
            "options": json.loads(row[1]),
            "correct_option_id": row[2]
        })
    return quizzes

def record_user_progress(user_id, day_number, completed, wrong_quiz_ids):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO user_progress (user_id, day_number, completed, wrong_quiz_ids) VALUES (?, ?, ?, ?)",
              (user_id, day_number, completed, json.dumps(wrong_quiz_ids)))
    conn.commit()
    conn.close()

def seed_tasks_and_quizzes():
    conn = get_connection()
    c = conn.cursor()

    example_tasks = [
        {
            "day_number": 1,
            "task_text": "👋 Learn greetings like Bonjour, Salut, Merci, Comment ça va?",
            "resource_links": "https://www.duolingo.com/course/fr/en/Learn-French, https://www.youtube.com/watch?v=IMcbfQZ1Hs8"
        },
        {
            "day_number": 2,
            "task_text": "🎧 Practice pronunciation with YouTube videos",
            "resource_links": "https://www.youtube.com/watch?v=CjN1WQl9x4U"
        },
        {
            "day_number": 3,
            "task_text": "🗣️ Practice saying your name in French: 'Je m'appelle...'",
            "resource_links": ""
        },
        {
            "day_number": 4,
            "task_text": "📝 Listen to Coffee Break French Ep.1",
            "resource_links": "https://coffeebreaklanguages.com/french/"
        }
    ]

    example_quizzes = [
        # Day 1
        {"day": 1, "question": "What does 'Bonjour' mean?", "options": ["Goodbye", "Please", "Hello", "Thank you"], "correct_option_id": 2},
        {"day": 1, "question": "What does 'Merci' mean?", "options": ["Sorry", "Thanks", "Hello", "Please"], "correct_option_id": 1},
        # Day 2
        {"day": 2, "question": "Which sound does 'ou' make in French?", "options": ["oo", "ow", "ay", "uh"], "correct_option_id": 0},
        {"day": 2, "question": "How do you pronounce 'r' in French?", "options": ["Guttural", "Like English R", "Silent", "Rolled"], "correct_option_id": 0},
        # Day 3
        {"day": 3, "question": "What does 'Je m'appelle' mean?", "options": ["I live in", "I work at", "My name is", "Nice to meet you"], "correct_option_id": 2},
        {"day": 3, "question": "How do you say 'I am from Singapore' in French?", "options": ["Je suis Singapour", "Je viens de Singapour", "Je habite à Singapour", "Je suis né Singapour"], "correct_option_id": 1},
        # Day 4
        {"day": 4, "question": "What does 'Comment ça va ?' mean?", "options": ["What’s your name?", "How are you?", "Where do you live?", "Can I help you?"], "correct_option_id": 1},
        {"day": 4, "question": "Which phrase means 'See you soon'?", "options": ["À demain", "Bonne nuit", "À bientôt", "Au revoir"], "correct_option_id": 2},
        {"day": 4, "question": "What does 'Je vais bien' mean?", "options": ["I'm okay", "I’m late", "I’m going home", "I need help"], "correct_option_id": 0}
    ]

    # Insert daily tasks
    for task in example_tasks:
        c.execute("INSERT INTO daily_tasks (day_number, task_text, resource_links) VALUES (?, ?, ?)",
                  (task['day_number'], task['task_text'], task['resource_links']))

    conn.commit()

    # Map task_id from DB
    c.execute("SELECT id, day_number FROM daily_tasks")
    id_map = {day: id for id, day in c.fetchall()}

    for quiz in example_quizzes:
        task_id = id_map[quiz['day']]
        options_json = json.dumps(quiz['options'])
        c.execute("INSERT INTO quizzes (task_id, question, options, correct_option_id) VALUES (?, ?, ?, ?)",
                  (task_id, quiz['question'], options_json, quiz['correct_option_id']))

    conn.commit()
    conn.close()
    print("Database seeded with daily tasks and quizzes.")

if __name__ == "__main__":
    seed_tasks_and_quizzes()
