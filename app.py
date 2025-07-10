"""
Aperam AI Hub - Main Application
Modular Streamlit application for AI Hub
"""
import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import configuration and utilities
from src.config.settings import get_app_config
from src.utils.css_loader import load_main_css
from src.utils.helpers import initialize_session_state, log_user_action

# Import pages
from src.pages.home import render_home_page
from src.pages.agent_space import render_agent_space
from src.pages.use_cases import render_use_cases_page
from src.pages.governance import render_governance_page
from src.pages.academy import render_academy_page
from src.pages.news import render_news_page
# from src.pages.analytics import render_analytics_page

def main():
    """Main application function"""
    
    # Get configuration
    config = get_app_config()
    
    # Page configuration
    st.set_page_config(
        page_title=config.name,
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load CSS
    load_main_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar and handle navigation
    render_sidebar()
    
    # Handle navigation
    handle_navigation()
    
    # Render footer
    render_footer()

def render_sidebar():
    """Render sidebar navigation"""
    try:
        st.sidebar.image("static/images/Accelerate_main_logo.png", width=200)
    except:
        st.sidebar.markdown("### 🚀 Accelerate")
    
    st.sidebar.markdown("---")
    st.sidebar.title("AI Hub Navigation")
    
    # Navigation options
    page_options = [
        "🏠 Home", 
        "🤖 Agent Studio", 
        "💡 Use Case Intake", 
        "📚 AI Governance",
        "🎓 AI Academy",
        "📰 AI News",
        "📊 Analytics Dashboard"
    ]
    
    # Get current page from session state
    current_page = st.session_state.get('page', '🏠 Home')
    
    # Find current index for dropdown
    try:
        current_index = page_options.index(current_page)
    except ValueError:
        current_index = 0
    
    # Create selectbox with current page selected
    selected_page = st.sidebar.selectbox(
        "Choose a section:", 
        page_options,
        index=current_index
    )
    
    # If selection changed, update session state
    if selected_page != current_page:
        st.session_state.page = selected_page
        # Reset agent view when navigating
        if 'agent_view' in st.session_state:
            del st.session_state.agent_view
        st.rerun()

def handle_navigation():
    """Handle page navigation and routing"""
    # Get current page
    page = st.session_state.get('page', '🏠 Home')
    
    # Log page navigation
    log_user_action("page_navigation", {"page": page})
    
    # Route to appropriate page
    if page == "🏠 Home":
        render_home_page()
    elif page == "🤖 Agent Studio":
        render_agent_space()
    elif page == "💡 Use Case Intake":
        render_use_cases_page()
    elif page == "📚 AI Governance":
        render_governance_page()
    elif page == "🎓 AI Academy":
        render_academy_page()
    elif page == "📰 AI News":
        render_news_page()
    elif page == "📊 Analytics Dashboard":
        render_placeholder_page("Analytics Dashboard", "📊")
    else:
        render_home_page()

def render_placeholder_page(page_name: str, icon: str):
    """Render placeholder page for pages not yet implemented"""
    # Temporary navigation back to home
    if st.button("← Back to Home"):
        st.session_state.page = "🏠 Home"
        st.rerun()

    st.title(f"{icon} {page_name}")
    st.info(f"🚧 {page_name} is being migrated to the new modular architecture. Coming soon!")
    
    # Show progress
    st.progress(0.3)
    st.write("**Migration Progress:** 30% complete")    
    

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("**Aperam AI Hub** | Built with ❤️ by the AI Team | Contact: ai-team@aperam.com")
    
    # Development info (only in debug mode)
    config = get_app_config()
    if config.debug:
        st.markdown(f"*Version: {config.version} | Debug Mode: Enabled*")

if __name__ == "__main__":
    main()