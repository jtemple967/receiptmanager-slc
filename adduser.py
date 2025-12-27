import database
import streamlit as st
import time

if 'attempt' not in st.session_state:
    st.session_state.attempt = 1

with st.form("Add user"):
    st.title("Add User")
    user = st.text_input("User", key=f"user_{st.session_state.attempt}")
    password = st.text_input("Password", type='password', key=f"password_{st.session_state.attempt}")
    confirm_password = st.text_input("Confirm Password", type='password', key=f"confirm_password_{st.session_state.attempt}")    
    submit = st.form_submit_button("Submit")
    
    if "status" in st.session_state:
        st.error(st.session_state.status)

    if submit:
        if user == "" or password == "" or confirm_password == "":
            st.session_state.status = "User, password and confirm_password is required"
            st.rerun()

        conn = database.ReceiptsDatabase()
        conn.database_connect()

        # Check if user already exists
        users = conn.get_users(search_user=user)
        if users.shape[0] > 0:
            st.session_state.status = f"User {user} already exists"
            st.rerun()

        st.session_state.attempt += 1

        if "status" in st.session_state:
            del st.session_state.status

        conn.create_user(user, password)
        st.toast("User added...")
        time.sleep(1)
        st.rerun()