import os
import sys
from pygame import mixer

class MusicPlayer:
    def __init__(self, music_folder="songs") -> None:
        self.music_folder = music_folder
        self.available_songs = []
        self.load_available_songs()

    def load_available_songs(self):
        for song in os.listdir(self.music_folder):
            if song.endswith(".mp3"):
                self.available_songs.append(song)

    def get_songs(self):
        return '\n- '.join(self.available_songs)

    def play_song(self, song_name):
        if song_name in self.available_songs:
            print(f"Playing {song_name}")
            mixer.init()
            mixer.music.load(os.path.join(self.music_folder, song_name))
            mixer.music.play()
        return

    def stop_song(self, args=None):
        mixer.music.stop()
        return