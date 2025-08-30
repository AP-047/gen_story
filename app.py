# app.py

import os
import streamlit as st
from models.story_generator import NoirStoryGenerator
from media_generators.audio_narrator import NoirNarrator
from media_generators.background_music import NoirMusicPlayer
from media_generators.image_generator import NoirImageLoader

# Cache singletons
@st.cache_resource
def get_story_generator():
    return NoirStoryGenerator()

@st.cache_resource
def get_narrator():
    return NoirNarrator()

@st.cache_resource
def get_music_player():
    return NoirMusicPlayer()

@st.cache_resource
def get_image_loader():
    return NoirImageLoader()

def main():
    st.title("🕵️ Easy Noir Detective Stories")
    st.markdown("*Simple language, matching audio, and background music*")

    if 'profile' not in st.session_state:
        st.session_state.profile = None
    if 'chapters' not in st.session_state:
        st.session_state.chapters = None
    if 'audio_files' not in st.session_state:
        st.session_state.audio_files = None

    if st.session_state.profile is None:
        show_quiz()
    else:
        show_story()

def show_quiz():
    st.header("🎭 Create Your Detective Profile")
    with st.form("form"):
        name = st.text_input("Detective's name", "Detective Morgan")
        style = st.selectbox("Investigation approach", [
            "Methodical evidence analysis",
            "Intuitive gut feelings",
            "Psychological profiling"
        ])
        atm = st.selectbox("Story atmosphere", [
            "Rain-soaked city streets",
            "Smoke-filled jazz clubs",
            "Abandoned industrial areas"
        ])
        music = st.selectbox("Background music", ["hidden_truth", "mysterious_lights"])
        submit = st.form_submit_button("Start Story")
        if submit and name:
            st.session_state.profile = {
                'detective_name': name,
                'investigation_style': style,
                'atmosphere': atm,
                'music_choice': music
            }
            st.rerun()

def show_story():
    st.header(f"🔍 Case File: {st.session_state.profile['detective_name']}")
    if st.session_state.chapters is None:
        generate_story()
    display_story()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 New Profile"):
            reset()
            st.rerun()
    with col2:
        if st.button("🎲 New Story"):
            st.session_state.chapters = None
            st.session_state.audio_files = None
            st.rerun()
    with col3:
        if st.button("🎵 Toggle Music"):
            toggle_music()

def generate_story():
    progress = st.progress(0)
    st.info("📝 Generating story...")
    sg = get_story_generator()
    chapters = sg.generate_chapters(st.session_state.profile)
    st.session_state.chapters = chapters
    progress.progress(30)

    st.info("🎙️ Generating narration...")
    nr = get_narrator()
    audios = []
    for i,(_,text) in enumerate(chapters, start=1):
        path = nr.narrate_chapter(text, i)
        audios.append(path)
    st.session_state.audio_files = audios
    progress.progress(60)

    st.info("🎵 Starting music...")
    mp = get_music_player()
    mp.change_theme(st.session_state.profile['music_choice'])
    mp.play(volume=0.2)
    progress.progress(100)
    st.success("✅ Story ready!")

def display_story():
    il = get_image_loader()
    chapters = st.session_state.chapters
    audios = st.session_state.audio_files

    for i,(prompt,text) in enumerate(chapters, start=1):
        st.markdown(f"## Chapter {i}")
        img = il.get_image(i)
        if img: st.image(img, width=400)
        st.write(text)
        if audios[i-1]:
            st.audio(audios[i-1], format='audio/mp3')
        st.markdown("---")

def toggle_music():
    mp = get_music_player()
    if mp.is_playing:
        mp.stop()
    else:
        mp.play(volume=0.2)

def reset():
    st.session_state.profile = None
    st.session_state.chapters = None
    st.session_state.audio_files = None

if __name__ == "__main__":
    main()
