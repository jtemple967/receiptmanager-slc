import streamlit as st
from sqlalchemy import text
import os
import hashlib
import datetime
from io import BytesIO

class ReceiptsDatabase:

    def __init__(self):

        if not os.path.exists(st.secrets['databaase']['db_name']):

            conn = self.database_connect()
            st.session_state.database_init = True

            with conn.session as s:
                sql_string = """create table if not exists 
                        receipts 
                        (id integer primary key autoincrement,
                        payee TEXT, 
                        amount FLOAT, 
                        receipt_date DATE, 
                        category TEXT, 
                        recorded BOOLEAN,
                        created_by TEXT,
                        created_date DATETIME,
                        modified_by TEXT,
                        modified_date DATETIME,
                        receipt_image BLOB)"""
                
                s.execute(text(sql_string))

                sql_string = """create table if not exists 
                        users
                        (id integer primary key autoincrement,
                        user TEXT, 
                        password TEXT, 
                        created_by TEXT,
                        created_date DATETIME,
                        modified_by TEXT,
                        modified_date DATETIME)"""
                
                s.execute(text(sql_string))

                sql_string = """insert into users
                            (user, password, created_date, created_by)
                            values (:user, :password, :created_date, :created_by)
                            """          
                
                s.execute(text(sql_string),
                        params={"user":"admin", 
                                "password":self.hash_password("admin"), 
                                "created_date":datetime.datetime.now(),
                                "created_by":"admin", 
                                }
                        )
                s.commit()

    def hash_password(self, password):
        hashed_password = hashlib.sha256((password+st.secrets.security.salt).encode('utf-8')).hexdigest()
        return hashed_password

    def verify_password(self, user, password):

        conn = self.database_connect()

        hashed_password = self.hash_password(password)

        sql_string = """select id from users where user = :user and password = :password"""
        
        results = conn.query(sql_string,
                            params={
                                "user":user,
                                "password":hashed_password
                                })

        if results.shape[0] > 0:
            return results.loc[0]['id']
        else:
            return False
    
    def database_connect(self):
        return st.connection('receipt_db', type='sql')


    def create_receipt(self, payee_var, amount_var, receipt_date_var, category_var, image_var):
        conn = self.database_connect()

        sql_string = """insert into receipts
                                  (payee, amount, receipt_date, category, recorded, created_date, created_by)
                                  values (:payee, :amount, :receipt_date, :category, False, :created_date, :created_by)
                                  """
        with conn.session as s:
            s.execute(text(sql_string),
                                    params={"payee":payee_var, 
                                            "amount":amount_var, 
                                            "receipt_date":receipt_date_var, 
                                            "category":category_var,
                                            "created_date":datetime.datetime.now(),
                                            "created_by":st.session_state.user
                                    }
                                    )
            s.commit()

    def create_photo_receipt(self, image_var):
        conn = self.database_connect()

        sql_string = """insert into receipts (receipt_image, recorded, created_date, created_by)
                                  values (:receipt_image, False, :created_date, :created_by)
                                  """
        with conn.session as s:
            s.execute(text(sql_string),
                                    params={"receipt_image":image_var, 
                                            "created_date":datetime.datetime.now(),
                                            "created_by":st.session_state.user
                                    }
                                    )
            s.commit()

    def get_receipts(self, all_receipts=False):
        conn = self.database_connect()
        if all_receipts:
            sql_string = """select id, payee, amount, receipt_date, category,
                            case when receipt_image is not null then '/?image_id=' || id else null end as image_id,
                            recorded, created_date, created_by, modified_date, modified_by from receipts
                            order by receipt_date, payee, amount"""
        else:
            sql_string = """select id, False as selected, payee, amount, receipt_date, category, 
                            case when receipt_image is not null then '/?image_id=' || id else null end as image_id,
                            recorded, created_date, created_by from receipts
                            where recorded = False order by receipt_date, payee, amount"""            
        receipts = conn.query(sql_string,
                                ttl=0)
        return receipts
    
    def get_receipt_image(self, record_id):
        image_stream = None
        conn = self.database_connect()
        sql_string = """select receipt_image from receipts
                        where id = :id"""
        results = conn.query(sql_string,
                                params={
                                    "id":record_id
                                },
                                ttl=0)
        
        if results.shape[0] > 0:
            image_stream = results.loc[0]['receipt_image']
        return image_stream
    
    def mark_receipt_as_recorded(self, id):
        conn = self.database_connect()

        with conn.session as s:

            sql_string = """update receipts set recorded = True, modified_date = :modified_date, modified_by = :modified_by where id = :id"""          
            
            s.execute(text(sql_string),
                    params={"id":id, 
                            "modified_date":datetime.datetime.now(),
                            "modified_by":st.session_state.user
                            }
                    )
            s.commit()

    def create_user(self, user, password):

        conn = self.database_connect()

        with conn.session as s:

            sql_string = """insert into users
                        (user, password, created_date, created_by)
                        values (:user, :password, :created_date, :created_by)
                        """          
            
            s.execute(text(sql_string),
                    params={"user":user, 
                            "password":self.hash_password(password), 
                            "created_date":datetime.datetime.now(),
                            "created_by":st.session_state.user, 
                            }
                    )
            s.commit()

    def change_user_password(self, user, password):
        conn = self.database_connect()

        with conn.session as s:

            sql_string = """update users set password = :password, modified_date = :modified_date, modified_by = :modified_by where user = :user
                        """          
            
            s.execute(text(sql_string),
                    params={
                            "password":self.hash_password(password), 
                            "modified_date":datetime.datetime.now(),
                            "modified_by":st.session_state.user, 
                            "user":user,                             
                            }
                    )
            s.commit()

    def get_users(self, search_user=None):
        conn = self.database_connect()
        if search_user:
            sql_string = """select id, user, created_date, created_by from users where user = :user"""
            params = {"user":search_user}
        else:
            sql_string = """select id, user, created_date, created_by, modified_date, modified_by from users"""
            params=None
        users = conn.query(sql_string, params=params, ttl=0)
        return users
    
    def purge_recorded_transactions(self, number_days=90):
        conn = self.database_connect()

        with conn.session as s:

            sql_string = "delete from receipts where recorded = True and current_timestamp - created_date >= :number_days"
            results = s.execute(text(sql_string),
                      params={"number_days":number_days}
            )
            s.commit()
            
            return results.rowcount