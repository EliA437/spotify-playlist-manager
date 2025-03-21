from io import BytesIO
import os
import requests
from dotenv import load_dotenv
from PIL import Image
import openai

load_dotenv()

openai.api_key = os.getenv('OPEN_AI_KEY')

# Read top artists
with open('User Data/TopArtists.txt') as file:
    top_artists_contents = file.read()

# Read top tracks
with open('User Data/TopTracks.txt') as file:
    top_tracks_contents = file.read()

def open_ai_api_req(promp):
        response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"{promp}"        # Input to ChatGpt
        }]
        )
        return response
# this method exists to avaoid previous issues with rules against creating images with certain words and promp limits
def create_image_prompt():
    image_creation_prompt = open_ai_api_req(f'make a description for an abstract art piece based off of the mood of the genres of these songs dont include anthing against the safety system{top_tracks_contents}')
    return image_creation_prompt['choices'][0]['message']['content']  # Extract actual text

# Create and save image
def create_image():

    ai_edited_prompt = create_image_prompt()
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
    image_name = "image_2.png"      # make this ai generated as well
    image_path = os.path.join(folder_name, image_name)

    # Open the image from the response and save it
    img = Image.open(BytesIO(response.content))
    img.save(image_path)

    print(f"Image saved to {image_path}")

create_image()


# Prompts
def ask_prompts():

    #print(top_artists_contents)

    prompt1 = f'{top_artists_contents} What time period did most of these artists become popular, who is the most popular artist, what places are most of these artists from, what genres do they primarily belong to, do these artists have any notable collaborations, how has their popularity evolved over time, what are some of their most popular songs, do they have any common influences or inspirations, and how do they engage with their fanbase?'

    num_artists_recomended = 100
    prompt2 = f'Can you recomend me {num_artists_recomended} more artists that I might like based on: {top_artists_contents}'

    prompt3 = f'Can you guess my gender, age, and what region im from based on my top artist{top_artists_contents}'

    # Call API based on prompts
    print('What your top artists say about you: \n\n')
    completion_0 = open_ai_api_req(prompt1)
    print(completion_0.choices[0].message.content + '\n')

    print('Giving recomendations... \n\n')
    completion_1 = open_ai_api_req(prompt2)
    print(completion_1.choices[0].message.content + '\n')

    print('Guessing age, gender, and region... \n\n')
    completion_2 = open_ai_api_req(prompt3)
    print(completion_2.choices[0].message.content + '\n')