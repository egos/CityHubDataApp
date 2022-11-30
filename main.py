import streamlit as st
import pandas as pd
import numpy as np
import json
import io
import plotly.express as px
import plotly.graph_objects as go
from streamlit import session_state
from utils import *
import pickle

import firebase_admin
from firebase_admin import db,  credentials

# firebase_admin.delete_app(firebase_admin.get_app())

st.set_page_config(page_title = "VALEO_AG_IHM", layout="wide")
sections = ['Moteur Recherche', 'Data mining']
menu = st.sidebar.radio("MENU", sections, index  = 0)

if 'scrap' not in session_state: 
    session_state['scrap'] = []

key_dict = json.loads(st.secrets['textkey'])
cred = credentials.Certificate(key_dict)
url = 'https://cityhub-dev-default-rtdb.europe-west1.firebasedatabase.app/'
# if "db" not in session_state: 
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred,    {'databaseURL' : url} ) 
     
if menu == sections[0]: 
    print(firebase_admin.get_app())
    print(' ')
    ref = db.reference('test/agg')
    ListKey = ref.get(False,True).keys()
    st.write(str(ListKey))
    
    Key = st.text_input('Key')

    if Key : 
        Key = Key.split(' ')
        L0 = db.reference('test/agg/{}'.format(Key[0])).get()
        if len(Key)>1: 
            for k in Key[1:]: 
                print(k)
                L1 = db.reference('test/agg/{}'.format(k)).get()
                L0 = np.intersect1d(L0, L1)       
        ListIndex = list(L0) 
        print(ListIndex)
    if st.button("check"):
        if ListIndex: 
            st.write('{} resultats '.format(len(ListIndex)))
        
    if st.button("get data") :
        st.write('{} resultats '.format(len(ListIndex))) 
        L = []
        p = 0
        pmax = len(ListIndex)
        my_bar = st.progress(0)
        for index in ListIndex:
            p += 1
            progress = int(100*(p)/pmax)
            my_bar.progress(progress)
            print(index, end = ' ')
            ref = db.reference('test/items/{}'.format(index))
            res = ref.get()
            L.append(res)
        df = pd.DataFrame.from_dict(L)
        st.dataframe(df, use_container_width= True)      

    
if menu == sections[1]: 
    if st.button('donwload opendata.paris.fr'): 
        with st.spinner('Wait for it...'):
            session_state['scrap'] = scrap()
        st.success('Done!')
        
    VerifData = len(session_state['scrap']) > 0
    if  VerifData: 
        df, dfr,dfNull,dfstat,ex, dftransfert,dfk = session_state['scrap']
        st.dataframe(df , use_container_width= True)
        c1, c2 = st.columns(2)
        c1.table(dftransfert )
        c2.table(dfk )
        
    if st.button('export to firebase'):
        if VerifData:
            
            
            p = 0
            my_bar = st.progress(0)
            dfx = dfr.fillna('NAN')
            pmax = len(dfx)
            st.write('exporting {} items ... '.format(pmax))
            for idx, row in dfx.iterrows():
                p += 1
                progress = int(100*(p)/pmax)
                my_bar.progress(progress)
                ref = db.reference('test/items')
                ref.update({idx : row.to_dict()})
            st.success('Done!')
            st.write('exporting aggregation collection... ')
            with st.spinner('Wait for it...'):
                Keyword = dfr.Keywords.fillna('NAN').str.split(';')
                agg = collections.defaultdict(list)
                ref = db.reference('test/agg')
                for idx, row in Keyword.iteritems():
                    if row != ['NAN']: 
                        for r in row : 
                            agg[r].append(idx)                         
                ref = db.reference('test/agg')
                ref.set(agg)
            st.success('Done!')