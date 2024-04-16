import os
from flask import Flask, redirect, request, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import claude_comp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

#we want to put these in a secure env variables 
client_id = 'b3ffacb3f32c4524b45258fd2557483a'
client_secret = '5ccdf155fca14eb0b1cdfd8e3c01b69a'
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

class SpotifyTrack():
    def __init__(self, uri, name, artist, album):
        self.uri = uri
        self.name = name
        self.artist = artist
        self.album = album

class SpotifyPlaylist():
    def __init__(self) -> None:      
        scope = 'playlist-modify-public playlist-modify-private user-library-read'
        
        self.bot =  claude_comp()
        self.sp  = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIFY_CLIENT_ID'],
                                               client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
                                               redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'],
                                               scope=scope))

        self.playlist = None
        self.name = "making your playlist presents..."

        self.playlist_response = None
        self.last_response = None
    








################################################
if __name__ == '__main__':
    app.run(debug=True)
