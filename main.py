from fetch_data import get_playlist_info, get_users_top_artists, get_users_top_tracks, save_playlist_names_to_txt


if __name__ == "__main__":
    
    playlists_info = get_playlist_info()
    
    if playlists_info:
        # Save playlist names and URLs
        save_playlist_names_to_txt(playlists_info)
        
        # Save playlist lengths
        #save_playlist_lengths_to_txt(playlists_info)

    else:
        print("No playlists found. Make sure your account has playlists and try again.")

    # Save users top artists
    get_users_top_artists()

    # Save users top tracks
    get_users_top_tracks()