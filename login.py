import database
import streamlit as st
from streamlit_cookies_controller import CookieController
import time
from cookiemanager import CookieManager

with st.form("Login"):
    user = st.text_input("User")
    password = st.text_input("Password", type='password')
    submit_login = st.form_submit_button("Login")

    if submit_login:
        cookie_manager = CookieManager()
        conn = database.ReceiptsDatabase()
        conn.database_connect()

        time.sleep(1)

        uid = conn.verify_password(user, password)
        if uid:
            cookie_manager.set("ReceiptsUserId",user)
            st.session_state['user'] = user
            st.rerun()
        else:
            st.error("Invalid user or password")  