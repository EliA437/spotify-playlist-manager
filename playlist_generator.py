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

def start_playlist_generator(init_prompt):

    converted_prompt = f"create a list of {init_prompt} with the format: ('Track Name', 'Artist') no numbers"

    # // HELPER METHODS //
    def create_name():
        max_length = 30

        print("Creating playlist name...\n")
        
        # Create playlist name with chat gpt
        name_prompt = f'{converted_prompt} playlist name must just be in the format: Playlist Name. Nothing else around it. No characters just the playlist name. No longer than 30 characters or 3 words'
        playlist_name = open_ai_api_req(name_prompt) 

        # // filters to make sure playlist name is correct //

        # Ensure max 3 word length
        words = playlist_name.split()  # Split into words
        playlist_name = ' '.join(words[:3])  # Keep only the first 3 words while adding a space inbetween

        # Remove anything thas not an alphabetical character except the spaces
        playlist_name = ''.join(c for c in playlist_name if c.isalpha() or c.isspace() or c.isalnum) 

        print(f" playlist_name: {playlist_name}\n")

        return playlist_name
    
    # Function to get track URI
    def get_track_uri(track_name, artist_name=""):
        query = f"track:{track_name} artist:{artist_name}"
        result = sp.search(q=query, type="track", limit=1)

        if result['tracks']['items']:
            return result['tracks']['items'][0]['uri']
        return None

    # // Main Methods //

    def create_playlist():
        playlist_name = create_name() # Use the create playlist name heleper method to create a new name for the playlist
        user_id = sp.current_user()['id']

        # Create a new playlist
        playlist_data = {
            "name": playlist_name,
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

        
        if response.status_code == 201: # playlist create successful
            playlist = response.json()
            playlist_id = playlist['id']
            print(f"Playlist Created: {playlist['name']} ")
            add_songs_to_playlist(playlist_id) # if the playlist is successfully created we can now add songs and pass through playlist id
        else:                                                                               # playlist creation not successful
            print(f"Failed to create playlist: {response.status_code} - {response.text}")
            return

    
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
    def add_songs_to_playlist(playlist_id):
        track_uris = build_track_uri_list()
        if track_uris:
            print('Adding songs now...')
            sp.playlist_add_items(playlist_id, track_uris)
            print("Songs added to playlist!")
        else:
            print("No valid songs found. - this error occurs when their is an issue with the AI, just try running it a few more times and it will probalbly work")

    
    create_playlist()




