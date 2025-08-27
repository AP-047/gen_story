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
        with st.spinner("Loading AI storyteller..."):
            st.session_state.story_generator = load_story_generator()
    
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
    st.write("Answer a few questions to personalize your noir experience...")
    
    with st.form("detective_profile"):
        detective_name = st.text_input(
            "What's your detective's name?", 
            value="Detective Morgan",
            help="This will be your character in the story"
        )
        
        investigation_style = st.selectbox(
            "Your investigation approach:",
            [
                "Methodical evidence analysis",
                "Intuitive gut feelings", 
                "Aggressive interrogation",
                "Psychological profiling"
            ],
            help="How does your detective solve cases?"
        )
        
        atmosphere_preference = st.selectbox(
            "Your preferred story atmosphere:",
            [
                "Rain-soaked city streets",
                "Smoke-filled jazz clubs",
                "Abandoned industrial areas", 
                "Upscale corrupt society"
            ],
            help="What setting appeals to you most?"
        )
        
        story_complexity = st.selectbox(
            "Story complexity level:",
            ["Simple mystery", "Complex investigation", "Psychological thriller"],
            help="How intricate should your story be?"
        )
        
        submitted = st.form_submit_button("🚀 Generate My Story")
        
        if submitted and detective_name.strip():
            st.session_state.user_profile = {
                'detective_name': detective_name.strip(),
                'investigation_style': investigation_style,
                'atmosphere': atmosphere_preference,
                'complexity': story_complexity
            }
            st.rerun()

def show_story_experience():
    st.header(f"🔍 Case File: {st.session_state.user_profile['detective_name']}")
    
    # Story generation
    if st.session_state.current_story is None:
        with st.spinner("🧠 AI is crafting your personalized noir story..."):
            story_text = st.session_state.story_generator.generate_noir_story(
                st.session_state.user_profile, 
                scene_type="opening"
            )
            st.session_state.current_story = story_text
    
    # Display story
    st.markdown("### 📖 Your Story Begins...")
    story_container = st.container()
    
    with story_container:
        st.markdown(f"**Setting:** {st.session_state.user_profile['atmosphere']}")
        st.markdown(f"**Investigation Style:** {st.session_state.user_profile['investigation_style']}")
        st.markdown("---")
        
        # Display the AI-generated story
        st.markdown(st.session_state.current_story)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎲 Generate New Story"):
            st.session_state.current_story = None
            st.rerun()
    
    with col2:
        if st.button("🔄 Change Detective Profile"):
            st.session_state.user_profile = None
            st.session_state.current_story = None
            st.rerun()
    
    with col3:
        if st.button("📱 Continue Story"):
            st.info("Story continuation coming in next phase! 🚀")

if __name__ == "__main__":
    main()
