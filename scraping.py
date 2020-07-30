import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import numpy as np
import pandas as pd
from csv import writer
from pandas import DataFrame

# spotify developer login credientials. Credentials are specific to each user and generally shouldn't be shared, but if you make
# your own credentials.json file w/your spotify client ID and secret ID the code will still work. 
# (Spotify Developer page -> My Dashboard -> Login -> Create an app and the info should be displayed on your app panel)
credentials = json.load(open('credentials.json'))
client_id = credentials['client_id']
client_secret = credentials['client_secret']

playlist_index = 0

# how many items to get from each playlist (by default this is the first 5 items)
number_items = 5

# load the json file that contains the info for all the playlists to pull songs from
playlists = json.load(open('playlists.json'))

while (playlist_index < len(playlists)):
    i = 0

    playlist_uri = playlists[playlist_index]['uri']
    playlist_title = playlists[playlist_index]['title']

    # gives access to spotify data
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    uri = playlist_uri
    playlist_id = uri.split(':')[2]

    # just get the items field from the playlist, only get the first number_items songs
    results = sp.playlist_tracks(playlist_id, 'items', number_items, 0) 

    # put info in a dataframe and convert it to a json file.
    # Note: this code creates a file local to my computer but should work if you change it to be local to your device
    results_df = pd.DataFrame(data=results)
    results_df.to_json (r'C:\Users\laurafang\Desktop\Nautilus\test1.json')

    with open (r'C:\Users\laurafang\Desktop\Nautilus\test1.json', 'r') as f:
        song = json.load(f)

    # get title, artist, and uri for each of the 5 songs from the playlist and add to csv file
    while (i < number_items):  
        song_title = song['items'][str(i)]['track']['name']
        song_artist = song['items'][str(i)]['track']['album']['artists'][0]['name']
        song_uri = song['items'][str(i)]['track']['uri']

        # open file in append mode
        with open('test1doc.csv', 'a+', newline='') as write_obj:
            # create a writer object from the csv module
            csv_writer = writer(write_obj)
            # add contents of list as last row in the csv file
            csv_writer.writerow([song_title, song_artist, song_uri])

        i = i + 1

    playlist_index = playlist_index + 1
