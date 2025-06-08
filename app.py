import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
HF = os.getenv("HUGGINGFACE_API_TOKEN")
SU = os.getenv("SUPA_URL")
SK = os.getenv("SUPA_KEY")

supabase = create_client(SU,SK)

st.set_page_config(page_title="AIdentify", layout="centered")

from questions import questions, trait_scores
from utils.utils import get_user_id, language, check_test_completed, big5_to_mbti_weighted, ai_summary,query_huggingface_model

texts = {
    "TR": {
        "head": "🧠 AIdentify",
        "title": "Kişilik Testine Hoş Geldiniz",
        "intro": "Lütfen aşağıdaki soruları cevaplayınız.",
        "button": "Testi tekrarla",
        "submit": "Cevapları Kaydet"
    },
    "EN": {
        "head": "🧠 AIdentify",
        "title": "Welcome to the Personality Test",
        "intro": "Please answer the questions below.",
        "button": "Again",
        "submit": "Submit Answers"
    }
}
lang = language()
st.title(texts[lang]["head"])

user_id = get_user_id()
show_test = check_test_completed(user_id)

if show_test:
    response = supabase.table("user_results").select("ai_summary").eq("user_id", user_id).order("created_at", desc=True).limit(1).execute()
    if response.data:
        st.text_area("AIdentify", response.data[0]["ai_summary"], height=400)
        if texts[lang] == "TR":
            st.write("Modelin türkçe cevaplarda performansı büyük oranda düşüşe uğradığı için cevap ingilizce olarak sağlanmıştır.")

    if st.button(texts[lang]["button"]):
        supabase.table("user_results").update({"finished_test": False}).eq("user_id", user_id).execute()
        st.rerun()

else:
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

        final_scores["mbti_type"] = big5_to_mbti_weighted(final_scores)

        prompt = ai_summary(final_scores)
        ai_response = query_huggingface_model(prompt)
        data = {
            "user_id": user_id,
            "openness": final_scores["Openness"],
            "conscientiousness": final_scores["Conscientiousness"],
            "extroversion": final_scores["Extraversion"],
            "agreeableness": final_scores["Agreeableness"],
            "neuroticism": final_scores["Neuroticism"],
            "mbti_type": final_scores["mbti_type"],
            "ai_summary": ai_response,
            "finished_test": True
        }


        response = supabase.table("user_results").insert(data).execute()





