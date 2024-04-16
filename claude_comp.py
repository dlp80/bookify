import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import anthropic

client = anthropic.Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key="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",
        )

def claude_comp():
    
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="generate a playlist of [genre, user input] songs inspired by [book name, user input] written by [author name, user input]. use songs found on spotify and list in the form of song title, artist name",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "genre: kpop\nbook name: nona the ninth\nauthor name: tamsyn muir"
                    }
                ]
            }
        ]
    )
    print(message.content)
