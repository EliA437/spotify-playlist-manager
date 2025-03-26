import base64
import os
import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from analyze_data_wAI import open_ai_api_req
import re
from requests.exceptions import SSLError
import time
from PIL import Image

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-modify-private, playlist-modify-public, user-top-read, ugc-image-upload'

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

def start_playlist_generator(init_prompt, num_songs):

    converted_prompt = f"create a list of {init_prompt} with the format: ('Track Name', 'Artist') no numbers that must be {num_songs} long"

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
    
    def get_valid_access_token():
        print('getting access token')
        token_info = sp_oauth.get_cached_token()
        if not token_info:
            print("Not authorized or token has expired.")
            return None
        return token_info['access_token']

    def image_to_base64(image_path):
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())  # This converts the image to base64
                return encoded_string.decode('utf-8')  # Return the base64 string
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def compress_image(image_path, output_path, max_width=1000, max_height=1000, quality=70):
        try:
            with Image.open(image_path) as img:
                # Resize the image if it exceeds the max dimensions
                img.thumbnail((max_width, max_height))

                # Save the image with reduced quality
                img.save(output_path, format='JPEG', quality=quality)  # JPEG is generally more compressed than PNG
                print(f"Image saved as {output_path} with reduced size.")
                return output_path  # Return the path to the compressed image

        except Exception as e:
            print(f"An error occurred: {e}")
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
        access_token = access_token = get_valid_access_token() 
        # Authorization check
        if not access_token:
            print("Not authorized. Please check your Spotify credentials.")
            return  # Exit the function if not authorized
        else:
            print("You are authorized.")

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, json=playlist_data)

        
        if response.status_code == 201: # playlist create successful
            playlist = response.json()
            playlist_id = playlist['id']
            print(f"Playlist Created: {playlist['name']} ")

            # // apon successfull playlist creation //
            add_songs_to_playlist(playlist_id) # if the playlist is successfully created we can now add songs and pass through playlist id
            print('Getting playlist image')

            # // ADD PLAYLIST IMAGE //
            folder_name = 'Playlist Images'
            image_name = "image_2.jpeg"      
            image_path = os.path.join(folder_name, image_name)
            compressed_image_path = "Playlist Images/compressed_img.jpeg"  # Path to save the compressed image


            # Refresh access token if it's expired
            access_token = access_token = get_valid_access_token() 
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'image/jpeg'
            }
            # Compress image
            compressed_image = compress_image(image_path, compressed_image_path, 300, 300, 70)
            # Convert image to base 64
            image_base64 = image_to_base64(compressed_image)

            url = f"https://api.spotify.com/v1/playlists/{playlist_id}/images"
            
            #image_base64 = '/9j/2wCEABoZGSccJz4lJT5CLy8vQkc9Ozs9R0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0cBHCcnMyYzPSYmPUc9Mj1HR0dEREdHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR//dAAQAAf/uAA5BZG9iZQBkwAAAAAH/wAARCAABAAEDACIAAREBAhEB/8QASwABAQAAAAAAAAAAAAAAAAAAAAYBAQAAAAAAAAAAAAAAAAAAAAAQAQAAAAAAAAAAAAAAAAAAAAARAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwAAARECEQA/AJgAH//Z'
            #print(f"image in base 64: {image_base64}")

            # Post a req to the API
            print('Adding playlist image')
            for attempt in range(3):  # Retry 3 times
                try:
                    response = requests.put(url, headers=headers, data=image_base64)
                    #print(image_base64)
                    if response.status_code == 202:
                        print("Playlist cover image updated successfully!")
                        return
                    else:
                        print(f"Error {response.status_code}: {response.text}")
                except requests.exceptions.RequestException as e:
                    print(f"Request failed with error: {e}")
                time.sleep(3)  # Wait for 3 seconds before retrying

            print("Failed to upload playlist image after 3 attempts")

        else:                                                                               # playlist creation not successful
            print(f"Failed to create playlist: {response.status_code} - {response.text}")
            return
        
            # Fetch image file -> decode it -> create post request to the API
    
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





