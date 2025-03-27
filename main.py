from fetch_data import get_playlist_info, get_users_top_artists, get_users_top_tracks, save_playlist_names_to_txt
from visualize_data import create_top_tracks_bargraph, read_top_tracks
from analyze_data_wAI import ask_prompts, create_image
from playlist_generator import start_playlist_generator

# This script provides a terminal-based interface for managing Spotify playlists

    # UNUSED METHODS (kept for potential future use) 
    # save_playlist_lengths_to_txt(playlists_info)

def main():
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        LIGHTGREEN = '\033[38;5;10m'  # Bright green
        MEDIUMGREEN = '\033[38;5;34m'  # Medium green
        DARKGREEN = '\033[38;5;22m'  # Dark green
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    
    # create a playlist for coding
    # Display menu options to the user
    print("\n")
    print(bcolors.LIGHTGREEN + "Welcome to the Spotify Playlist Manager\n" + bcolors.ENDC)
    print(bcolors.LIGHTGREEN + "**************************************" + bcolors.ENDC)
    print(bcolors.DARKGREEN + "1: Create a playlist" + bcolors.ENDC)
    print(bcolors.DARKGREEN + "2: Get a list of your top 50 songs" + bcolors.ENDC)
    print(bcolors.DARKGREEN + "3: Get a list of your top 50 artists" + bcolors.ENDC)
    print(bcolors.DARKGREEN + "4: Get a list of your playlists" + bcolors.ENDC)
    print(bcolors.LIGHTGREEN + "**************************************" + bcolors.ENDC)

    choice = ''

    while True:
        # Get user input and ensure it is valid
        choice = input(bcolors.WARNING + "Enter a number 1 - 4 based on what you would like to do (or 'q' to quit): \n" + bcolors.ENDC)

        if choice not in ('1', '2', '3', '4', 'q'):
            print("Please input a valid number.")
            continue  

        if choice == "q":
            print("Goodbye!")
            break  
        
        # Option 1: Create a playlist
        if choice == "1":
            playlist_info = input('What type of playlist would you like to create? \n')
              
            while True:
                num_songs = input('What is the max amount of songs you want on it? (Must be <= 50)\n')
                int_num_songs = int(num_songs)
                
                if int_num_songs > 50 or int_num_songs <= 0:
                    print('Please enter a valid number.')
                    continue  
                else:
                    # Generate prompt for playlist creation
                    prompt = f'create a playlist that is {playlist_info} with no more and no less than {num_songs} songs on it MUST BE {num_songs} long'
                    create_image()
                    start_playlist_generator(prompt, num_songs)
                break  

        # Option 2: Get top 50 songs
        elif choice == "2":
            print('Getting your top 50 songs...\n')
            get_users_top_tracks()

            while True:
                # Ask the user if they want to visualize their top tracks
                to_be_analyzed = input('Would you like to create a graph to analyze your top songs in relation to their popularity? Type (y/n): \n')

                if to_be_analyzed not in ('y', 'n'):
                    print('Please enter a valid choice.')
                    continue  

                if to_be_analyzed == 'y':
                    print("Creating top tracks bar graph...")
                    create_top_tracks_bargraph()
                break  

        # Option 3: Get top 50 artists
        elif choice == "3":
            print('Getting your top 50 artists...\n')
            get_users_top_artists()

            while True:
                # Ask the user if they want AI-based recommendations
                to_be_analyzed = input('Would you like more recommendations based on your top artists (y/n): \n')

                if to_be_analyzed not in ('y', 'n'):
                    print('Please enter a valid choice.')
                    continue  

                if to_be_analyzed == 'y':
                    print("Creating AI analysis...")
                    ask_prompts()
                break  

        # Option 4: Get user's playlists
        elif choice == "4":
            print("Fetching your playlists...")
            playlist_info = get_playlist_info()
            save_playlist_names_to_txt(playlist_info)

if __name__ == "__main__":
    main()
