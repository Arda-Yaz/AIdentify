import streamlit as st
from supabase import create_client

supa_url = "https://pzbbixzhrbculvcodjla.supabase.co"
supa_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB6YmJpeHpocmJjdWx2Y29kamxhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg1MTY1MjksImV4cCI6MjA2NDA5MjUyOX0.uxhFp8ugGKEwCd31Dy-GQk1ByFlf74bDacSu8Dal98w"

supabase= create_client(supa_url, supa_key)

st.set_page_config(page_title="AIdentify", layout="centered")

from questions import questions, trait_scores
from utils.utils import get_user_id, language

texts = {
    "TR": {
        "head": "🧠 AIdentify",
        "title": "Kişilik Testine Hoş Geldiniz",
        "intro": "Lütfen aşağıdaki soruları cevaplayınız."
    },
    "EN": {
        "head": "🧠 AIdentify",
        "title": "Welcome to the Personality Test",
        "intro": "Please answer the questions below."
    }
}
lang = language()
st.title(texts[lang]["head"])

user_id = get_user_id()

st.title(texts[lang]["title"])
st.subheader(texts[lang]["intro"])

st.divider()
answers = {}

for i, (key, text) in enumerate(questions.items(), start=1):
    slider_key = f"{key}_{user_id}"
    st.markdown(f"<div style='padding-top: 70px;font-size:18px; font-weight:bold'>{i}.{text[lang]}</div>", unsafe_allow_html=True)
    response = st.slider("", 1, 5, 3, key=slider_key)
    answers[key] = response


if st.button("Cevapları Kaydet / Submit Answers"):
    for key, answer in answers.items():
        trait = questions[key]["trait"]
        reverse = questions[key]["reverse"]

        score = 6 - answer if reverse else answer

        trait_scores[trait].append(score)

    final_scores = {trait: round(sum(scores) / len(scores), 2)
                    for trait, scores in trait_scores.items()}


    data = {
        "user_id": user_id,
        "openness": final_scores["Openness"],
        "conscientiousness": final_scores["Conscientiousness"],
        "extroversion": final_scores["Extraversion"],
        "agreeableness": final_scores["Agreeableness"],
        "neuroticism": final_scores["Neuroticism"],
        "mbti_type": None,
        "ai_summary": None,
        "feedback": None
    }
    response = supabase.table("user_results").insert(data).execute()



