import streamlit as st

# Simple test to check if Streamlit works
st.title("🔍 Test App")
st.write("If you can see this, Streamlit is working!")

# Test if we can import our generator
try:
    from models.story_generator import NoirStoryGenerator
    st.success("✅ Story generator imported successfully!")
    
    # Test basic functionality
    if st.button("Test Generator"):
        with st.spinner("Testing..."):
            generator = NoirStoryGenerator()
            st.success("✅ Generator created successfully!")
            
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.write("Please check the error details above.")

st.write("---")
st.write("If everything above worked, the main app should work too.")
