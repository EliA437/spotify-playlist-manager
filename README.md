# Spotify Playlist Manager

## Setup Instructions

### 1) Clone the Repository
```sh
git clone <repository-url>
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