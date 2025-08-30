import os
import streamlit as st
from models.story_generator import NoirStoryGenerator
from media_generators.image_generator import NoirImageLoader
from media_generators.audio_narrator import NoirNarrator
from media_generators.background_music import NoirMusicPlayer

# Cache resource singletons
@st.cache_resource
def load_story_generator():
    return NoirStoryGenerator()

@st.cache_resource
def load_image_loader():
    return NoirImageLoader()

@st.cache_resource
def load_narrator():
    return NoirNarrator()

@st.cache_resource
def load_music_player():
    return NoirMusicPlayer()

def main():
    st.title("🕵️ AI-Powered Noir Detective Stories")
    st.markdown("*With static visuals, Google TTS narration, and atmospheric music*")
    
    # Session state defaults
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    if 'current_story' not in st.session_state:
        st.session_state.current_story = None
    if 'story_audio' not in st.session_state:
        st.session_state.story_audio = None

    # Page flow
    if st.session_state.user_profile is None:
        show_personality_quiz()
    else:
        show_story_experience()

def show_personality_quiz():
    st.header("🎭 Create Your Detective Profile")
    with st.form("detective_profile"):
        name = st.text_input("Detective's name:", value="Detective Morgan")
        style = st.selectbox("Investigation approach:", [
            "Methodical evidence analysis",
            "Intuitive gut feelings",
            "Aggressive interrogation",
            "Psychological profiling"
        ])
        atmosphere = st.selectbox("Story atmosphere:", [
            "Rain-soaked city streets",
            "Smoke-filled jazz clubs",
            "Abandoned industrial areas",
            "Upscale corrupt society"
        ])
        music_choice = st.selectbox("Background music:", [
            "hidden_truth", "mysterious_lights"
        ])
        submitted = st.form_submit_button("🚀 Create My Story Experience")
        if submitted and name.strip():
            st.session_state.user_profile = {
                'detective_name': name.strip(),
                'investigation_style': style,
                'atmosphere': atmosphere,
                'music_choice': music_choice
            }
            st.rerun()

def show_story_experience():
    st.header(f"🔍 Case File: {st.session_state.user_profile['detective_name']}")
    if st.session_state.current_story is None:
        generate_complete_story()
    display_story_with_media()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎲 New Story"):
            reset_session()
            st.rerun()
    with col2:
        if st.button("🔄 Change Profile"):
            reset_session()
            st.session_state.user_profile = None
            st.rerun()
    with col3:
        if st.button("🎵 Toggle Music"):
            toggle_music()

def reset_session():
    st.session_state.current_story = None
    st.session_state.story_audio = None

def generate_complete_story():
    progress = st.progress(0)
    status = st.empty()

    # 1) Generate story
    status.text("📝 Writing your noir story...")
    sg = load_story_generator()
    text = sg.generate_complete_noir_story(st.session_state.user_profile)
    st.session_state.current_story = text
    progress.progress(50)

    # 2) Generate narration
    status.text("🎙️ Recording narration...")
    narrator = load_narrator()
    chapters = extract_chapters(text)
    audio_files = []
    for i, chap in enumerate(chapters, start=1):
        audio = narrator.narrate_chapter(chap, chapter_number=i)
        audio_files.append(audio)
    st.session_state.story_audio = audio_files
    progress.progress(100)
    status.text("✅ Story ready!")

def extract_chapters(story_text):
    parts = story_text.split('## Chapter')[1:]
    chapters = []
    for part in parts[:4]:
        lines = part.split('\n')
        content = '\n'.join(lines[2:]).strip()
        if len(content) > 500:
            content = content[:500] + "..."
        chapters.append(content)
    return chapters

def display_story_with_media():
    img_loader = load_image_loader()
    st.markdown("### 📖 Your Detective Story")
    for i, chap in enumerate(extract_chapters(st.session_state.current_story), start=1):
        st.markdown(f"## Chapter {i}")
        # static image
        img = img_loader.get_image(i)
        if img:
            st.image(img, width=400)
        # text
        st.markdown(chap)
        # audio
        audio = st.session_state.story_audio[i-1]
        if audio and os.path.exists(audio):
            st.audio(audio, format='audio/mp3')
        st.markdown("---")

def toggle_music():
    player = load_music_player()
    if player.is_playing:
        player.stop()
        st.success("🎵 Music stopped")
    else:
        choice = st.session_state.user_profile['music_choice']
        player.change_theme(choice)
        if player.play(volume=0.2):
            st.success(f"🎵 Playing: {choice}")
        else:
            st.warning("🎵 Music file not found")

if __name__ == "__main__":
    main()
