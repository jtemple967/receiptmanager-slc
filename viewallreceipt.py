import database
import streamlit as st

conn = database.ReceiptsDatabase()
conn.database_connect()

if "status" in st.session_state:
    del st.session_state.status

receipts = conn.get_receipts(all_receipts=True)

st.title("View All Receipts")
st.dataframe(receipts,
            hide_index=True,
            column_config={
                "id": None,
                "payee" : "Payee",
                "amount" : st.column_config.NumberColumn("Amount", format="$ %.2f"),
                "receipt_date" : st.column_config.DateColumn("Date"),
                "category" : "Category",
                "image_id": st.column_config.LinkColumn(label="Receipt Image", display_text="Image"),
                "recorded" : st.column_config.CheckboxColumn("Recorded"),
                "created_date" : st.column_config.DatetimeColumn("Created Date"),
                "created_by" : "Created By",
                "modified_date" : st.column_config.DatetimeColumn("Modified Date"),
                "modified_by" : "Modified By"

            }
            )