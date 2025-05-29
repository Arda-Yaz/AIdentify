import streamlit as st
st.set_page_config(page_title="AIdentify", layout="centered")

from questions import questions
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

st.write(answers)
if st.button("Cevapları Kaydet / Submit Answers"):
    st.success("Cevaplar kaydedildi!")
    st.json(answers)


