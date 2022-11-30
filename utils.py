import pandas as pd
import numpy as np
import io
import json
import requests
import pickle
import collections
import streamlit as st


def scrap():
    DictResult = {}
    datasets = {'architecture-contemporaine-remarquable-en-ile-de-france-biens-labellises-et-prot': {},
    'chateaux-remarquables-dile-de-france-et-leur-parc0': {},
    'femmes-illustres-a-paris-portraits': {},
    'liste-des-jardins-remarquables': {},
    'liste_des_musees_franciliens': {},
    'principaux-sites-touristiques-en-ile-de-france0': {},
    'que-faire-a-paris-': {}}

    d = {}
    for dataset in datasets.keys():
        source = 'data.iledefrance'
        source = 'opendata.paris.fr'
    #     URL = "https://data.iledefrance.fr/api/records/1.0/search/?dataset="
        URL = "https://opendata.paris.fr/api/records/1.0/search/?dataset="
        URL = URL + dataset +'&rows=-1'
        r = requests.get(URL)
        st.write(r, dataset)
        print(r, dataset)
        data = r.json()
        if 'records' in  data.keys(): 
            dfv = pd.DataFrame(data['records']).fields.apply(pd.Series)
            dfv['source'] = source
            d[dataset] = dfv
            datasets[dataset]['source'] = source
    dd2 = d.copy()        
    L = []
    for k,dfv in dd2.items():
        dfv['File'] = k
        L.append(dfv)
    df = pd.concat(L).reset_index(drop = True)
    
    dfsize = df.groupby(df.File).size()
    
    d2 = {}
    for col in df.columns:
        d2[col] = df.loc[df[col].notnull(),col].iloc[0]
    ex = pd.Series(d2)
    
    d_transfert = {
        'File'       : ['File'],
        'source'     : ['source'],
        'Title'      : ['name', 'title'],
        'Summary'    : ['lead_text'],
        'Description': ['desc1', 'desc2', 'desc3', 'desc4', 'desc5', 'lead_text', 'description', 'title_event'],
        'Theme'      : [],
        'Category'   : [],
        'Keywords'   : ['tags'],
        'City'       : ['address_city'],
        'Department' : [],
        'Region'     : [],
        'Postal-Code': ['address_zipcode'],
        'Phone'      : ['contact_phone'],
        'Url'        : ['url'],
        'Email'      : ['contact_mail'],
        'Address'    : ['address_city','address_name' ,'address_street'],
        'Location'   : ['geo_point_2d','lat','long'],
        'Images'     : ['thumb_url','cover_url'],
    'Price-Details' : ['price_detail'],
        'Start-at'   : ['date_start'],
        'End-at'     : ['date_end'],
        'Transport'  : ['transport'],
    }
    dftransfert = pd.Series(d_transfert)
    
    L = []
    Stat = []
    for idx, row in df.fillna(0).iterrows():
        dx = {}
        s = {}
        for k, v in d_transfert.items():
            l = [row[c] for c in v if row[c] != 0]  
            s[k] = len(l)        
            if len(l)>0 :
                if len(l) == 1 : l = l[0]
                dx[k] = l
        s['File'] = row.File
        L.append(dx)
        Stat.append(s)
    dfr = pd.DataFrame(L) 
    
    dfstat = pd.DataFrame(Stat)
    dfstat.groupby('File')[dfstat.columns].mean().round(2)
    
    b = ((100*dfr.notnull().sum()/dfr.shape[0]).round(1).astype(str) + '%').rename('Ratio')
    a = dfr.notnull().sum().astype(int).rename('Hit')
    dfNull = pd.concat([a , b], axis = 1)
    
    k = 'tags'
    dfk  = df[df[k].notnull()][k].str.replace(';','|').str.get_dummies().sum().rename('Objects').to_frame()
    dfk['source'] = source
    
    d =  [df, dfr,dfNull,dfstat,ex, dftransfert, dfk]
    
    return d        
        




