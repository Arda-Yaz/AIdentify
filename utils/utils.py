import uuid
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager



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
