from gtts import gTTS
import os, pygame

# narration via gTTS
class Narrator:
    def __init__(self):
        print("Initializing Google TTS narrator...")
        os.makedirs("assets/audio_narration", exist_ok=True)
        try:
            pygame.mixer.init()
        except:
            pass

    # generate an mp3 matching the text
    def narrate_chapter(self, text, chapter_number):
        filename = f"chapter_{chapter_number}.mp3"
        path = os.path.join("assets/audio_narration", filename)
        # always regenerate to match updated text
        try:
            tts = gTTS(text=text, lang="en", slow=True)
            tts.save(path)
        except Exception as e:
            print(f"TTS error: {e}")
            return None
        return path

    # play the chapter audio
    def play_audio(self, path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except:
            pass