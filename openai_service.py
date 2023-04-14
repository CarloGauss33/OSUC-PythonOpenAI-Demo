import openai
import json
import os
from config import settings

openai.api_key = settings.OPENAI_API_KEY

class ChatManager:
    def __init__(self, history_file_path="history.json"):
        self.history_file_path = history_file_path
        self.history = []
        self.find_or_create_history()
        self.load_history()

    def find_or_create_history(self):
        if not os.path.exists(self.history_file_path):
            with open(self.history_file_path, "w") as f:
                json.dump([], f)

    def load_history(self):
        with open(self.history_file_path, "r") as f:
            self.history = json.load(f)

    def save_history(self):
        with open(self.history_file_path, "w") as f:
            json.dump(self.history, f)

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        self.save_history()

    def get_messages(self, system_message=""):
        return [{ "role": "system", "content": system_message }] + self.history

class CompletionsBot:
    def __init__(self):
        self.engine = "gpt-4"

    def get_chat_completion(self, messages, temperature=0.1, max_tokens=500):
        response = openai.ChatCompletion.create(
            model=self.engine,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        if response.choices:
            return response.choices[0].message.content
        return 'No se pudo generar una respuesta'


completions_bot = CompletionsBot()
chat_manager = ChatManager()