import os
import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from analyze_data_wAI import open_ai_api_req

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private, playlist-modify-public, playlist-modify-private, user-top-read' # Change this to grant access to do different things

# Authenticate with Spotify (this will open a browser for login)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_path=".spotifycache",  # Store the token in a local file
    show_dialog=True
)

# Get an authenticated Spotify client
sp = spotipy.Spotify(auth_manager=sp_oauth)

# Get playlist info
def get_playlist_info():

    print("Fetching your Spotify playlist data...\n")

    playlists = sp.current_user_playlists()
    playlists_info = []
    
    for pl in playlists.get('items', []):  # Iterate through all playlists
        name = pl.get('name', 'Unknown Playlist')  # Playlist name
        url = pl.get('external_urls', {}).get('spotify', 'No URL')  # Playlist URL
        
        # Fetch the tracks of the playlist (this will give you the track count)
        playlist_tracks = sp.playlist_tracks(pl['id'])
        track_count = len(playlist_tracks['items'])  # Get the number of tracks
        
        playlists_info.append((name, url, track_count))
    
    return playlists_info

# Write playlist names and url to text file
def save_playlist_names_to_txt(playlists_info, folder="Playlist Data", filename="PlaylistNames.txt"):

    print(f"Writing playlist names...")

    file_path = os.path.join(folder, filename)
    with open(file_path, "w", encoding="utf-8") as file:  # open in write mode
        for name, url, _ in playlists_info:  # Unpack name, url, and ignore the length
            file.write(f"{name}: {url}\n\n")
            
    print(f"Playlist names and urls have been saved to {filename}")

# Write playlist name and length to text file
def save_playlist_lengths_to_txt(playlists_info, folder="Playlist Data", filename="PlaylistLengths.txt"):

    print(f"Writing playlist lengths...")

    file_path = os.path.join(folder, filename)
    with open(file_path, "w") as file:  # open in write mode
        for name, _, playlist_length in playlists_info:  # Unpack name, ignore url, and get length
            length = ""
            if playlist_length >= 100:
                length = "Equal to or greater than 100 tracks"
            else:
                length = playlist_length
            file.write(f"{name}: {length} tracks\n\n")
            
    print(f"Playlist lengths have been saved to {filename}")

# Get the users top artists
def get_users_top_artists(folder='User Data', filename='TopArtists.txt'):

    print(f"Fetching your top artists...")

    top_artists_data = sp.current_user_top_artists(limit=50)     # Fetch top artists. Change limit to fetch more. Maximum is 50
    top_artists = [artist['name'] for artist in top_artists_data.get('items', [])]      # Extract artist names

    # Write to file
    file_path = os.path.join(folder, filename)
    with open(file_path, "w") as file:  # open in write mode
        for artist_name in top_artists:  # Unpack name, url, and ignore the length
            file.write(f"{artist_name}\n")
            
    print(f"Top artists have been saved to {filename}")

# Get the users top tracks
def get_users_top_tracks(folder='User Data', filename='TopTracks.txt'):

    print(f"Fetching your top tracks...")

    top_tracks_data = sp.current_user_top_tracks(limit=30)     # Fetch top tracks. Change limit to fetch more. Maximum is 50

    # Extract track names and popularity scores
    top_tracks = [(track['name'], track['popularity']) for track in top_tracks_data.get('items', [])]

    file_path = os.path.join(folder, filename)

    with open(file_path, "w") as file:  
        i = 1
        for track_name , track_popularity in top_tracks:  
            file.write(f"{i}: {track_name} - Popularity: {track_popularity}\n")
            i += 1
     

    print(f"Top tracks have been saved to {filename}")



