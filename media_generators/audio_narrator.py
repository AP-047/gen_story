from gtts import gTTS
import os, pygame

class NoirNarrator:
    """Generate and play chapter-specific narration via gTTS."""
    def __init__(self):
        print("🎙️ Initializing Google TTS narrator...")
        os.makedirs("assets/audio_narration", exist_ok=True)
        try:
            pygame.mixer.init()
        except:
            pass

    def narrate_chapter(self, text, chapter_number):
        """Generate an MP3 matching exactly the text."""
        filename = f"chapter_{chapter_number}.mp3"
        path = os.path.join("assets/audio_narration", filename)
        # Always regenerate to match updated text
        try:
            tts = gTTS(text=text, lang="en", slow=True)
            tts.save(path)
        except Exception as e:
            print(f"TTS error: {e}")
            return None
        return path

    def play_audio(self, path):
        """Play the chapter audio."""
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except:
            pass

# Quick test
if __name__ == "__main__":
    nr = NoirNarrator()
    sample = "Detective Morgan steps into the rain and examines the crime scene."
    audio = nr.narrate_chapter(sample, 1)
    print("Generated:", audio)
