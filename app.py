import streamlit as st
from models.story_generator import NoirStoryGenerator

# Initialize the story generator (cached for performance)
@st.cache_resource
def load_story_generator():
    return NoirStoryGenerator()

def main():
    st.title("🕵️ AI-Powered Noir Detective Stories")
    st.markdown("*Step into the shadows of crime and mystery...*")
    
    # Initialize session state
    if 'story_generator' not in st.session_state:
        try:
            with st.spinner("Loading AI storyteller..."):
                st.session_state.story_generator = load_story_generator()
        except Exception as e:
            st.error(f"Error loading AI model: {e}")
            st.stop()
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    
    if 'current_story' not in st.session_state:
        st.session_state.current_story = None

    # Show personality quiz or story
    if st.session_state.user_profile is None:
        show_personality_quiz()
    else:
        show_story_experience()

def show_personality_quiz():
    st.header("🎭 Create Your Detective Profile")
    
    with st.form("detective_profile"):
        detective_name = st.text_input("Detective's name:", value="Detective Morgan")
        
        investigation_style = st.selectbox(
            "Investigation approach:",
            ["Methodical evidence analysis", "Intuitive gut feelings", "Aggressive interrogation", "Psychological profiling"]
        )
        
        atmosphere_preference = st.selectbox(
            "Story atmosphere:",
            ["Rain-soaked city streets", "Smoke-filled jazz clubs", "Abandoned industrial areas", "Upscale corrupt society"]
        )
        
        submitted = st.form_submit_button("🚀 Generate My Story")
        
        if submitted and detective_name.strip():
            st.session_state.user_profile = {
                'detective_name': detective_name.strip(),
                'investigation_style': investigation_style,
                'atmosphere': atmosphere_preference
            }
            st.rerun()

def show_story_experience():
    st.header(f"🔍 Case File: {st.session_state.user_profile['detective_name']}")
    
    if st.session_state.current_story is None:
        with st.spinner("🧠 Generating your noir story..."):
            try:
                story_text = st.session_state.story_generator.generate_complete_noir_story(
                    st.session_state.user_profile
                )
                st.session_state.current_story = story_text
            except Exception as e:
                st.error(f"Error generating story: {e}")
                return
    
    # Display story
    st.markdown("### 📖 Your Story")
    st.markdown(st.session_state.current_story)
    
    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 New Story"):
            st.session_state.current_story = None
            st.rerun()
    
    with col2:
        if st.button("🔄 Change Profile"):
            st.session_state.user_profile = None
            st.session_state.current_story = None
            st.rerun()

if __name__ == "__main__":
    main()
