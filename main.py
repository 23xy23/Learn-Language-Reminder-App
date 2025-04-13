import requests
import time
from keep_alive import keep_alive
from database import get_task_by_day, get_quizzes_by_task_id

# Replace with your actual values
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
CHAT_ID = "PASTE_YOUR_CHAT_ID_HERE"

# Simulated memory store for incorrect quiz questions (in real usage, use a database or persistent file)
retry_store = {}

keep_alive()

# Loop through a fixed number of days (you can make this dynamic by querying the DB for total days)
for day in range(1, 15):
    task = get_task_by_day(day)
    if not task:
        print(f"No task found for day {day}.")
        continue

    message = f"Day {day} - Your French Task: {task['task_text']}\nResources: {task['resource_links']}"
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                 params={"chat_id": CHAT_ID, "text": message})
    print(f"Sent task: {message}")

    quizzes = get_quizzes_by_task_id(task["task_id"])
    for quiz in quizzes:
        poll_data = {
            "chat_id": CHAT_ID,
            "question": quiz['question'],
            "options": quiz['options'],
            "type": "quiz",
            "correct_option_id": quiz['correct_option_id']
        }
        response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll", json=poll_data)
        print(f"Sent poll: {quiz['question']}")

        user_got_it_wrong = False  # Replace this with real check later
        if user_got_it_wrong:
            retry_store.setdefault(day + 2, []).append(quiz)

        time.sleep(5)  # avoid flooding

    if day in retry_store:
        for retry_quiz in retry_store[day]:
            retry_data = {
                "chat_id": CHAT_ID,
                "question": f"[RETRY] {retry_quiz['question']}",
                "options": retry_quiz['options'],
                "type": "quiz",
                "correct_option_id": retry_quiz['correct_option_id']
            }
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll", json=retry_data)
            print(f"Re-sent retry quiz: {retry_quiz['question']}")
            time.sleep(5)

    confirm_poll = {
        "chat_id": CHAT_ID,
        "question": "Have you completed today's task?",
        "options": ["Yes", "No"],
        "type": "regular",
        "is_anonymous": False
    }
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll", json=confirm_poll)
    print("Sent daily completion confirmation poll.")

    time.sleep(86400)
