import matplotlib.pyplot as plt

song_names = []
popularity_scores = []

# Read TopTracks.txt
with open('User Data/TopTracks.txt', 'r') as file:
    for line in file:
        parts = line.split(': ', 1)

        if len(parts) == 2:
            rest_of_line = parts[1].strip() # The part after the :

            song_parts = rest_of_line.split(' - Popularity: ')
            if len(song_parts) == 2:
                song_name = song_parts[0].strip()
                popularity_score = int(song_parts[1].strip())

                # Append song name and score to lists
                song_names.append(song_name)
                popularity_scores.append(popularity_score)


# Create the bar graph
plt.figure(figsize=(10, 6))  # Adjust the size of the graph
plt.bar(song_names, popularity_scores)

# Customize the graph
plt.title('Songs Popularity Score')  # Title of the graph
plt.xlabel('Songs')                 # Label for the x-axis
plt.ylabel('Popularity Score')      # Label for the y-axis

plt.xticks(rotation=90)


plt.tight_layout()  # Makes sure everything fits within the figure

# Optionally save the graph as an image
plt.savefig('Visualized Data/song_popularity_graph.png')
