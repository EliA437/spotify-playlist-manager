import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private'  # Access private playlists

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
    file_path = os.path.join(folder, filename)
    with open(file_path, "w") as file:  # open in write mode
        for name, url, _ in playlists_info:  # Unpack name, url, and ignore the length
            file.write(f"{name}: {url}\n\n")
            
    print(f"Playlist names and urls have been saved to {filename}")

# Write playlist name and length to text file
def save_playlist_lengths_to_txt(playlists_info, folder="Playlist Data", filename="PlaylistLengths.txt"):
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
    
if __name__ == "__main__":
    print("Fetching your Spotify playlists...\n")
    
    playlists_info = get_playlist_info()
    
    if playlists_info:
        # Save playlist names and URLs
        save_playlist_names_to_txt(playlists_info)
        
        # Save playlist lengths
        save_playlist_lengths_to_txt(playlists_info)
    else:
        print("No playlists found. Make sure your account has playlists and try again.")
