import streamlit as st
st.set_page_config(page_title="AIdentify", layout="centered")

from questions import questions
from utils.utils import get_user_id, language

texts = {
    "TR": {
        "head": "🧠 Kişilik Testi",
        "title": "Kişilik Testine Hoş Geldiniz",
        "intro": "Lütfen aşağıdaki soruları cevaplayınız."
    },
    "EN": {
        "head": "🧠 Personality Test",
        "title": "Welcome to the Personality Test",
        "intro": "Please answer the questions below."
    }
}
lang = language()
st.title(texts[lang]["head"])

user_id = get_user_id()

st.title(texts[lang]["title"])
st.write(texts[lang]["intro"])

# Soruları göster
st.subheader("Sorular")
answers = {}

for key, text in questions.items():
    slider_key = f"{key}_{user_id}"
    response = st.slider(text[lang], 1, 5, 3, key=slider_key)
    answers[key] = response

st.write(answers)
# Gönder butonu
if st.button("Cevapları Kaydet / Submit Answers"):
    st.success("Cevaplar kaydedildi!")
    st.json(answers)


