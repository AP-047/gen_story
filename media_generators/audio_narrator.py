import pyttsx3
import os
from pathlib import Path

class NoirNarrator:
    def __init__(self):
        print("🎙️ Initializing audio narrator...")
        
        # Voice configurations - easily changeable
        self.voice_configs = {
            "noir_detective": {
                "rate": 140,      # Slow, dramatic pace
                "volume": 0.8,
                "voice_index": 0  # Usually male voice
            },
            "mysterious": {
                "rate": 120,      # Even slower, more mysterious
                "volume": 0.7,
                "voice_index": 0
            },
            "energetic": {
                "rate": 180,      # Faster pace
                "volume": 0.9,
                "voice_index": 1  # Usually female voice
            }
        }
        
        # Set current voice style
        self.current_voice = "noir_detective"
        
        # Initialize TTS engine
        self.engine = None
        self.setup_engine()
    
    def setup_engine(self):
        """Setup the text-to-speech engine"""
        try:
            self.engine = pyttsx3.init()
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            print(f"✅ Found {len(voices)} voices available")
            
            # Apply current voice configuration
            self.apply_voice_config()
            
        except Exception as e:
            print(f"⚠️ Audio narrator not available: {e}")
            self.engine = None
    
    def apply_voice_config(self):
        """Apply the current voice configuration"""
        if not self.engine:
            return
        
        try:
            config = self.voice_configs[self.current_voice]
            voices = self.engine.getProperty('voices')
            
            # Set voice (male/female)
            if len(voices) > config['voice_index']:
                self.engine.setProperty('voice', voices[config['voice_index']].id)
            
            # Set rate and volume
            self.engine.setProperty('rate', config['rate'])
            self.engine.setProperty('volume', config['volume'])
            
            print(f"🎙️ Voice configured: {self.current_voice}")
            
        except Exception as e:
            print(f"⚠️ Voice configuration failed: {e}")
    
    def change_voice_style(self, style_name):
        """Change the narrator voice style"""
        if style_name in self.voice_configs:
            self.current_voice = style_name
            self.apply_voice_config()
            print(f"🎙️ Voice changed to: {style_name}")
        else:
            print(f"⚠️ Voice style '{style_name}' not found")
    
    def narrate_chapter(self, text, chapter_number=1, save_audio=True):
        """Convert text to speech for a chapter"""
        
        if not self.engine:
            print("⚠️ Audio narrator not available")
            return None
        
        try:
            print(f"🎙️ Generating narration for Chapter {chapter_number}...")
            
            if save_audio:
                # Save as audio file
                audio_path = self.save_narration(text, chapter_number)
                return audio_path
            else:
                # Just speak it (real-time)
                self.engine.say(text)
                self.engine.runAndWait()
                return "spoken"
                
        except Exception as e:
            print(f"⚠️ Narration failed: {e}")
            return None
    
    def save_narration(self, text, chapter_number):
        """Save narration as audio file"""
        try:
            os.makedirs("assets/audio_narration", exist_ok=True)
            
            filename = f"chapter_{chapter_number}_{self.current_voice}.wav"
            filepath = os.path.join("assets/audio_narration", filename)
            
            # Save to file
            self.engine.save_to_file(text, filepath)
            self.engine.runAndWait()
            
            print(f"✅ Audio saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"⚠️ Audio save failed: {e}")
            return None
    
    def get_available_voices(self):
        """Get list of available voice styles"""
        return list(self.voice_configs.keys())

# Test the narrator
if __name__ == "__main__":
    narrator = NoirNarrator()
    
    test_text = """Detective Morgan stepped through the rain-soaked streets. 
    The crime scene awaited, shrouded in mystery and danger. 
    This case would test every skill acquired over years of investigation."""
    
    # Test different voice styles
    for style in ["noir_detective", "mysterious", "energetic"]:
        narrator.change_voice_style(style)
        audio_path = narrator.narrate_chapter(test_text, chapter_number=1)
        print(f"Generated with {style}: {audio_path}")
