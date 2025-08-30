# media_generators/audio_narrator.py

from gtts import gTTS
import os
import pygame

class NoirNarrator:
    """Generate and play narration using Google TTS."""
    def __init__(self):
        print("🎙️ Initializing Google TTS narrator...")
        os.makedirs("assets/audio_narration", exist_ok=True)
        try:
            pygame.mixer.init()
            print("✅ Audio mixer initialized")
        except Exception as e:
            print(f"⚠️ Pygame mixer init failed: {e}")

    def narrate_chapter(self, text, chapter_number=1):
        """Generate natural narration for a chapter and save to MP3."""
        filename = f"chapter_{chapter_number}.mp3"
        filepath = os.path.join("assets/audio_narration", filename)
        
        if not os.path.exists(filepath):
            try:
                print(f"🎙️ Generating narration for Chapter {chapter_number}...")
                tts = gTTS(text=text, lang='en', slow=True)
                tts.save(filepath)
                print(f"✅ Audio saved: {filepath}")
            except Exception as e:
                print(f"⚠️ TTS failed: {e}")
                return None
        
        return filepath

    def play_audio(self, filepath):
        """Play an MP3 file via pygame."""
        try:
            if filepath and os.path.exists(filepath):
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.play()
                print(f"🎵 Playing audio: {filepath}")
            else:
                print(f"⚠️ Audio file not found: {filepath}")
        except Exception as e:
            print(f"⚠️ Audio playback failed: {e}")
