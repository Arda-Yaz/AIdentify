import uuid
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager


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
    st.write("Cookie id:" , user_id)
else:
    st.write("Saved id:", user_id)


