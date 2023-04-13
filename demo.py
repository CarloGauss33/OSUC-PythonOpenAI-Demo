import os
import openai
from config import settings

openai.api_key = settings.OPENAI_API_KEY

user_message = input("User: ")

response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages= [
                    {'role': 'user', 'content': user_message},
                ]
            )

print(f"Bot: {response.choices[0].message.content}")