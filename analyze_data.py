import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv('OPEN_AI_KEY')

# Read top artists
with open('User Data/TopArtists.txt') as file:
    top_artists_contents = file.read()
#print(top_artists_contents)

prompt = 'What does this say about me if these are my top artists'

completion = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": f"{prompt}: {top_artists_contents}"        # Input to ChatGpt
    }]
)

print(completion.choices[0].message.content + '\n')
