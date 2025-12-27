import database
import streamlit as st
import time

if 'attempt' not in st.session_state:
    st.session_state.attempt = 1

with st.form("Change password"):
    st.title("Change Password")
    user = st.text(st.session_state.user)
    old_password = st.text_input("Old Password", type='password', key=f"old_password_{st.session_state.attempt}")
    password = st.text_input("New Password", type='password', key=f"password_{st.session_state.attempt}")
    confirm_password = st.text_input("Confirm New Password", type='password', key=f"confirm_password_{st.session_state.attempt}")    
    submit = st.form_submit_button("Submit")
    
    if "status" in st.session_state:
        st.error(st.session_state.status)

    if submit:
        if user == "" or old_password == "" or password == "" or confirm_password == "":
            st.session_state.status = "User, old password, new password and confirmation password is required"
            st.rerun()

        conn = database.ReceiptsDatabase()
        conn.database_connect()

        uid = conn.verify_password(st.session_state.user, old_password)
        if not uid:
            st.session_state.status = "Old password not valid"
            st.rerun()

        if password != confirm_password:
            st.session_state.status = "New passwords don't match"
            st.rerun()

        st.session_state.attempt += 1

        if "status" in st.session_state:
            del st.session_state.status

        conn.change_user_password(st.session_state.user, password)
        st.toast("Password changed...")
        time.sleep(1)
        st.rerun()