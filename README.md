# Spotify Playlist Manager

## Description

This project allows you to create personalized playlists based on a promp. Some of its features include:

- **Playlist Creation**: Based on a promp it can create you a playlist automatically and upload it to your Spotify account.
- **Top 50 Songs**: Retrieve a list of the top 50 songs based on various criteria, such as user preferences or trending data.
- **Top 50 Artists**: Access a list of the top 50 artists, showcasing the most popular musicians across genres.
- **Spotify Popularity Comparison**: A graph is generated to compare the popularity of the top 50 songs using Spotify's popularity scores. This helps you visually understand how popular the songs are on the platform.

The project uses **Matplotlib**, a scientific library, to create the graphs that display the comparisons between songs and their popularity scores.

Overall, this project makes it easier to create playlists, discover new artists and tracks, and gain insights into the popularity of songs on Spotify.


## Setup Instructions

### 1) Clone the Repository
```sh
git clone https://github.com/EliA437/spotify-playlist-manager
cd spotify-playlist-manager
```

### 2) Create a `.env` File
Inside the project folder, create a `.env` file and add the following variables with your API keys:
```sh
# Spotify API
CLIENT_ID = ''
CLIENT_SECRET = ''

# OpenAI API
OPEN_AI_KEY = ''
```

### 3) Install Virtual Environment (if necessary)
- On **Linux/macOS**:
  ```sh
  sudo apt install python3.12-venv  # Not required on Windows
  ```

### 4) Set Up Virtual Environment
```sh
python3 -m venv venv
```
- **Activate it:**
  - On **Linux/macOS**:
    ```sh
    source venv/bin/activate
    ```
  - On **Windows**:
    ```sh
    venv\Scripts\activate
    ```

### 5) Install Dependencies
```sh
pip install -r requirements.txt
```

### 6) Run the Program
```sh
python main.py
```
