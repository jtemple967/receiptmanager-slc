import database
import streamlit as st

conn = database.ReceiptsDatabase()
conn.database_connect()

if "status" in st.session_state:
    del st.session_state.status

users = conn.get_users()

st.title("List Users")
st.dataframe(users,
            hide_index=True,
            column_config={
                "id": None,
                "user" : "Payee",
                "created_date" : st.column_config.DatetimeColumn("Created Date"),
                "created_by" : "Created By",
                "modified_date" : st.column_config.DatetimeColumn("Modified Date"),
                "modified_by" : "Modified By",
            }
)