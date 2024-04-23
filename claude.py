import os
import asyncio
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()

client = Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=os.environ.get('ANTHROPIC_API_KEY'),
        )
    
genre = input("enter music genre: \n")
book = input("enter book title: \n")
author = input("enter author name: \n")

statement = f"genre: {genre} \nbook name: {book}\nauthor name: {author}"


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
                    "text": statement
                }
            ]
        }
    ]
)
print(message.content)
