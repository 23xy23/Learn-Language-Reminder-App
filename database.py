import sqlite3
import json

# Connect to database
conn = sqlite3.connect("french_bot.db")
c = conn.cursor()

# Create tables
c.execute("""
CREATE TABLE IF NOT EXISTS daily_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day_number INTEGER NOT NULL,
    task_text TEXT NOT NULL,
    resource_links TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    options TEXT NOT NULL,
    correct_option_id INTEGER NOT NULL,
    FOREIGN KEY(task_id) REFERENCES daily_tasks(id)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    day_number INTEGER NOT NULL,
    completed INTEGER DEFAULT 0,
    wrong_quiz_ids TEXT DEFAULT '[]'
)
""")

# Example data (you'll want to copy in your own)
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
    }
]

example_quizzes = [
    {
        "day": 1,
        "question": "What does 'Bonjour' mean?",
        "options": ["Goodbye", "Please", "Hello", "Thank you"],
        "correct_option_id": 2
    },
    {
        "day": 1,
        "question": "What does 'Merci' mean?",
        "options": ["Sorry", "Thanks", "Hello", "Please"],
        "correct_option_id": 1
    },
    {
        "day": 2,
        "question": "Which sound does 'ou' make in French?",
        "options": ["oo", "ow", "ay", "uh"],
        "correct_option_id": 0
    }
]

# Insert daily tasks
for task in example_tasks:
    c.execute("INSERT INTO daily_tasks (day_number, task_text, resource_links) VALUES (?, ?, ?)",
              (task['day_number'], task['task_text'], task['resource_links']))

# Map task_id from DB
conn.commit()
c.execute("SELECT id, day_number FROM daily_tasks")
id_map = {day: id for id, day in c.fetchall()}

# Insert quizzes
for quiz in example_quizzes:
    task_id = id_map[quiz['day']]
    options_json = json.dumps(quiz['options'])
    c.execute("INSERT INTO quizzes (task_id, question, options, correct_option_id) VALUES (?, ?, ?, ?)",
              (task_id, quiz['question'], options_json, quiz['correct_option_id']))

conn.commit()
conn.close()
print("Database setup and seeded with example tasks + quizzes.")
