import os
import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from analyze_data_wAI import open_ai_api_req
import re

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-modify-private, playlist-modify-public, user-top-read'

# Authenticate with Spotify
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_path=".spotifycache",
    show_dialog=True
)

sp = spotipy.Spotify(auth_manager=sp_oauth)



def create_playlist(init_prompt):

    converted_prompt = f"create a list of {init_prompt} with the format: ('Track Name', 'Artist') no numbers or anthing"

    user_id = sp.current_user()['id']

    # Create a new playlist
    playlist_data = {
        "name": "AI Generated Playlist",
        "description": "Generated using AI recommendations",
        "public": False
    }

    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    access_token = sp_oauth.get_access_token(as_dict=False)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=playlist_data)

    if response.status_code == 201:
        playlist = response.json()
        playlist_id = playlist['id']
        print(f"Playlist Created: {playlist['name']} ({playlist['external_urls']['spotify']})")
    else:
        print(f"Failed to create playlist: {response.status_code} - {response.text}")
        return

    # Function to get track URI
    def get_track_uri(track_name, artist_name=""):
        query = f"track:{track_name} artist:{artist_name}"
        result = sp.search(q=query, type="track", limit=1)

        if result['tracks']['items']:
            return result['tracks']['items'][0]['uri']
        return None

    # AI generates a list of songs
    def build_track_name_list():
        track_list = open_ai_api_req(converted_prompt)  # Simulating the OpenAI API response

        # Step 1: Use a regular expression to extract song and artist pairs
        pattern = r"\('([^']+)', '([^']+)'\)"
        matches = re.findall(pattern, track_list)

        # Step 2: Print the result to verify
        for song, artist in matches:
            print(f"Song: {song}, Artist: {artist}")

        return matches

    # Convert track names to URIs
    def build_track_uri_list():
        track_name_list = build_track_name_list()  # Get track name list

        songs = []
        artists = []

        # Separate the song and artist into different lists
        for song, artist in track_name_list:
            songs.append(song)
            artists.append(artist)

        track_uris = [get_track_uri(track, artist) for track, artist in track_name_list if get_track_uri(track, artist)]
        return track_uris

    # Add tracks to playlist
    def add_songs_to_playlist():
        track_uris = build_track_uri_list()
        if track_uris:
            sp.playlist_add_items(playlist_id, track_uris)
            print("Songs added to playlist!")
        else:
            print("No valid songs found.")

    add_songs_to_playlist()



