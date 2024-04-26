import os
from flask import Flask, redirect, request, session, render_template
import requests
import urllib.parse
import jsonify
import json
import datetime
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler


#import claude as cl
import list as ls
from dotenv import load_dotenv
load_dotenv()



'''
# step 1, from ClaudeAI return the list of songs and artists
# step 2, with the output from Claude reformat the output to be a list of song / artist
# step 3, extract song titles and artist names
title, artist = ls.extract_song_info()
# intermediate - print the extracted lists
print(title)
print(artist)

'''
app = Flask(__name__)
app.secret_key = os.urandom(64)
#app.config['SECRET_KEY'] = os.urandom(64)
scope = 'user-read-private user-read-email playlist-modify-private playlist-modify-public'


 
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback' 
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

"""
cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)
"""

sp = Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                                   redirect_uri=REDIRECT_URI,
                                                   client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   show_dialog=True
                                                   ))


# where users to log into their spotify when first landing on our flask page
@app.route('/')
def index():
    return "welcome to bookify, a web app powered by spotify api <a href='/login'> login with spotify </a>"
    #return render_template('homepage.html')


@app.route('/login')
def login():
    scope = 'user-read-private user-read-email playlist-modify-private playlist-modify-public'

    params = {
         'client_id': CLIENT_ID,
         'response_type': 'code',
         'scope': scope,
         'redirect_uri': REDIRECT_URI,
         'show_dialog': True #change to false when done, set to true just for testing
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

#creating endpoint
@app.route('/callback')
def callback():
     if 'error' in request.args:
        return jsonify({"error": request.args['error']})
     
     if 'code' in request.args:
          request_body = {
               'code' : request.args['code'],
               'grant_type' : 'authorization_code',
               'redirect_uri' : REDIRECT_URI,
               'client_id' : CLIENT_ID,
               'client_secret' : CLIENT_SECRET
          }

          response = requests.post(TOKEN_URL, data=request_body)
          token_info = response.json()

          session['access_token'] = token_info['access_token']
          session['refresh_token'] = token_info['refresh_token']
          session['expires_at'] = datetime.datetime.now().timestamp() + token_info['expires_in']

          return redirect('/entry')
     
@app.route('/entry')
def entry_page():
    return render_template('homepage.html')

@app.route('/submit-book', methods=['POST'])
def submit_book():

    data = request.json
    # assigning user entries to session vars
    session['book_name'] = data.get('bookName')
    session['author_name'] = data.get('authorName')
    session['genre'] = data.get('genre')
    
    # test print, o/p looks like: Rock Babel R.F. Kuang
    #print(genre, book_name, author_name)
    #return # jsonify({'message': 'Book data received successfully'})

    return redirect('/playlists')

@app.route('/playlists')
def make_playlists():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token') #incoming endpoint
    

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    # 0 - setting up user id, empty uri list, init variables
    user_id = sp.current_user()["id"]
    spotify_song_uris = []
    genre = session.get('genre')
    book_name = session.get('book_name')
    author_name = session.get('author_name')
    
    # 1 - generating playlist from claude
    titles, artist = ls.extract_song_info(genre, book_name, author_name)
    # intermediate - print the extracted lists
    # print(title)
    # print(artist)

    # 2 - making claude output into a dict for search purposes
    song_artist_list = dict(zip(artist, titles))
    spotify_song_uris = []

    for song in titles:
        result = sp.search(q=f"track:{song}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            spotify_song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")
    
    playlist = sp.user_playlist_create(user=user_id, name=f"now reading playlist", public=False)
    sp.playlist_add_items(playlist_id=playlist["id"], items=spotify_song_uris)
    
    return redirect('/finished')
    #return spotify_song_uris, user_id
    # response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    # playlists = response.json()
    # return jsonify(playlists)

@app.route('/finished')
def exit_page():
    return render_template('fin.html')


@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.datetime.now().timestamp() > session['expires_at']:
        request_body = {
            'grant-type': 'refresh-token',
            'refresh-token': session['refresh_token'],
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=request_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/playlists')
    


# running the flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)














####################

"""
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
    
    # 1. claude output
    title, artist = ls.extract_song_info()
    # intermediate - print the extracted lists
    # print(title)
    # print(artist)
   
   
    # 2. making claude output into a dict for search purposes
    song_artist_list = dict(zip(artist, title))
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





    




################################################
if __name__ == '__main__':
    app.run(debug=True)

"""