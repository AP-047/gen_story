import streamlit as st

# Simple test app
st.title("🕵️ Noir Story Generator - Test")
st.write("Welcome to your AI storytelling project!")

# Simple user input
name = st.text_input("What's your detective name?")
if name:
    st.write(f"Hello Detective {name}! Your story begins...")

# Simple dropdown
story_mood = st.selectbox(
    "Choose your story mood:",
    ["Dark and Mysterious", "Suspenseful", "Classic Noir"]
)

if st.button("Generate Story Teaser"):
    st.write(f"Detective {name} steps into the {story_mood.lower()} world of crime...")
    st.write("*This is just a test - we'll add AI generation next!*")
