import os
import dotenv

class ConfigTokens:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.TELGRAM_BOT_TOKEN = os.getenv("TELGRAM_BOT_TOKEN")

settings = ConfigTokens()