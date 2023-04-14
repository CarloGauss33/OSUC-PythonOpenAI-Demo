import os
import dotenv
dotenv.load_dotenv()

class ConfigTokens:
    def __init__(self) -> None:
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

settings = ConfigTokens()