import os

from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

#we want to put these in a secure env variables 
client_id = 'b3ffacb3f32c4524b45258fd2557483a'
client_secret = '5ccdf155fca14eb0b1cdfd8e3c01b69a'
redirect_uri = 'http://localhost:5000/callback' 
scope = 'playlist-modify-public, user-top-read, user-library-modify, user-library-read'

if __name__ == '__main__':
    app.run(debug=True)
