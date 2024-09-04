from bs4 import BeautifulSoup
import requests as req
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
sp= spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        show_dialog=True,
        cache_path="token.txt"
       # username= USERNAME

    ))
date = input("Which year do you want to travel in time?\n Type the date in format YYYY-MM-DD:")
#
response = req.get("https://www.billboard.com/charts/hot-100/" + date)
soup=BeautifulSoup(response.text, 'html.parser')
song_names_spans=soup.select("li ul li h3")
song_names= [song.getText().strip() for song in song_names_spans]
#print(song_names)
song_uris=[]
year=date.split("-")[0]
for song in song_names:
    try:
        print(f"Searching for : {song}")
        result = sp.search(q=f"track:{song}",type="track")
        if not result['tracks']['items']:
            print(f"Initial search for {song} returned no results. Trying with year filter.")
            result=sp.search(q=f"track:{song} year:{year}",type="track")
        if result['tracks']['items']:
            uri=result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
            print(f"Found {song}: {uri}")
        else:
            print(f"{song} doesn't exist on Spotify, Skipped!")

    except Exception as e:
        print(f"An error occured: {e}")
print("List of song URIs:", song_uris)






if song_uris:
    playlist = sp.user_playlist_create(user=os.getenv("user_ID"), name=f"{date} Billboard 100", public=False)
    print(playlist)
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
    print(f"Added {len(song_uris)} songs to the playlist.")
else:
    print("No songs found to add to the playlist.")
# user_id = sp.current_user()["id"]
# print(f"Authenticated user ID: {user_id}")
#sp = spotipy.Spotify(auth="ACCESS_TOKEN")  # Use the access token from your JSON

# Retrieve user profile information
#user_info = sp.current_user()

# Get the user ID
#user_id = user_info['id']
#print(f"Authenticated user ID: {user_id}")