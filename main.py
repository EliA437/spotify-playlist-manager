from fetch_data import get_playlist_info, get_users_top_artists, get_users_top_tracks, save_playlist_names_to_txt
from visualize_data import create_top_tracks_bargraph, read_top_tracks
from analyze_data_wAI import ask_prompts, create_image
from playlist_generator import create_playlist
# eventually add main terminal logic here for interacting with the program

if __name__ == "__main__":

# UNUSED METHODS  
        
    #save_playlist_lengths_to_txt(playlists_info)
    #create_image()

# Terminal
    print("\n")
    print("Welcome to the spotify playlist manager\n")
    print("**************************************")
    print("1: Create a playlist")
    print("2: Get a list of your top 50 songs")
    print("3: Get a list of your top 50 artists")
    print("4: Get a list of your playlists")
    print("**************************************\n")
    print("(press q at anytime to quit)")

    choice = ''

    while True:
        choice = input("Enter a number 1 - 4 based on what you would like to do (or 'q' to quit): \n")

        if choice not in ('1', '2', '3', '4', 'q'):
            print("Please input a valid number.")
            continue  

        if choice == "q":
            print("Goodbye!")
            break  
        
        # "1: Create a playlist"
        if choice == "1":

            playlist_info = input(
                'What type of playlist would you like to create? \n'
            )
              
            while True:
              
                num_songs =  input('How many songs do you want on it? (Must be <= 50)\n')
                int_num_songs = int(num_songs)
                if int_num_songs > 50 or int_num_songs <= 0:
                    print('Please enter a valid number.')
                    continue  
                else:
                    prompt = f'create a playlist that is {playlist_info} with no more and no less than {num_songs} songs on it'
                    create_playlist(prompt)

                break  

        # "2: Get a list of your top 50 songs"
        elif choice == "2":
            print('Getting your top 50 songs...\n')
            get_users_top_tracks()

            while True:
                to_be_analyzed = input(
                    'Would you like to create a graph to analyze your top songs in relation to their popularity? Type (y/n): \n'
                )

                if to_be_analyzed not in ('y', 'n'):
                    print('Please enter a valid choice.')
                    continue  

                if to_be_analyzed == 'y':
                    print("Creating top tracks bar graph...")
                    create_top_tracks_bargraph()

                break  
        # "3: Get a list of your top 50 artists"
        elif choice == "3":
            print('Getting your top 50 artists...\n')
            get_users_top_artists()

            while True:
                to_be_analyzed = input(
                    'Would you like more recomendations based on your top artists (y/n): \n'
                )

                if to_be_analyzed not in ('y', 'n'):
                    print('Please enter a valid choice.')
                    continue  

                if to_be_analyzed == 'y':
                    print("Creating AI analysis...")
                    ask_prompts()

                break  
        # "4: Get a list of your playlists"
        elif choice == "4":
            print("Fetching your playlists...")
            playlist_info = get_playlist_info()
            save_playlist_names_to_txt(playlist_info)

