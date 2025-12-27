import database
import streamlit as st

conn = database.ReceiptsDatabase()
conn.database_connect()

if "status" in st.session_state:
    del st.session_state.status

receipts = conn.get_receipts()

with st.form("View Receipts"):
    st.title("View Receipts")
    receipt_data = st.data_editor(receipts,
                hide_index=True,
                column_config={
                    "id": None,
                    "selected" : st.column_config.CheckboxColumn("Select"),
                    "payee" : "Payee",
                    "amount" : st.column_config.NumberColumn("Amount", format="$ %.2f"),
                    "receipt_date" : st.column_config.DateColumn("Date"),
                    "category" : "Category",
                    "image_id": st.column_config.LinkColumn(label="Receipt Image", display_text="Image"),
                    "recorded" : st.column_config.CheckboxColumn("Recorded"),
                    "created_date" : st.column_config.DatetimeColumn("Created Date"),
                    "created_by" : "Created By"
                },
                disabled={"id","receipt_date","payee","amount","recorded","category","image","created_date","created_by"}
                )
    mark_record = st.form_submit_button("Mark Selected as Recorded")

    if mark_record:
        for index, row in receipt_data.iterrows():
            if row['selected']:
                conn.mark_receipt_as_recorded(row['id'])
    
        st.rerun()