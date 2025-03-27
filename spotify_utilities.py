from analyze_data_wAI import open_ai_api_req
from PIL import Image
import base64

def create_name(converted_prompt):
    max_words = 2
    print("Creating playlist name...\n")
    
    # Create playlist name with chat gpt
    name_prompt = f'{converted_prompt} playlist name must just be in the format: Playlist Name. Nothing else around it. No characters just the playlist name. No longer than 30 characters or 3 words'
    playlist_name = open_ai_api_req(name_prompt) 

    # // filters to make sure playlist name is correct //
    
    # Ensure max 2 word length
    words = playlist_name.split()  # Split into words
    playlist_name = ' '.join(words[:max_words])  # Keep only the first 3 words while adding a space in between

    # Remove anything that's not an alphabetical character except spaces
    playlist_name = ''.join(c for c in playlist_name if c.isalpha() or c.isspace() or c.isalnum())
    
    print(f"Playlist name: {playlist_name}\n")
    return playlist_name

def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())  # Convert image to base64
            return encoded_string.decode('utf-8')  # Return base64 string
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