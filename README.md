# Receipt Manager

A simple receipt tracker for personal finance

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Set your secrets file:

[connections.receipt_db]
url = "sqlite:///data/receiptmanager.db"

[database]
db_name = "data/receiptmanager.db"

[security]
salt = "6xZ"

[fernet]
fernet_key="xxxxx" (this is the only value you'll need to change. Refer to the cryptography documentation on how to generate this)

3. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
