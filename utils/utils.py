import uuid
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from supabase import create_client
import requests
from dotenv import load_dotenv
import os

load_dotenv()

HF = os.getenv("HUGGINGFACE_API_TOKEN")
SU = os.getenv("SUPA_URL")
SK = os.getenv("SUPA_KEY")
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"

supabase= create_client(SU,SK)

def get_user_id():
    cookies = EncryptedCookieManager(
        prefix="aidentify_",
        password = "my_super_secret_password_1234"
    )

    if not cookies.ready():
        st.stop()

    user_id = cookies.get("user_id")

    if user_id is None :
        user_id = str(uuid.uuid4()) #uuid4 for anonymity
        cookies["user_id"] = user_id
        cookies.save()

    return user_id

def language():
    selected = st.radio("Choose Language / Dil Seçiniz", ["EN", "TR"], key="language_select")
    st.session_state.language = selected
    return st.session_state.language

def check_test_completed(user_id: str) -> bool:
    response = supabase.table("user_results").select("finished_test, created_at").eq("user_id", user_id).execute()

    if response.data and len(response.data) > 0:
        latest = max(response.data, key=lambda x: x["created_at"])
        return latest.get("finished_test", False)

    return False

def big5_to_mbti_weighted(scores):
    # The correlation coefficients used here are based on a study published on ResearchGate.
    # Authors: Radha Divi and Chandra Sekhar Potala.
    # Source: https://www.researchgate.net/publication/365004120_Correlation_based_data_unification_for_personality_trait_prediction
    weights = {
        "E": {"Neuroticism": -0.30, "Extraversion": 0.71, "Openness": 0.28, "Agreeableness": -0.02, "Conscientiousness": 0.13},
        "I": {"Neuroticism": 0.31, "Extraversion": -0.72, "Openness": -0.32, "Agreeableness": 0.02, "Conscientiousness": -0.13},

        "S": {"Neuroticism": 0.15, "Extraversion": -0.28, "Openness": -0.66, "Agreeableness": 0.01, "Conscientiousness": 0.10},
        "N": {"Neuroticism": -0.14, "Extraversion": 0.27, "Openness": 0.64, "Agreeableness": -0.00, "Conscientiousness": -0.13},

        "T": {"Neuroticism": -0.13, "Extraversion": 0.00, "Openness": -0.17, "Agreeableness": -0.41, "Conscientiousness": 0.22},
        "F": {"Neuroticism": 0.12, "Extraversion": -0.00, "Openness": 0.13, "Agreeableness": 0.28, "Conscientiousness": -0.27},

        "J": {"Neuroticism": 0.07, "Extraversion": -0.13, "Openness": -0.25, "Agreeableness": 0.05, "Conscientiousness": 0.46},
        "P": {"Neuroticism": -0.07, "Extraversion": 0.16, "Openness": 0.26, "Agreeableness": -0.06, "Conscientiousness": -0.46},
    }

    # E-I
    e_score = sum(scores[trait] * weights["E"][trait] for trait in weights["E"])
    i_score = sum(scores[trait] * weights["I"][trait] for trait in weights["I"])
    mbti = "E" if e_score >= i_score else "I"

    # S-N
    s_score = sum(scores[trait] * weights["S"][trait] for trait in weights["S"])
    n_score = sum(scores[trait] * weights["N"][trait] for trait in weights["N"])
    mbti += "S" if s_score >= n_score else "N"

    # T-F
    t_score = sum(scores[trait] * weights["T"][trait] for trait in weights["T"])
    f_score = sum(scores[trait] * weights["F"][trait] for trait in weights["F"])
    mbti += "T" if t_score >= f_score else "F"

    # J-P
    j_score = sum(scores[trait] * weights["J"][trait] for trait in weights["J"])
    p_score = sum(scores[trait] * weights["P"][trait] for trait in weights["P"])
    mbti += "J" if j_score >= p_score else "P"

    return mbti


def ai_summary(final_scores):
    prompt = f"""Here are my Personality trait scores:
        Openness: {final_scores['Openness']}
        Conscientiousness: {final_scores['Conscientiousness']}
        Extraversion: {final_scores['Extraversion']}
        Agreeableness: {final_scores['Agreeableness']}
        Neuroticism: {final_scores['Neuroticism']}
        MBTI: {final_scores['mbti_type']}

     Based on my Big Five scores and MBTI type, please provide a personal analysis according to the following topics:

    - 🌟 Key Traits and Tendencies: Describe the main characteristics and natural tendencies reflected in my scores and MBTI type.
    - ⚠️ Areas for Awareness: Which traits might present challenges or situations where I might want to be more mindful?
    - 💬 Communication Style: How do I typically express myself and interact with others, considering my personality profile?
    - 📈 Personal Growth Suggestions: What are some practical ways I can deepen my self-awareness and develop skills or habits that align with my personality?
    - 💘 Romantic Compatibility: Based on my MBTI and Big Five scores, which personality types might complement mine in relationships, and why?
    - 🧑‍💼 Career Suitability: What kinds of careers or work environments tend to be a good match for my personality traits?
    - 🏛️ Mythological or Historical Analogy: Which famous figure, mythological character, or archetype shares similarities with my personality, and why?

    Please write the answers in a clear, respectful, and personalized manner.

    Note: Please interpret my Big Five scores according to the following five ranges to reflect how strongly each trait is expressed:
    Traits are scored between 1-5:
    
    - 5: Very High (traits strongly expressed)
    - 4: High (traits often expressed)
    - 3: Medium (traits moderately expressed)
    - 2: Low (traits less expressed)
    - 1: Very Low (traits minimally expressed)
    """


    return prompt

def query_huggingface_model(prompt: str):
    headers = {
        "Authorization": f"Bearer {HF}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1000,
            "temperature": 0.7,
            "top_p": 0.9,
            "return_full_text": False
        }
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL_ID}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        print("API Hatası:", response.status_code, response.text)
        return None