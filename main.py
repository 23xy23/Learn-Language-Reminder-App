import requests
import time
from keep_alive import keep_alive
keep_alive()


# Replace with your actual values
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
CHAT_ID = "PASTE_YOUR_CHAT_ID_HERE"

# Simulated memory store for incorrect quiz questions (in real usage, use a database or persistent file)
retry_store = {}

# Daily messages and multiple vocab quizzes per day
daily_tasks = [
    {
        "task": "👋 Bonjour! Day 1: Learn greetings like Bonjour, Salut, Merci.\nResources:\n- Duolingo: https://www.duolingo.com/course/fr/en/Learn-French\n- YouTube: https://www.youtube.com/watch?v=IMcbfQZ1Hs8\n- Flashcards: https://quizlet.com/subject/french-greetings/",
        "quizzes": [
            {
                "question": "What does 'Bonjour' mean?",
                "options": ["Goodbye", "Please", "Hello", "Thank you"],
                "correct_option_id": 2
            },
            {
                "question": "What does 'Merci' mean?",
                "options": ["Sorry", "Thanks", "Hello", "Please"],
                "correct_option_id": 1
            },
            {
                "question": "What does 'Salut' mean?",
                "options": ["Cheers", "Hi/Bye", "No", "See you later"],
                "correct_option_id": 1
            }
        ]
    },
    {
        "task": "🎧 Day 2: Practice French pronunciation with YouTube videos.",
        "quizzes": [
            {
                "question": "Which letter is often silent at the end of French words?",
                "options": ["E", "T", "X", "S"],
                "correct_option_id": 0
            },
            {
                "question": "How do you pronounce 'r' in French?",
                "options": ["Guttural", "Like English R", "Silent", "Rolled"],
                "correct_option_id": 0
            },
            {
                "question": "Which sound does 'ou' make in French?",
                "options": ["oo", "ow", "ay", "uh"],
                "correct_option_id": 0
            }
        ]
    },
    {
        "task": "🗣️ Day 3: Practice saying your name in French: 'Je m'appelle...'.",
        "quizzes": [
            {
                "question": "What does 'Je m'appelle' mean?",
                "options": ["I live in", "I work at", "My name is", "Nice to meet you"],
                "correct_option_id": 2
            },
            {
                "question": "How do you say 'I am from Singapore' in French?",
                "options": ["Je suis Singapour", "Je viens de Singapour", "Je habite à Singapour", "Je suis né Singapour"],
                "correct_option_id": 1
            },
            {
                "question": "What is 'Nice to meet you' in French?",
                "options": ["Enchanté", "Bonsoir", "Bonjour", "Merci"],
                "correct_option_id": 0
            }
        ]
    },
    {
        "task": "📝 Day 4: Listen to Coffee Break French Ep.1Resources:- Coffee Break French: https://coffeebreaklanguages.com/french/",
        "quizzes": [
            {
                "question": "What does 'Comment ça va ?' mean?",
                "options": ["What’s your name?", "How are you?", "Where do you live?", "Can I help you?"],
                "correct_option_id": 1
            },
            {
                "question": "Which phrase means 'See you soon'?",
                "options": ["À demain", "Bonne nuit", "À bientôt", "Au revoir"],
                "correct_option_id": 2
            },
            {
                "question": "What does 'Je vais bien' mean?",
                "options": ["I'm okay", "I’m late", "I’m going home", "I need help"],
                "correct_option_id": 0
            }
        ]
    },
    {
        "task": "✍️ Day 5: Write 3 lines about yourself in French.\nResources:\n- Writing tips: https://www.lawlessfrench.com/writing/",

        "quizzes": [
            {
                "question": "Which verb means 'to be'?",
                "options": ["avoir", "aller", "être", "faire"],
                "correct_option_id": 2
            },
            {
                "question": "What’s the French for 'I live in Singapore'?",
                "options": ["Je habite à Singapour", "Je suis Singapour", "Je vis à Singapour", "Je reste Singapour"],
                "correct_option_id": 2
            },
            {
                "question": "What does 'J’ai 20 ans' mean?",
                "options": ["I’m 20 years old", "I’ve been here 20 years", "I have 20 friends", "I arrived at 20"],
                "correct_option_id": 0
            }
        ]
    },
    {
        "task": "📺 Day 6: Watch Extra en français S1E1 (YouTube)Resources:- Episode Link: https://www.youtube.com/watch?v=QkHQ0CYwjaI",
        "quizzes": [
            {
                "question": "Who is the main character who gets a letter?",
                "options": ["Pablo", "Sam", "Lola", "Sacha"],
                "correct_option_id": 3
            },
            {
                "question": "What does Sam struggle with?",
                "options": ["Cooking", "Driving", "Speaking French", "Finding friends"],
                "correct_option_id": 2
            },
            {
                "question": "What is Sam’s nationality?",
                "options": ["French", "English", "American", "Canadian"],
                "correct_option_id": 2
            }
        ]
    },
    {
        "task": "🧪 Day 7: Review flashcards and Duolingo checkpointResources:- Duolingo Checkpoint: https://www.duolingo.com/",
        "quizzes": [
            {
                "question": "What does 'répéter' mean?",
                "options": ["To draw", "To repeat", "To read", "To write"],
                "correct_option_id": 1
            },
            {
                "question": "Which one is a French verb meaning 'to have'?",
                "options": ["faire", "être", "aller", "avoir"],
                "correct_option_id": 3
            },
            {
                "question": "What does 'bonne chance' mean?",
                "options": ["Good night", "Good morning", "Good luck", "Goodbye"],
                "correct_option_id": 2
            }
        ]
    },
    {
        "task": "🧮 Day 8: Learn numbers & shopping phrases.\nResources:\n- Numbers 1–100: https://youtu.be/CjN1WQl9x4U\n- Shopping in French: https://youtu.be/LI9V3Y4nD0g",
        "quizzes": [
            {
                "question": "What is the French word for 'twenty'?",
                "options": ["vingt", "dix", "trente", "quinze"],
                "correct_option_id": 0
            },
            {
                "question": "How do you say 'How much is it?' in French?",
                "options": ["Combien ça coûte ?", "Où est le prix ?", "Quel prix ?", "Ça coûte combien cher ?"],
                "correct_option_id": 0
            },
            {
                "question": "What does 'Je voudrais acheter...' mean?",
                "options": ["I’m looking for...", "I want to go to...", "I would like to buy...", "Do you sell..."],
                "correct_option_id": 2
            }
        ]
    },
    {
        "task": "🕐 Day 9: Telling time in French.\nResources:\n- Clock Reading: https://www.youtube.com/watch?v=dqB7GxH40y0",
        "quizzes": [
            {
                "question": "What does 'Il est huit heures' mean?",
                "options": ["It’s eight o’clock", "It’s ten o’clock", "It’s one o’clock", "It’s midnight"],
                "correct_option_id": 0
            },
            {
                "question": "How do you say 'quarter past four' in French?",
                "options": ["Quatre et quart", "Quatre heures quinze", "Quatre quinze", "Quinze de quatre"],
                "correct_option_id": 0
            },
            {
                "question": "What does 'midi' refer to in French?",
                "options": ["Midnight", "Morning", "Afternoon", "Noon"],
                "correct_option_id": 3
            }
        ]
    },
    {
        "task": "🗺️ Day 10: Asking for directions.\nResources:\n- Directions Vocabulary: https://youtu.be/WKYB9Z3Jtz4",
        "quizzes": [
            {
                "question": "What does 'à gauche' mean?",
                "options": ["To the right", "Straight ahead", "To the left", "At the back"],
                "correct_option_id": 2
            },
            {
                "question": "What does 'Où est la gare ?' mean?",
                "options": ["Where is the park?", "Where is the station?", "Where is the hotel?", "Where is the bus stop?"],
                "correct_option_id": 1
            },
            {
                "question": "What does 'C’est loin ?' mean?",
                "options": ["Is it far?", "Is it safe?", "Is it here?", "Is it new?"],
                "correct_option_id": 0
            }
        ]
    },
    {
        "task": "🎧 Day 11: Listening Practice with FrenchPod101.\nResources:\n- FrenchPod101 Supermarket Ep: https://youtu.be/Sv8NJlzuSrM",
        "quizzes": [
            {
                "question": "What does 'le supermarché' mean?",
                "options": ["The market", "The convenience store", "The supermarket", "The shopping mall"],
                "correct_option_id": 2
            },
            {
                "question": "What is 'panier' in a French shop?",
                "options": ["Fridge", "Shelf", "Bag", "Basket"],
                "correct_option_id": 3
            },
            {
                "question": "What does 'payer par carte' mean?",
                "options": ["Pay by cash", "Pay by card", "Ask for change", "Split the bill"],
                "correct_option_id": 1
            }
        ]
    },
    {
        "task": "🗣️ Day 12: Speaking Practice – Asking for prices.\nResources:\n- Sample Dialogue: https://youtu.be/IxlO14vuoEo",
        "quizzes": [
            {
                "question": "What does 'C’est combien ?' mean?",
                "options": ["How many?", "How is it?", "How much is it?", "How fast?"],
                "correct_option_id": 2
            },
            {
                "question": "What is the French for 'I would like some bread'?",
                "options": ["Je prends du pain", "Je veux pain", "Je voudrais du pain", "Du pain s’il vous plaît"],
                "correct_option_id": 2
            },
            {
                "question": "What does 'C’est trop cher' mean?",
                "options": ["It’s too far", "It’s expensive", "It’s broken", "It’s too small"],
                "correct_option_id": 1
            }
        ]
    },
    {
        "task": "📺 Day 13: Watch Tivi5 Monde Plus kids show.\nResources:\n- Watch Site: https://www.tv5mondeplus.com",
        "quizzes": [
            {
                "question": "What does 'bonjour tout le monde' mean?",
                "options": ["Good night everyone", "Hello everyone", "Goodbye everyone", "Everyone’s busy"],
                "correct_option_id": 1
            },
            {
                "question": "What does 'regarde ça!' mean?",
                "options": ["Stop it!", "Do it again!", "Look at that!", "Get it now!"],
                "correct_option_id": 2
            },
            {
                "question": "What does 'amusant' mean?",
                "options": ["Tiring", "Funny", "Noisy", "Hard"],
                "correct_option_id": 1
            }
        ]
    },
    {
        "task": "✍️ Day 14: Recap & write a short entry.\nResources:\n- Sentence Starters: https://www.lawlessfrench.com/writing/",
        "quizzes": [
            {
                "question": "How do you say 'I went to the market' in French?",
                "options": ["Je suis allé au marché", "Je vais au marché", "J’ai marché au marché", "Je prends le marché"],
                "correct_option_id": 0
            },
            {
                "question": "How do you write 'I bought vegetables'?",
                "options": ["Je prends des légumes", "J’achète légumes", "J’ai acheté des légumes", "Je suis légumes"],
                "correct_option_id": 2
            },
            {
                "question": "How do you say 'It was fun' in French?",
                "options": ["C’était drôle", "C’est fun", "C’était amusant", "Il était bon"],
                "correct_option_id": 2
            }
        ]
    }

]

# Loop through each day
for day, entry in enumerate(daily_tasks, start=1):
    # Send reminder message
    message = f"Day {day}/{len(daily_tasks)} - Your French Task: {entry['task']}"
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                 params={"chat_id": CHAT_ID, "text": message})
    print(f"Sent task: {message}")

    # Send multiple quizzes with retry mechanism placeholder
    for quiz_index, quiz in enumerate(entry['quizzes']):
        poll_data = {
            "chat_id": CHAT_ID,
            "question": quiz['question'],
            "options": quiz['options'],
            "type": "quiz",
            "correct_option_id": quiz['correct_option_id']
        }
        response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll", json=poll_data)
        print(f"Sent poll: {quiz['question']}")

        # Simulate response check (placeholder logic for retry tracking)
        # In real use, check actual poll responses via Telegram webhook
        user_got_it_wrong = False  # Replace this with real check later
        if user_got_it_wrong:
            retry_store.setdefault(day + 2, []).append(quiz)

        time.sleep(5)  # avoid flooding

    # Resend quizzes marked for retry
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

    # Send a poll to check if user completed the task
    confirm_poll = {
        "chat_id": CHAT_ID,
        "question": "Have you completed today's task?",
        "options": ["Yes", "No"],
        "type": "regular",
        "is_anonymous": False
    }
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll", json=confirm_poll)
    print("Sent daily completion confirmation poll.")

    # Wait 24 hours before next (adjust or remove for testing)
    time.sleep(86400)
