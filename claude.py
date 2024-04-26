import os
import re
import asyncio
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()


def claude_prompt(genre, book, author):

    #basic input from when testing claude functionality
    #genre = input("enter music genre: \n")
    #book = input("enter book title: \n")
    #author = input("enter author name: \n")

    statement = f"genre: {genre} \nbook name: {book}\nauthor name: {author}"

    client = Anthropic(
                # defaults to os.environ.get("ANTHROPIC_API_KEY")
                api_key=os.environ.get('ANTHROPIC_API_KEY'),
            )
        

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="Create a playlist of songs inspired by a user input book. Use songs found on spotify and list in the form of a subscriptable list with the song title, artist name. Only return the list in the response.",
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

    
    #print(message.to_json())
    #return message.content
    return message.to_json()
