import streamlit as st
import pandas as pd
import numpy as np
import json
import io
import plotly.express as px
import plotly.graph_objects as go
from streamlit import session_state
# from utils import *
import pickle

import firebase_admin
from firebase_admin import db,  credentials

# firebase_admin.delete_app(firebase_admin.get_app())
key_dict = json.loads(st.secrets['textkey'])
creds = credentials.Certificate(key_dict)
url = 'https://cityhub-dev-default-rtdb.europe-west1.firebasedatabase.app/'
# if "db" not in session_state: 
if not firebase_admin._apps:
    db = firebase_admin.initialize_app(creds,    {'databaseURL' : url} ) 
print(firebase_admin.get_app())
print(' ')
# session_state['db']
# else : db = session_state['db']
# ref = db.reference('items2')
# data = db.reference().get()
# ref = db.reference('items2')
# L  = ref.order_by_child('Keywords').equal_to("Loisirs").get()

ListItems = db.reference('items').get()
ListItems[2].keys()
st.dataframe(pd.DataFrame.from_dict(ListItems))