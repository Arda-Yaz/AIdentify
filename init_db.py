import sqlite3

def add_questions():
    questions = [
        "What is your favorite color?",
        "How often do you exercise?",
        "Do you enjoy socializing with others?"
    ]

    conn = sqlite3.connect('data/aidentify.db')
    c = conn.cursor()

    for question in questions:
        c.execute("INSERT INTO questions (question_text) VALUES (?)", (question,))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_questions()