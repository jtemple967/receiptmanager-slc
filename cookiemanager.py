import streamlit as st
from streamlit_cookies_controller import CookieController
from cryptography.fernet import Fernet
import time

class CookieManager():

    def __init__(self):
        
        self.FERNET = Fernet(st.secrets.fernet.fernet_key)
        self.controller = CookieController()

    def set(self, cookie_name, cookie_value):
        encrypted_value = self.FERNET.encrypt(cookie_value.encode()).decode()
        self.controller.set(name=cookie_name, value=encrypted_value)
        time.sleep(1)

    def get(self, cookie_name):
        value = None
        encrypted_value = self.controller.get(cookie_name)
        if encrypted_value:
            try:
                value = self.FERNET.decrypt(encrypted_value).decode()
            except Exception as e:
                self.remove(cookie_name)
        return value
    
    def remove(self, cookie_name):
        self.controller.remove(cookie_name)