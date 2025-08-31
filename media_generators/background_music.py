import pygame
import os

# play one of two fixed background music tracks
class MusicPlayer:
    def __init__(self):
        print("Initializing music player...")
        try:
            pygame.mixer.init()
            print("Audio mixer initialized")
        except Exception as e:
            print(f"Pygame mixer init failed: {e}")

        # hard-coded music file paths
        self.files = {
            "hidden_truth": "assets/background_music/hidden_truth.mp3",
            "mysterious_lights": "assets/background_music/mysterious_lights.mp3"
        }
        self.current = "hidden_truth"
        self.is_playing = False

    # select which track to play
    def change_theme(self, theme):
        if theme in self.files:
            self.current = theme
            print(f"Music theme set to: {theme}")
        else:
            print(f"Unknown music theme: {theme}")

    # start looping the selected track
    def play(self, volume=0.3):
        path = self.files.get(self.current)
        if path and os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
                self.is_playing = True
                print(f"Playing: {self.current}")
                return True
            except Exception as e:
                print(f"Music playback failed: {e}")
                return False
        else:
            print(f"Music file missing: {path}")
            return False

    # stop playback
    def stop(self):
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            print("Music stopped")
        except Exception as e:
            print(f"Stop music failed: {e}")
