from io import BytesIO
import os
import requests
from dotenv import load_dotenv
from PIL import Image
import openai

load_dotenv()

openai.api_key = os.getenv('OPEN_AI_KEY')

# Read top artists
with open('User Data/TopArtists.txt', encoding="utf-8", errors="replace") as file:
    top_artists_contents = file.read()

# Read top tracks
with open('User Data/TopTracks.txt', encoding="utf-8", errors="replace") as file:
    top_tracks_contents = file.read()

def open_ai_api_req(prompt):
    # Make the API request to OpenAI's ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"{prompt}"  # Input to ChatGPT
        }]
    )
    
    # Extract the actual text from the API response
    text_content = response['choices'][0]['message']['content']
    return text_content

# this method exists to avaoid previous issues with rules against creating images with certain words and promp limits
def create_image_prompt(songs_list):    # 3 Songs list is edited with this method to create an image prompt
    image_creation_prompt = open_ai_api_req(f'make an abstract painting based on {songs_list} ignore any stuff here that might go against the image creation policy of openai') 
    return image_creation_prompt#['choices'][0]['message']['content']  # Extract actual text

# Create and save image
def create_image(songs_list): # 1 Pass in songs list to create image
    print('Creating playlist image...')
    ai_edited_prompt = create_image_prompt(songs_list)  # 2 Send it to create edited prompt to change it
    if len(ai_edited_prompt) >= 1000:
        ai_edited_prompt = ai_edited_prompt[:1000]

    response = openai.Image.create(
        prompt=ai_edited_prompt,
        n=1,  # number of images to generate
        size="1024x1024"  # image size 
    )

    # Get the image URL
    image_url = response['data'][0]['url']
    #print(image_url)

    # Download the image using requests
    response = requests.get(image_url)

    folder_name = 'Playlist Images'
    image_name = "image_2.jpeg"      
    image_path = os.path.join(folder_name, image_name)

    # Open the image from the response and save it
    img = Image.open(BytesIO(response.content))
    img.save(image_path)

    print(f"Image saved to {image_path}")

# Prompts
def ask_prompts():

    #print(top_artists_contents)

    # Analize users top artists
    def prompt_1():
        prompt1 = f'{top_artists_contents} What time period did most of these artists become popular, who is the most popular artist, what places are most of these artists from, what genres do they primarily belong to, do these artists have any notable collaborations, how has their popularity evolved over time, what are some of their most popular songs, do they have any common influences or inspirations, and how do they engage with their fanbase?'

        print('What your top artists say about you: \n\n')
        completion_0 = open_ai_api_req(prompt1)
        print(completion_0)

    # Recommend artists
    def prompt_2():
        num_artists_recomended = 100
        prompt2 = f'Can you recomend me {num_artists_recomended} more artists that I might like based on: {top_artists_contents} DO NOT INCLUDE DUPLICATE ARTISTS TO THE LIST'
        print('Giving recomendations... \n\n')
        completion_1 = open_ai_api_req(prompt2)
        print(completion_1)

    # Guess user info based on top artists
    def prompt_3():
        prompt3 = f'Can you guess my gender, age, and what region im from based on my top artist{top_artists_contents}'
        print('Guessing age, gender, and region... \n\n')
        completion_2 = open_ai_api_req(prompt3)
        print(completion_2)

    prompt_2() # Only call prompt 2 for now
   



    