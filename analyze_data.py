import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv('OPEN_AI_KEY')

# Read top artists
with open('User Data/TopArtists.txt') as file:
    top_artists_contents = file.read()
#print(top_artists_contents)

prompt1 = f'What does this say about me if these are my top artists: {top_artists_contents}'                     

num_artists_recomended = 100
prompt2 = f'Can you recomend me {num_artists_recomended} more artists that I might like based on: {top_artists_contents}'

prompt3 = f'Can you guess my gender, age, and what region im from based on my top artist{top_artists_contents}'

def open_ai_api_req(promp):
    response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": f"{promp}"        # Input to ChatGpt
    }]
    )
    return response

print('What your top artists say about you: \n\n')
completion_0 = open_ai_api_req(prompt1)
print(completion_0.choices[0].message.content + '\n')

print('Giving recomendations... \n\n')
completion_1 = open_ai_api_req(prompt2)
print(completion_1.choices[0].message.content + '\n')

print('Guessing age, gender, and region... \n\n')
completion_2 = open_ai_api_req(prompt3)
print(completion_2.choices[0].message.content + '\n')