import database
import streamlit as st
from io import BytesIO
from PIL import Image

conn = database.ReceiptsDatabase()
conn.database_connect()

# Get the image id
image_id = st.query_params.get("image_id", None)
# Get the image passed, if any
image_blob = conn.get_receipt_image(image_id)

# Convert to an image?
image = None
if image_blob:
    # Wrap the blob in BytesIO and open with PIL
    img = Image.open(BytesIO(image_blob))

with st.form("View image"):
    st.title("View image")
    if img:
        st.image(img)
    submit = st.form_submit_button("Go back", on_click=st.query_params.clear)    