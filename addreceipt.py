import database
import streamlit as st
import time

if 'attempt' not in st.session_state:
    st.session_state.attempt = 1

with st.form("Receipts - Add Receipt"):
    st.title("Add Receipt")
    payee = st.text_input("Payee", key=f"payee_{st.session_state.attempt}")
    amount = st.number_input("Amount", key=f"amount_{st.session_state.attempt}")
    receipt_date = st.date_input("Date")
    category = st.text_input("Category", key=f"category_{st.session_state.attempt}")
    submit = st.form_submit_button("Submit")
    
    if "status" in st.session_state:
        st.error(st.session_state.status)

    if submit:
        if payee == "" or amount == 0 or category == "":
            st.session_state.status = "Payee, amount and category is required"
            st.rerun()

        st.session_state.attempt += 1

        if "status" in st.session_state:
            del st.session_state.status

        conn = database.ReceiptsDatabase()
        conn.database_connect()

        conn.create_receipt(payee, amount, receipt_date, category, None)
        st.toast("Receipt added...")
        time.sleep(1)
        st.rerun()