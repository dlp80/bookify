import os
import re
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth


################################
def extract_song_info(): #should take input from claude

    import claude as cl
    json_string = cl.claude_prompt()


    # Parse the JSON string into a Python dictionary
    data = json.loads(json_string)

    # Extract song titles and artist names
    text = data["content"][0]["text"]
    lines = text.split("\n")
    song_info = [line.split(" by ") for line in lines if line.strip() != "" and " by " in line]

    
    song_titles = []
    artist_names = []
    for item in song_info[1:]:  # Skip the first item, which is not a song entry
        song_title = item[0].split('"')[1]  # Extract song title from the string
        artist_name = item[1]  # Extract artist name directly
        song_titles.append(song_title)
        artist_names.append(artist_name)
    
    return song_titles, artist_names

################################





    


'''
class SpotifyTrack():
    def __init__(self, uri, name, artist, album):
        self.uri = uri
        self.name = name
        self.artist = artist
        self.album = album

class SpotifyPlaylist():
    def __init__(self) -> None:      
        scope = 'playlist-modify-public playlist-modify-private user-library-read'
        
        self.bot =  claude()
        self.sp  = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIFY_CLIENT_ID'],
                                               client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'],
                                               scope=scope))

        self.playlist = None
        self.name = "making your playlist presents..."

        self.playlist_response = None
        self.last_response = None
'''