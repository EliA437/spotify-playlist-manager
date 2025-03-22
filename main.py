from fetch_data import get_playlist_info, get_users_top_artists, get_users_top_tracks, save_playlist_names_to_txt
from visualize_data import create_top_tracks_bargraph, read_top_tracks
from analyze_data_wAI import ask_prompts, create_image
# eventually add main terminal logic here for interacting with the program

if __name__ == "__main__":

# FETCH DATA FILE  
    playlists_info = get_playlist_info()
    
    
    # Save playlist names and URLs
    save_playlist_names_to_txt(playlists_info)
        
    # Save playlist lengths
    #save_playlist_lengths_to_txt(playlists_info)

    # Save users top artists
    get_users_top_artists()

    # Save users top tracks
    get_users_top_tracks()

# VISUALIZE DATA FILE

    # Read top tracks data and save to lists
    read_top_tracks()

    # Create bar graph from top tracks info
    create_top_tracks_bargraph()

# ANALIZE DATA FILE

    #ask_prompts()
    create_image()