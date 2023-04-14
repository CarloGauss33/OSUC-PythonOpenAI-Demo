import os
import openai
from config import settings
import json

openai.api_key = settings.OPENAI_API_KEY
system_prompt = {
    "role": "system",
    "content": 'Analyze any text and return the emotion of the text. in a JSON RFC 8259 format. ' \
                'response_text should be in the user language. ' \
                'Example 1: {"emotion": "happy", "score": "0.9", "response_text": "Sample response text"}. ' \
                'Example 2: {"emotion": "sad", "score": "0.1", "response_text": "Sample response text"}. ' \
                'Example 3: {"emotion": "angry", "score": "0.5", "response_text": "Sample response text"}. ' \
                'Example 4: {"emotion": "neutral", "score": "0.5", "response_text": "Sample response text"}. ' \
}


messageHistory = [system_prompt]

while True:
    try:
        user_message = input("User: ")
        messageHistory.append({'role': 'user', 'content': user_message})

        raw_response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages= messageHistory
                    )

        response = raw_response.choices[0].message.content

        parsed_response = json.loads(response)
        emotion = parsed_response['emotion']
        score = parsed_response['score']
        response_text = parsed_response['response_text']
        messageHistory.append({'role': 'assistant', 'content': response })

        print(f"Bot: Emocion detectada: {emotion}, Score: {score}, Texto: {response_text}")
    except Exception as e:
        print(e)
        print("Algo ocurrió mal, intenta de nuevo")