from openai_service import completions_bot, chat_manager
import engines.budaApi as budaApi
import engines.musicPlayer as music_player
import json

budaApi = budaApi.BudaAPI()
music_player = music_player.MusicPlayer()

def get_bitcoin_price(args=None):
    return budaApi.get_bitcoin_price()

def turns_lights_on(args=None):
    print("Encendiendo luces")

def turns_lights_off(args=None):
    print("Apagando luces")

def play_song(song_name):
    music_player.play_song(song_name)
    return

def get_songs(args=None):
    return ", ".join(music_player.available_songs)

mapping = {
    'LIGHTS_ON': turns_lights_on,
    'LIGHTS_OFF': turns_lights_off,
    'PLAY_SONG': play_song,
    'GET_BITCOIN_PRICE': get_bitcoin_price,
    'GET_AVAILABLE_SONGS': get_songs,
    'DO_NOTHING': lambda args=None: None
}

def build_system_message():
    message = "You are an assistant bot for the user that can call certain actions. "
    message += "You can call the following actions: "
    message += "DO_NOTHING - does nothing, "
    message += "LIGHTS_ON - turns lights on, "
    message += "LIGHTS_OFF - turns lights off, "
    message += "GET_BITCOIN_PRICE - gets the bitcoin price, "
    message += "PLAY_SONG - plays a song, "
    message += "GET_AVAILABLE_SONGS - gets the available songs. "
    message += " Do not include any explanations, only provide a  RFC8259 compliant JSON response  following this format without deviation."
    message += "{ ACTION_NAME: action_name, ARGS: args, MESSAGE: message }"
    message += "message should be in the language of the user."
    message += "The JSON response: "
    return message

system_message = build_system_message()

while True:
    prompt = input("Ingresa tu mensaje: ")
    chat_manager.add_message("user", prompt + '. JSON Response: ')
    messages = chat_manager.get_messages(system_message)

    raw_response = completions_bot.get_chat_completion(messages)

    try:
        response = json.loads(raw_response)
        action = response.get("ACTION_NAME")
        args = response.get("ARGS")
        message = response.get("MESSAGE")
        action_response = mapping[action](args)

        print(message)
        if action_response:
            print(f"{action}: {action_response}")

        chat_manager.add_message("assistant", raw_response)
    except Exception as e:
        print("No se pudo procesar la respuesta")
        print(e)