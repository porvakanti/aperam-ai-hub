"""
Home Page - Aperam AI Hub
Main dashboard with navigation and quick stats
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from ..utils.helpers import navigate_to_page, show_breadcrumb, create_metric_card, log_user_action
from ..utils.css_loader import get_branded_header_css
from src.services import news_service

def render_home_page():
    """Render the home page"""
    show_breadcrumb("🏠 Home")
    
    # Main header
    st.markdown(get_branded_header_css(
        title="Aperam AI Hub",
        subtitle="by Accelerate"
    ), unsafe_allow_html=True)
    
    # Log page view
    log_user_action("page_view", {"page": "home"})
    
    # Main navigation cards
    render_main_navigation()
    
    # Secondary navigation
    render_secondary_navigation()
    
    # Quick stats
    render_quick_stats()
    
    # AI News preview
    render_news_preview()

def render_main_navigation():
    """Render main navigation cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤖 Agent Studio", key="home_agents", use_container_width=True, 
                    help="Interactive AI agents and demos • 5 Agents Available"):
            log_user_action("navigation", {"destination": "agent_studio", "source": "home_main"})
            navigate_to_page("🤖 Agent Studio")
    
    with col2:
        if st.button("💡 Use Cases", key="home_cases", use_container_width=True, 
                    help="Submit your AI ideas • Smart intake process"):
            log_user_action("navigation", {"destination": "use_cases", "source": "home_main"})
            navigate_to_page("💡 Use Case Intake")
    
    with col3:
        if st.button("📚 Governance", key="home_gov", use_container_width=True, 
                    help="AI policies and frameworks • Enterprise ready"):
            log_user_action("navigation", {"destination": "governance", "source": "home_main"})
            navigate_to_page("📚 AI Governance")

def render_secondary_navigation():
    """Render secondary navigation cards"""
    st.markdown("### More Resources")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎓 AI Academy", key="home_academy", use_container_width=True, 
                    help="Learn AI technologies • Multiple learning paths"):
            log_user_action("navigation", {"destination": "academy", "source": "home_secondary"})
            navigate_to_page("🎓 AI Academy")
    
    with col2:
        if st.button("📰 AI News", key="home_news_btn", use_container_width=True, 
                    help="Latest AI developments • Breaking news & updates"):
            log_user_action("navigation", {"destination": "news", "source": "home_secondary"})
            navigate_to_page("📰 AI News")
    
    with col3:
        if st.button("📊 Analytics", key="home_analytics", use_container_width=True, 
                    help="Usage metrics • Performance insights"):
            log_user_action("navigation", {"destination": "analytics", "source": "home_secondary"})
            navigate_to_page("📊 Analytics Dashboard")

def render_quick_stats():
    """Render quick statistics section"""
    st.subheader("🎯 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    # TODO: Replace with real data from analytics service
    col1.metric("Active Users", "127", "12", help="Number of active users in the last 30 days")
    col2.metric("Use Cases Submitted", "23", "5", help="AI use cases submitted this month")
    col3.metric("Agents Deployed", "5", "2", help="Number of active AI agents")
    col4.metric("Success Rate", "94%", "2%", help="Overall success rate of AI initiatives")

def render_news_preview():
    """Render AI news preview section"""
    st.subheader("📰 Latest AI News")
    news_service.get_breaking_news(category_filter, limit=5)
    ''' 
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # TODO: Replace with real news data
        st.markdown("""
        **🔥 Trending Today:**
        - Claude 4 Sonnet released with enhanced reasoning capabilities
        - Google announces Gemini 2.0 with improved multimodal features
        - Microsoft introduces new AI agents for enterprise automation
        """)
        
        if st.button("📰 View All AI News", key="home_news"):
            log_user_action("navigation", {"destination": "news", "source": "home_news_preview"})
            navigate_to_page("📰 AI News")
    
    with col2:
        st.info("**Breaking:** OpenAI releases new o3 reasoning model")
        st.write("*2 hours ago*")
    '''

def get_home_page_data():
    """Get data for home page (future: from API/database)"""
    return {
        "active_users": 127,
        "use_cases_submitted": 23,
        "agents_deployed": 5,
        "success_rate": 0.94,
        "recent_news": [
            {
                "title": "Claude 4 Sonnet released with enhanced reasoning capabilities",
                "source": "Anthropic",
                "time": "2 hours ago"
            },
            {
                "title": "Google announces Gemini 2.0 with improved multimodal features",
                "source": "Google AI",
                "time": "4 hours ago"
            },
            {
                "title": "Microsoft introduces new AI agents for enterprise automation",
                "source": "Microsoft",
                "time": "6 hours ago"
            }
        ]
    }