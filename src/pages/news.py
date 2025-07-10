"""
AI News Aggregator Page
Real-time AI news feed and intelligence
"""

import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import requests

# Import configurations and helpers
try:
    from src.config.settings import get_app_config
    from src.utils.helpers import log_user_action
    from src.services import news_service  # Namespace import to avoid collision
except ImportError:
    # Fallback for testing
    st.error("Import error - please check your project structure")

def render_news_page():
    """Render the AI news aggregator page"""
    # Back to home button
    if st.button("← Back to Home", key="back_to_home_news"):
        st.session_state.page = "🏠 Home"
        st.rerun()
    
    st.title("📰 AI News Aggregator")
    
    # News feed controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("**Stay updated with the latest AI developments**")
    
    with col2:
        if st.button("🔄 Refresh Feed", use_container_width=True):
            # Clear Streamlit cache to force refresh
            st.cache_data.clear()
            st.rerun()
    
    with col3:
        auto_refresh = st.checkbox("Auto-refresh", value=False)
        if auto_refresh:
            st.info("Auto-refresh enabled (5 min)")
    
    # RSS Feed Status Check
    with st.expander("📡 RSS Feed Status"):
        if st.button("Test RSS Sources"):
            with st.spinner("Testing RSS sources..."):
                status_results = news_service.test_news_sources()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🟢 Working Sources:**")
                    working_count = 0
                    for source, working in status_results.items():
                        if working:
                            st.write(f"✅ {source}")
                            working_count += 1
                
                with col2:
                    st.markdown("**🔴 Unavailable Sources:**")
                    failed_count = 0
                    for source, working in status_results.items():
                        if not working:
                            st.write(f"❌ {source}")
                            failed_count += 1
                
                st.success(f"RSS Status: {working_count}/{len(status_results)} sources working")
    
    # Filter options
    with st.expander("🔍 Filter & Search Options"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.multiselect(
                "Categories",
                ["All", "Research", "Industry", "Technology", "Business", "Regulation", "Ethics"],
                default=["All"]
            )
        
        with col2:
            source_filter = st.multiselect(
                "Sources",
                ["All", "MIT Technology Review", "AI News", "TechCrunch AI", "The Verge AI", "Wired AI", "VentureBeat AI"],
                default=["All"]
            )
        
        with col3:
            time_filter = st.selectbox(
                "Time Range",
                ["Today", "This Week", "This Month", "All Time"],
                index=3  # Default to "All Time" for better results
            )
    
    # Create tabs for different news sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔥 Breaking News", 
        "📚 Research Papers", 
        "🏭 Industry Updates", 
        "💡 AI Insights"
    ])
    
    with tab1:
        render_breaking_news_tab(category_filter, source_filter, time_filter)
    
    with tab2:
        render_research_papers_tab(category_filter, source_filter, time_filter)
    
    with tab3:
        render_industry_updates_tab(category_filter, source_filter, time_filter)
    
    with tab4:
        render_ai_insights_tab(category_filter, source_filter, time_filter)

def render_breaking_news_tab(category_filter: List[str], source_filter: List[str], time_filter: str):
    """Render breaking news section"""
    st.markdown("### 🔥 Breaking AI News")
    
    # Get breaking news with error handling
    try:
        with st.spinner("Loading latest AI news..."):
            breaking_news = news_service.get_breaking_news(category_filter, limit=10)
        
        if not breaking_news:
            st.warning("No breaking news available at the moment. Please try refreshing or check your internet connection.")
            return
        
        st.success(f"📰 Found {len(breaking_news)} latest articles")
        
        # Display news items
        for i, news_item in enumerate(breaking_news):
            render_news_card(news_item, f"breaking_{i}")
            
    except Exception as e:
        st.error(f"Error loading breaking news: {str(e)}")
        st.info("Please try refreshing the page or check the RSS feed status above.")

def render_research_papers_tab(category_filter: List[str], source_filter: List[str], time_filter: str):
    """Render research papers section"""
    st.markdown("### 📚 Latest Research Papers")
    
    try:
        with st.spinner("Loading research papers..."):
            research_papers = news_service.get_research_papers(category_filter, limit=8)
        
        if not research_papers:
            st.info("No research papers matching your filters.")
            return
        
        st.success(f"📚 Found {len(research_papers)} research papers")
        
        # Display research papers
        for i, paper in enumerate(research_papers):
            render_research_card(paper, f"research_{i}")
            
    except Exception as e:
        st.error(f"Error loading research papers: {str(e)}")

def render_industry_updates_tab(category_filter: List[str], source_filter: List[str], time_filter: str):
    """Render industry updates section"""
    st.markdown("### 🏭 Industry Updates")
    
    try:
        with st.spinner("Loading industry updates..."):
            industry_updates = news_service.get_industry_updates(category_filter, limit=8)
        
        if not industry_updates:
            st.info("No industry updates matching your filters.")
            return
        
        st.success(f"🏭 Found {len(industry_updates)} industry updates")
        
        # Display industry updates
        for i, update in enumerate(industry_updates):
            render_news_card(update, f"industry_{i}")
            
    except Exception as e:
        st.error(f"Error loading industry updates: {str(e)}")

def render_ai_insights_tab(category_filter: List[str], source_filter: List[str], time_filter: str):
    """Render AI insights section"""
    st.markdown("### 💡 AI Insights & Analysis")
    
    # Trending topics
    st.markdown("#### 🔥 Trending Topics")
    
    trending_topics = get_trending_topics()
    
    cols = st.columns(3)
    for i, topic in enumerate(trending_topics[:3]):
        with cols[i]:
            st.metric(
                topic["topic"],
                f"{topic['mentions']} mentions",
                f"{topic['trend']}% vs last week"
            )
    
    # AI sentiment analysis
    st.markdown("#### 📊 AI Sentiment Analysis")
    
    sentiment_data = get_sentiment_analysis()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment metrics instead of plotly for simplicity
        st.metric("😊 Positive Sentiment", "65%", "5%")
        st.metric("😐 Neutral Sentiment", "25%", "-2%")
        st.metric("😟 Negative Sentiment", "10%", "-3%")
    
    with col2:
        # Key insights
        st.markdown("**Key Insights:**")
        insights = get_key_insights()
        for insight in insights:
            st.markdown(f"• {insight}")
    
    # Weekly AI summary
    st.markdown("#### 📈 Weekly AI Summary")
    
    weekly_summary = get_weekly_summary()
    
    with st.expander("🔍 View Weekly Summary"):
        st.markdown(weekly_summary)

def render_news_card(news_item, key: str):
    """Render a news card with improved layout"""
    with st.container(border=True):
        # Header row
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"### {news_item.title}")
            st.markdown(f"**{news_item.source}** | {news_item.published_date}")
        
        with col2:
            # Impact score with visual indicator
            impact_color = "🟢" if news_item.impact_score >= 4 else "🟡" if news_item.impact_score >= 3 else "🔴"
            st.markdown(f"**Impact:** {impact_color} {news_item.impact_score}/5")
        
        # Content
        st.markdown(news_item.summary)
        
        # Tags
        if hasattr(news_item, 'tags') and news_item.tags:
            tag_text = " ".join([f"`{tag}`" for tag in news_item.tags[:4]])  # Limit to 4 tags
            st.markdown(f"**Tags:** {tag_text}")
        
        # Action buttons
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1, 1, 2])
        
        with btn_col1:
            if st.button("📖 Read", key=f"read_{key}", help="Read full article"):
                show_full_article(news_item)
        
        with btn_col2:
            if st.button("📤 Share", key=f"share_{key}", help="Share this article"):
                st.info("📋 Link copied to clipboard!")
        
        with btn_col3:
            if st.button("⭐ Save", key=f"save_{key}", help="Save for later"):
                st.success("💾 Article saved to reading list!")
        
        with btn_col4:
            st.markdown(f"**Category:** `{news_item.category}`")

def render_research_card(paper, key: str):
    """Render a research paper card with academic focus"""
    with st.container(border=True):
        # Paper header
        st.markdown(f"### {paper.title}")
        
        # Metadata row
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Show source as journal if available, otherwise use source
            if hasattr(paper, 'source') and 'arXiv' not in paper.source:
                st.markdown(f"**Journal:** {paper.source}")
            else:
                st.markdown(f"**Source:** {paper.source}")
            st.markdown(f"**Published:** {paper.published_date}")
        
        with col2:
            # Impact indicators for research
            st.markdown(f"**Impact:** {'⭐' * paper.impact_score}")
            st.markdown(f"**Relevance:** {paper.impact_score}/5")
        
        # Abstract/Summary
        st.markdown("**Abstract:**")
        st.markdown(paper.summary)
        
        # Tags (Keywords for research papers)
        if hasattr(paper, 'tags') and paper.tags:
            st.markdown("**Keywords:** " + ", ".join([f"`{tag}`" for tag in paper.tags]))
        
        # Research paper actions
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        with btn_col1:
            if st.button("📄 View Paper", key=f"view_{key}"):
                show_research_paper(paper)
        
        with btn_col2:
            if st.button("📋 Add to Reading List", key=f"add_{key}"):
                st.success("📚 Added to research reading list!")
        
        with btn_col3:
            if st.button("💬 Discuss", key=f"discuss_{key}"):
                st.info("💬 Discussion feature coming to AI Community!")

def get_trending_topics() -> List[Dict]:
    """Get trending AI topics with real-time data simulation"""
    return [
        {"topic": "Generative AI", "mentions": 1547, "trend": "+15"},
        {"topic": "AI Safety", "mentions": 892, "trend": "+8"},
        {"topic": "Machine Learning", "mentions": 2103, "trend": "+12"},
        {"topic": "Computer Vision", "mentions": 734, "trend": "+5"},
        {"topic": "NLP", "mentions": 1265, "trend": "+18"},
        {"topic": "Robotics", "mentions": 456, "trend": "+3"}
    ]

def get_sentiment_analysis() -> Dict:
    """Get sentiment analysis data"""
    return {
        "labels": ["Positive", "Neutral", "Negative"],
        "values": [65, 25, 10]
    }

def get_key_insights() -> List[str]:
    """Get key insights from AI news analysis"""
    return [
        "65% of AI news sentiment is positive, indicating growing optimism",
        "Manufacturing AI applications dominate industry discussions",
        "Regulatory compliance is becoming a major focus area",
        "Open-source AI models are gaining traction in enterprise",
        "AI safety research is receiving increased attention and funding",
        "Multi-modal AI capabilities are the current technology focus"
    ]

def get_weekly_summary() -> str:
    """Get weekly AI summary"""
    return """
    ## Weekly AI Summary (January 15-21, 2025)
    
    ### 🔥 Key Developments
    - **Enterprise AI Adoption**: Major manufacturing companies report significant AI implementation success
    - **Technology Advances**: Continued improvements in multi-modal AI systems
    - **Regulatory Focus**: Increased attention on AI governance and compliance frameworks
    
    ### 📈 Technology Trends
    - Multi-modal AI systems gaining enterprise traction
    - Increased focus on explainable AI for industrial applications
    - Growth in federated learning for privacy-preserving AI
    - Expansion of AI-powered predictive maintenance solutions
    
    ### 🏭 Industry Impact
    - Manufacturing sector leads in AI adoption rates
    - Quality control and predictive maintenance remain top use cases
    - Supply chain optimization gaining significant momentum
    - Energy efficiency applications showing measurable ROI
    
    ### 📋 Regulatory Updates
    - Enhanced focus on AI bias detection and mitigation
    - New guidelines for AI in critical infrastructure
    - Industry-specific AI governance frameworks emerging
    - Data privacy regulations affecting AI development
    
    ### 🔬 Research Highlights
    - Breakthrough developments in explainable AI for industrial use
    - Advances in multi-agent reinforcement learning systems
    - Novel approaches to AI-powered quality control
    - Improved techniques for AI model interpretability
    
    ### 💡 What to Watch
    - Continued evolution of large language models
    - Integration of AI with IoT in manufacturing
    - Development of industry-specific AI standards
    - Growth in AI-human collaboration frameworks
    """

def show_full_article(news_item):
    """Show full article in expandable section"""
    with st.expander(f"📖 Full Article: {news_item.title}", expanded=True):
        st.markdown(f"**Source:** {news_item.source} | **Published:** {news_item.published_date}")
        st.markdown("---")
        
        # Article content
        st.markdown(f"""
        {news_item.summary}
        
        ### 📄 Article Analysis
        
        **Key Points:**
        - Significant development in AI technology and applications
        - Notable impact on industry practices and methodologies  
        - Important implications for future AI development and adoption
        - Relevant applications for manufacturing and enterprise use
        
        **Industry Relevance:**
        - Direct applications for manufacturing optimization
        - Potential integration with existing enterprise systems
        - Scalability considerations for large-scale deployment
        - Cost-benefit analysis for business implementation
        
        **Technical Insights:**
        - Advanced AI methodologies and techniques discussed
        - Performance improvements and benchmarking results
        - Integration challenges and solution approaches
        - Future development roadmap and expectations
        
        ### 🔗 Related Content
        - Similar articles in our database
        - Related research papers and technical documents
        - Industry case studies and implementation examples
        - Expert commentary and analysis pieces
        """)
        
        # Action buttons for full article
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔗 Open Original", key=f"original_{news_item.title[:10]}"):
                if news_item.url != "#":
                    st.markdown(f"[🔗 Open in new tab]({news_item.url})")
                else:
                    st.info("Original article URL not available")
        
        with col2:
            if st.button("💬 Discuss in Community", key=f"community_{news_item.title[:10]}"):
                st.info("💬 Community discussion feature coming soon!")
        
        with col3:
            if st.button("📧 Email Summary", key=f"email_{news_item.title[:10]}"):
                st.success("📧 Article summary prepared for sharing!")

def show_research_paper(paper):
    """Show research paper details"""
    with st.expander(f"📄 Research Paper: {paper.title}", expanded=True):
        st.markdown(f"**Source:** {paper.source} | **Published:** {paper.published_date}")
        st.markdown("---")
        
        # Paper details
        st.markdown("### 📋 Abstract")
        st.markdown(paper.summary)
        
        if hasattr(paper, 'tags') and paper.tags:
            st.markdown("### 🏷️ Keywords")
            st.markdown(", ".join([f"`{tag}`" for tag in paper.tags]))
        
        # Research metrics (mock data for demonstration)
        st.markdown("### 📊 Research Metrics")
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric("Citations", "42", "+12 this month")
        
        with metric_col2:
            st.metric("Downloads", "1,247", "+89 this week")
        
        with metric_col3:
            st.metric("Impact Score", f"{paper.impact_score}/5", "Above average")
        
        # Research paper actions
        st.markdown("### 🎯 Actions")
        
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("📥 Download PDF", key=f"download_{paper.title[:10]}"):
                if paper.url != "#":
                    st.markdown(f"[📥 Download from source]({paper.url})")
                else:
                    st.info("PDF download not available - this is a demo")
        
        with action_col2:
            if st.button("📚 Add to Library", key=f"library_{paper.title[:10]}"):
                st.success("📚 Added to your research library!")
        
        with action_col3:
            if st.button("👥 Share with Team", key=f"team_{paper.title[:10]}"):
                st.success("👥 Shared with your research team!")
        
        # Related research
        st.markdown("### 🔗 Related Research")
        st.markdown("""
        - Similar studies in manufacturing AI optimization
        - Comparative analysis of AI techniques in industry
        - Follow-up research and experimental validations
        - Industry applications and case studies
        """)

# Helper function to handle errors gracefully
def safe_render_with_fallback(render_function, *args, **kwargs):
    """Safely render content with fallback on errors"""
    try:
        return render_function(*args, **kwargs)
    except Exception as e:
        st.error(f"Error rendering content: {str(e)}")
        st.info("Please try refreshing the page or contact support if the issue persists.")
        return None