from openai_service import completions_bot, chat_manager
import engines.budaApi as budaApi
import engines.musicPlayer as music_player
import engines.cameraManager as camera_manager
import json

class ChatbotManager:
    def __init__(self):
        self.budaApi = budaApi.BudaAPI()
        self.music_player = music_player.MusicPlayer()
        self.camera_manager = camera_manager.CameraManager()
        self.mappings = {}
        self.base_message = self.build_system_message()
        self.build_mappings()

    def turns_lights_on(self, args=None):
        print("Encendiendo luces")

    def turns_lights_off(self, args=None):
        print("Apagando luces")

    def take_video(self, args=None):
        self.camera_manager.take_video()

    def take_picture(self, args=None):
        self.camera_manager.take_picture()

    def play_song(self, song_name):
        print(f"Playing {song_name}")
        self.music_player.play_song(song_name)

    def stop_song(self):
        self.music_player.stop_song()

    def get_bitcoin_price(self, args=None):
        return self.budaApi.get_bitcoin_price()

    def get_songs(self, args=None):
        return self.music_player.get_songs()

    def available_songs(self, args=None):
        return self.music_player.get_songs()

    def build_mappings(self):
        self.mappings = {
            'LIGHTS_ON': self.turns_lights_on,
            'LIGHTS_OFF': self.turns_lights_off,
            'PLAY_SONG': self.play_song,
            'STOP_SONG': self.stop_song,
            'TAKE_PHOTO': self.take_picture,
            'TAKE_VIDEO': self.take_video,
            'AVAILABLE_SONGS': self.available_songs,
            'GET_BITCOIN_PRICE': self.get_bitcoin_price,
            'DO_NOTHING': lambda args=None: None,
            'ANSWER_QUESTION': lambda args=None: None,
        }

    def build_system_message(self):
        message = "You are an assistant bot for the user that can call certain actions. "
        message += "You can call the following actions: "
        message += "DO_NOTHING - does nothing, "
        message += "LIGHTS_ON - turns lights on, "
        message += "LIGHTS_OFF - turns lights off, "
        message += "TAKE_PHOTO - takes a photo, "
        message += "TAKE_VIDEO - takes a video, "
        message += "GET_BITCOIN_PRICE - gets the bitcoin price, bitcoin price will be sent in another message"
        message += "PLAY_SONG - plays a song "
        message += "AVAILABLE_SONGS - gets the available songs "
        message += "STOP_SONG - stops the song "
        message += "ANSWER_QUESTION - answers a question the response will be sent on MESSAGE field"
        message += " Do not include any explanations, only provide a  RFC8259 compliant JSON response  following this format without deviation."
        message += "{ ACTION_NAME: action_name, ARGS: args, MESSAGE: message }"
        message += "message should be in the language of the user."
        message += "The JSON response: "
        return message

    def ask(self, message):
        chat_manager.add_message("user", message)
        messages = chat_manager.get_messages(self.base_message)

        raw_response = completions_bot.get_chat_completion(messages)

        try:
            response = json.loads(raw_response)
            action = response.get("ACTION_NAME")
            args = response.get("ARGS")
            message = response.get("MESSAGE")
            print(action)
            action_response = self.mappings[action](args)

            if action_response:
                message += '\n' + action_response

            chat_manager.add_message("assistant", raw_response)

            return message

        except Exception as e:
            print(e)
            return 'No se pudo procesar la respuesta'


if __name__ == "__main__":
    chatbot_manager = ChatbotManager()

    print("Comenzando conversación")

    while True:
        message = input("User: ")
        response = chatbot_manager.ask(message)
        print("Assistant: ", response)