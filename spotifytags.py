import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import numpy as np
import pandas as pd
from csv import writer
from pandas import DataFrame

# Spotify developer login credentials. Credentials are specific to each user and generally shouldn't be shared,
# but if you make your own credentials.json file w/your spotify client ID and secret ID the code will still work.
# (Spotify Developer page -> My Dashboard -> Login -> Create an app and the info should be displayed on your app panel)
credentials = json.load(open('credentials.json'))
client_id = credentials['client_id']
client_secret = credentials['client_secret']

tracks_list = [] 
counter = 0 
i = 0

with open('test1doc.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
         uri = row[2].split(':')[2]
         tracks_list.append(uri)
         counter = counter + 1
    # print(tracks_list)

    # gives access to spotify data
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # get the audio features of each song in tracks_list
    results = sp.audio_features(tracks_list) 

    # put info in a data frame and convert it to a json file.
    # Note: this code creates a file local to my computer but should work if you change it to be local to your device
    results_df = pd.DataFrame(data=results)
    results_df.to_json(r'C:\Users\laurafang\Desktop\Nautilus\test2.json')

    with open(r'C:\Users\laurafang\Desktop\Nautilus\test2.json', 'r') as f:
        song = json.load(f)

    # get all cateogry values for each audio feature for each song
    while i < counter:
        danceability = song['danceability'][str(i)]
        energy = song['energy'][str(i)]
        key = song['key'][str(i)]
        mode = song['mode'][str(i)]
        acousticness = song['acousticness'][str(i)]
        instrumentalness = song['instrumentalness'][str(i)]
        liveness = song['liveness'][str(i)]
        valence = song['valence'][str(i)]
        tempo = song['tempo'][str(i)]

        # open file in append mode
        with open('spotifytags.csv', 'a+', newline='') as write_obj:
            # create a writer object from the csv module
            csv_writer = writer(write_obj)
            # add contents of list as last row in the csv file
            if i == 0:
                csv_writer.writerow(['danceability', 'energy', 'key', 'mode', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])
            else: 
                csv_writer.writerow([danceability, energy, key, mode, acousticness, instrumentalness, liveness, valence, tempo])

        i = i + 1
