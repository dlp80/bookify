import os
from flask import Flask, redirect, request, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler


#import claude as cl
import list as ls
from dotenv import load_dotenv
load_dotenv()




# step 1, from ClaudeAI return the list of songs and artists
# step 2, with the output from Claude reformat the output to be a list of song / artist
# Extract song titles and artist names
title, artist = ls.extract_song_info()
# Print the extracted lists
print(title)
print(artist)

'''
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

 
client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'http://localhost:5000/callback' 
scope = 'playlist-modify-public, user-top-read, user-library-modify, user-library-read'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)

sp = Spotify(auth_manager=sp_oauth)

#adding login with spotify
@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('user-top-read'))

#creating endpoint
@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('user-top-read'))

#creating the bulk of the web app - in the example this is used to "get playlists"

@app.route('/create_playlists')

def create_playlists():
    #re check token validity
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
            auth_url = sp_oauth.get_authorize_url()
            return redirect(auth_url)
    
    
    #call claude here to get song list
    statement = claude.in_info()
    text_block = claude.claude(statement)
    ##bot functionality?##
    song_list, artist_list = spclass.SpotifyPlaylist.extract_song_info(text_block)
   
   
    #parsing CLAUDE ouptut and using spotify api
    song_artist_list = dict(zip(artist_list, song_list))
    spotify_song_uris = []

    ##TAKEN OUT OF BELOW FOR LOOP ['artists'][0] -> remember to add back in
    for key, value in song_artist_list.items():
        spotify_result = sp_oauth.search(q=f"artist:{key} track:{value}", type="track")
        try:
            song_uri = spotify_result['tracks']['items'][0]['uri']
            spotify_song_uris.append(song_uri)
        except IndexError:
            print(f"{value} doesn't exist in Spotify. Skipped.")

    #print(len(spotify_song_uris))

    my_playlist = sp_oauth.user_playlist_create(user=f"{user_id}", name=f"My Bookify Playlist", public=False,
                                        description="A new soundtrack for my currently reading. Powered by Bookify")


'''


    




################################################
#if __name__ == '__main__':
    #app.run(debug=True)
