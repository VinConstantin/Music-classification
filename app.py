from flask import Flask, request
from flask import render_template
from pandas.io.json import json_normalize
from flask import jsonify
import pandas as pd
import numpy as np
import requests
import json

from sklearn.preprocessing import StandardScaler
import sklearn
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score


app = Flask(__name__)
header = list()
knnCustom = KNeighborsClassifier(n_neighbors=9)

@app.route('/')
@app.route('/index')
def index():
    return render_template('Home.html', title='À propos')


@app.route('/Music')
def Music():
    return render_template('index.html', title='Classification de musique')



@app.route('/Custom')
def custom():
    return render_template('default.html', title='Custom AI')


@app.route('/getGenre/<titre>')
def get_Music_Genre(titre):
    genre = MakePred(titre)
    return genre


@app.route('/constructModel', methods=["POST"])
def constructModel():
    data = request.get_json()
    array = json_normalize(data)
    header.extend(list(array))
    i = header.index("target")
    header.pop(i)
    print(header)
    trainModel(array)
    return jsonify(columns = header)

@app.route('/classifier', methods=["POST"])
def classifier():
    data = request.get_json()
    array = json_normalize(data)
    returnVal = MakePredCustom(array)
    return returnVal



def trainModel(all_df):

    X = all_df[header]
    y = all_df.target

    scaled_df = pd.DataFrame(X, columns=X.columns).fillna(0)

    X_train, X_test, y_train, y_test = train_test_split(scaled_df, y, test_size=0.2, random_state=3)

    k_best = find_best_k(X_train, y_train, X_test, y_test, min_k=1, max_k=25)
    knnCustom = KNeighborsClassifier(n_neighbors = k_best)

    knnCustom.fit(X_train, y_train)

    preds = knnCustom.predict(X_test)
    print_metrics(y_test, preds)
    
def MakePredCustom(data):
    print(header)
    X = data[header]

    #X = data[["Cost","Sold"]]
    y_predict = knnCustom.predict(X)

    result = y_predict[0]
    return result

# KNN ALGORITHM

# !/usr/bin/env python
# coding: utf-8

# In[259]:




# ###### Aller cherhcer une clé pour le API de spotify

# In[331]:




client_id = 'c7f5de676ada4290b185e65b841c903d'
client_secret = '1ed2aa769a5e46e2a5991eff761d68d0'

grant_type = 'client_credentials'

body_params = {'grant_type': grant_type}

url = 'https://accounts.spotify.com/api/token'

response = requests.post(url, data=body_params, auth=(client_id, client_secret))
response.text

# In[332]:


access_token = response.json()['access_token']
headers = {'Authorization': 'Bearer ' + access_token}

# ###### Aller cherche la liste de ids de la playlist Hip Hop
# 

# In[333]:


id = "37i9dQZF1DWT5MrZnPU1zD"

# In[334]:


r = requests.get("https://api.spotify.com/v1/playlists/{}/tracks".format(id), headers=headers)

# In[335]:


hip_hop_songs = r.json()

# In[336]:


hip_hop_ids = []
for song in hip_hop_songs['items']:
    hip_hop_ids.append(song['track']['id'])

# In[337]:


len(hip_hop_ids)

# ###### Aller cherche la liste de ids de la playlist Classic

# In[338]:


id = "37i9dQZF1DWWEJlAGA9gs0"
r = requests.get("https://api.spotify.com/v1/playlists/{}/tracks".format(id), headers=headers)
classical_songs = r.json()

# In[339]:


classical_ids = []
for song in classical_songs['items']:
    classical_ids.append(song['track']['id'])

# In[340]:


len(classical_ids)

# ###### Aller cherche la liste de ids de la playlist Techno

# In[361]:


id = "3dD968kYUZpgY38zSOiKgM"
r = requests.get("https://api.spotify.com/v1/playlists/{}/tracks".format(id), headers=headers)
techno_songs = r.json()

# In[362]:


techno_ids = []
for song in techno_songs['items']:
    techno_ids.append(song['track']['id'])

# In[363]:


len(techno_ids)

# ###### Aller cherche la liste de ids de la playlist Jazz

# In[344]:


id = "37i9dQZF1DX0SM0LYsmbMT"
r = requests.get("https://api.spotify.com/v1/playlists/{}/tracks".format(id), headers=headers)
jazz_songs = r.json()

# In[345]:


jazz_ids = []
for song in jazz_songs['items']:
    jazz_ids.append(song['track']['id'])

# In[346]:


len(jazz_ids)

# ###### Aller cherche la liste de ids de la playlist Country

# In[347]:


id = "4SssSas9VvpPXlMCWXnu91"
r = requests.get("https://api.spotify.com/v1/playlists/{}/tracks".format(id), headers=headers)
country_songs = r.json()

# In[348]:


country_ids = []
for song in country_songs['items']:
    country_ids.append(song['track']['id'])

# In[349]:


len(country_ids)

# ##### Aller chercher les caractéristiques de chacune des chansons de la playlist Hip Hop

# In[350]:


hip_hop_ids_test = ",".join(hip_hop_ids)

# In[351]:


r = requests.get(f"https://api.spotify.com/v1/audio-features/?ids={hip_hop_ids_test}", headers=headers)

# In[352]:


hip_hop_features = r.json()

# In[353]:


df_hip_hop = pd.DataFrame(hip_hop_features['audio_features'])

# In[354]:


df_hip_hop['target'] = "Hip-Hop"

# ##### Aller chercher les caractéristiques de chacune des chansons de la playlist Classique

# In[355]:


classical_ids = ",".join(classical_ids)

# In[356]:


r = requests.get(f"https://api.spotify.com/v1/audio-features/?ids={classical_ids}", headers=headers)
classical_features = r.json()

# In[357]:


df_classical = pd.DataFrame(classical_features['audio_features'])

# In[358]:


df_classical['target'] = "Classical"

# ##### Aller chercher les caractéristiques de chacune des chansons de la playlist Techno

# In[368]:


techno_ids = ",".join(techno_ids)

# In[369]:


r = requests.get(f"https://api.spotify.com/v1/audio-features/?ids={techno_ids}", headers=headers)
techno_features = r.json()

# In[ ]:


df_techno = pd.DataFrame(techno_features['audio_features'])

# In[370]:


df_techno['target'] = 'Techno'

# ##### Aller chercher les caractéristiques de chacune des chansons de la playlist Jazz

# In[371]:


jazz_ids_test = ",".join(jazz_ids)

# In[372]:


r = requests.get(f"https://api.spotify.com/v1/audio-features/?ids={jazz_ids_test}", headers=headers)

# In[373]:


jazz_features = r.json()

# In[374]:


df_jazz = pd.DataFrame(jazz_features['audio_features'])

# In[375]:


df_jazz['target'] = "Jazz"

# ##### Aller chercher les caractéristiques de chacune des chansons de la playlist Country

# In[376]:


country_ids_test = ",".join(country_ids)

# In[377]:


r = requests.get(f"https://api.spotify.com/v1/audio-features/?ids={country_ids_test}", headers=headers)

# In[378]:


country_features = r.json()

# In[379]:


df_country = pd.DataFrame(country_features['audio_features'])

# In[380]:


df_country['target'] = "Country"

# <h1>Mettre toutes les listes ensemble </h1>

# In[381]:


all_df = pd.concat([df_hip_hop, df_classical, df_techno, df_jazz, df_country])

# In[382]:


all_df.head()

# ##### Selectionner les caractéristiques voulu pour l'algorithme
# 

# In[383]:


X = all_df[['acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'speechiness',
            'tempo', 'time_signature', 'valence']]

# In[384]:


y = all_df.target

# ###### Scaling Features

# In[386]:



scaler = StandardScaler()
scaled_data = scaler.fit_transform(X)

scaled_df = pd.DataFrame(X, columns=X.columns)
scaled_df.head()

# In[387]:



X_train, X_test, y_train, y_test = train_test_split(scaled_df, y, test_size=0.2, random_state=3)

# In[388]:



from sklearn.preprocessing import StandardScaler
import sklearn
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score

# ##### Essayer plusieurs valeurs de k pour trouver le plus optimal

# In[389]:




def find_best_k(X_train, y_train, X_test, y_test, min_k=1, max_k=25):
    best_k = 0
    best_score = 0.0
    for k in range(min_k, max_k + 1, 2):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        preds = knn.predict(X_test)
        f1 = f1_score(y_test, preds, average='micro')
        if f1 > best_score:
            best_k = k
            best_score = f1

    print("Meilleur valeur de k: {}".format(best_k))
    print("F1-Score: {}".format(best_score))
    return best_k


# In[390]:


best_k = find_best_k(X_train, y_train, X_test, y_test, min_k=1, max_k=25)

# ##### Une valeur de k = 1 a été sélectionné pour le plus optimal

# In[391]:


knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)
preds = knn.predict(X_test)

# In[392]:


from sklearn.metrics import classification_report


# ##### Score de classification

# In[393]:


def print_metrics(labels, preds):
    print("Precision Score: {}".format(precision_score(labels, preds, average='micro')))
    print("Recall Score: {}".format(recall_score(labels, preds, average='micro')))
    print("Accuracy Score: {}".format(accuracy_score(labels, preds)))
    print("F1 Score: {}".format(f1_score(labels, preds, average='micro')))


print_metrics(y_test, preds)


def MakePred(titre):
    url = "https://api.spotify.com/v1/search?q={}&type=track".format(titre)
    r = requests.get(url, headers=headers)
    reponse = r.json()
    id = reponse['tracks']['items'][0]['id']

    url = "https://api.spotify.com/v1/audio-features/{}".format(id)
    r = requests.get(url, headers=headers)
    reponse = r.json()

    y_predict = knn.predict([[reponse['acousticness'], reponse['danceability'], reponse['energy'],
                              reponse['instrumentalness'], reponse['key'], reponse['liveness'],
                              reponse['loudness'], reponse['speechiness'], reponse['tempo'],
                              reponse['time_signature'], reponse['valence']]])

    genre = y_predict[0]
    return genre
