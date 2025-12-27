import database
import streamlit as st
import time

if 'attempt' not in st.session_state:
    st.session_state.attempt = 1

with st.form("Receipts - Add Photo Receipt"):
    st.title("Add Receipt")
    photo = st.camera_input("Receipt Image")
    submit = st.form_submit_button("Submit")
    
    if "status" in st.session_state:
        st.error(st.session_state.status)

    if submit:
        if not photo:
            st.session_state.status = "Photo is required"
            st.rerun()

        st.session_state.attempt += 1

        if "status" in st.session_state:
            del st.session_state.status

        photo_data = photo.getvalue()

        conn = database.ReceiptsDatabase()
        conn.database_connect()

        conn.create_photo_receipt(photo_data)
        st.toast("Receipt added...")
        time.sleep(1)
        st.rerun()