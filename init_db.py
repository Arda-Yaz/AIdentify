import sqlite3

def placeholder():
    return print("Placeholder")

def create_table():
    conn = sqlite3.connect("data/aidentify.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS user_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        openness REAL,
        conscientiousness REAL,
        extroversion REAL,
        agreeableness REAL,
        neuroticism REAL,
        mbti_type TEXT,
        ai_summary TEXT,
        feedback TEXT, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    placeholder()