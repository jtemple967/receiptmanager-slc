import database
import streamlit as st
import time

with st.form("Receipts - Cleanup"):
    st.title("Clean Up Recorded Receipts")
    number_days = st.number_input(label="Number days back to purge", min_value=30)
    submit = st.form_submit_button("Submit")
    
    if submit:
        conn = database.ReceiptsDatabase()
        conn.database_connect()

        number_rows = conn.purge_recorded_transactions(number_days=number_days)
        st.toast(f"Removed {number_rows} receipts")
        time.sleep(1)
        st.rerun()