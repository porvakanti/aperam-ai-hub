import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Aperam AI Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Aperam/Accelerate branding
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #490B42 0%, #F1511B 100%);
    padding: 1.5rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.demo-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    border: 2px solid #e0e0e0;
    margin: 1rem 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}
.demo-card:hover {
    transform: translateY(-2px);
    border-color: #F1511B;
}
.agent-card {
    background: linear-gradient(135deg, #490B42 0%, #F1511B 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin: 1rem 0;
    box-shadow: 0 6px 16px rgba(0,0,0,0.2);
}
.agent-tile {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    border: 3px solid #490B42;
    margin: 1rem;
    text-align: center;
    box-shadow: 0 6px 16px rgba(73,11,66,0.1);
    transition: all 0.3s;
}
.agent-tile:hover {
    border-color: #F1511B;
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(241,81,27,0.2);
}
.live-badge {
    background: #28a745;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: bold;
}
.poc-badge {
    background: #17a2b8;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Sidebar navigation with logo
try:
    st.sidebar.image("Accelerate_main_logo.png", width=200)
except:
    st.sidebar.markdown("### 🚀 Accelerate")

st.sidebar.markdown("---")
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a section:", [
    "🏠 Home", 
    "🤖 Agent Space", 
    "💡 Use Case Intake", 
    "📚 AI Governance",
    "🎓 AI Academy",
    "📰 AI News",
    "📊 Analytics Dashboard"
])

# Update page based on session state OR sidebar selection
if 'page' in st.session_state:
    # If user clicked something, use that
    page = st.session_state.page
else:
    # Otherwise use sidebar selection
    pass

# Reset session state if sidebar selection changes
if page != st.session_state.get('last_sidebar_page', ''):
    st.session_state.last_sidebar_page = page
    if 'page' in st.session_state:
        del st.session_state.page
    if 'agent_view' in st.session_state:
        del st.session_state.agent_view

# Add breadcrumb to ALL pages except Home
def show_breadcrumb():
    if page != "🏠 Home":
        if st.button("← Back to Home", key="breadcrumb"):
            st.session_state.page = "🏠 Home"
            if 'agent_view' in st.session_state:
                del st.session_state.agent_view
            st.rerun()
        st.markdown("---")

# HOME PAGE
if page == "🏠 Home":
    show_breadcrumb()  # Will do nothing since it's Home page
    st.markdown("""
    <div class="main-header">
        <h1>Aperam AI Hub</h1>
        <h3>by Accelerate</h3>
        <p>Your Gateway to AI Transformation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Breadcrumb navigation
    if page != "🏠 Home":
        if st.button("← Back to Home", key="breadcrumb"):
            st.session_state.page = "🏠 Home"
            if 'agent_view' in st.session_state:
                del st.session_state.agent_view
            st.rerun()
        st.markdown("---")
    
    # Main navigation cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤖 Agent Space", key="home_agents", use_container_width=True, help="Interactive AI agents and demos • 5 Agents Available"):
            st.session_state.page = "🤖 Agent Space"
            st.rerun()
    
    with col2:
        if st.button("💡 Use Cases", key="home_cases", use_container_width=True, help="Submit your AI ideas • Smart intake process"):
            st.session_state.page = "💡 Use Case Intake"
            st.rerun()
    
    with col3:
        if st.button("📚 Governance", key="home_gov", use_container_width=True, help="AI policies and frameworks • Enterprise ready"):
            st.session_state.page = "📚 AI Governance"
            st.rerun()
    
    # Secondary navigation cards
    st.markdown("### More Resources")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎓 AI Academy", key="home_academy", use_container_width=True, help="Learn AI technologies • Multiple learning paths"):
            st.session_state.page = "🎓 AI Academy"
            st.rerun()
    
    with col2:
        if st.button("📰 AI News", key="home_news_btn", use_container_width=True, help="Latest AI developments • Breaking news & updates"):
            st.session_state.page = "📰 AI News"
            st.rerun()
    
    with col3:
        if st.button("📊 Analytics", key="home_analytics", use_container_width=True, help="Usage metrics • Performance insights"):
            st.session_state.page = "📊 Analytics Dashboard"
            st.rerun()
    
    st.subheader("🎯 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Users", "127", "12")
    col2.metric("Use Cases Submitted", "23", "5")
    col3.metric("Agents Deployed", "5", "2")
    col4.metric("Success Rate", "94%", "2%")
    
    # AI News Section on Homepage
    st.subheader("📰 Latest AI News")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **🔥 Trending Today:**
        - Claude 4 Sonnet released with enhanced reasoning capabilities
        - Google announces Gemini 2.0 with improved multimodal features
        - Microsoft introduces new AI agents for enterprise automation
        """)
        
        if st.button("📰 View All AI News", key="home_news"):
            st.session_state.page = "📰 AI News"
            st.rerun()
    
    with col2:
        st.info("**Breaking:** OpenAI releases new o3 reasoning model")
        st.write("*2 hours ago*")

# AGENT SPACE
elif page == "🤖 Agent Space":
    show_breadcrumb()
    st.title("🤖 Agent Space")
    st.write("Explore our AI capabilities through live agents and prototype demonstrations")
    
    # Initialize session state for agent selection
    if 'agent_view' not in st.session_state:
        st.session_state.agent_view = 'tiles'
    
    # Show tiles or detailed view based on state
    if st.session_state.agent_view == 'tiles':
        # Two main tiles - make them clickable containers
        col1, col2 = st.columns(2)
        
        with col1:
            # Use button as invisible overlay
            clicked_live = st.button("", key="live_tile", use_container_width=True, help="Access Live Production Agents")
            st.markdown("""
            <div class="agent-tile" style="min-height: 250px; cursor: pointer;">
                <h2>🔴 Live Production Agents</h2>
                <span class="live-badge">ENTERPRISE READY</span>
                <br><br>
                <p>Deployed and battle-tested AI agents ready for business use</p>
                <h3>Available Now:</h3>
                <p>• R&D Research Assistant</p>
                <p>• Materials Analysis Engine</p>
                <br>
                <p><em>Click anywhere to access →</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            if clicked_live:
                st.session_state.agent_view = 'live'
                st.rerun()
        
        with col2:
            # Use button as invisible overlay  
            clicked_demo = st.button("", key="demo_tile", use_container_width=True, help="Try Demo Agents")
            st.markdown("""
            <div class="agent-tile" style="min-height: 250px; cursor: pointer;">
                <h2>🧪 Portfolio & POCs</h2>
                <span class="poc-badge">TRY NOW</span>
                <br><br>
                <p>Interactive demos and proof-of-concepts showcasing AI capabilities</p>
                <h3>Experience:</h3>
                <p>• Document Intelligence</p>
                <p>• Steel Specs Assistant</p>
                <p>• Predictive Analytics</p>
                <br>
                <p><em>Click anywhere to try →</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            if clicked_demo:
                st.session_state.agent_view = 'demo'
                st.rerun()
    
    elif st.session_state.agent_view == 'live':
        # Back button
        if st.button("← Back to Agent Space", key="back_live"):
            st.session_state.agent_view = 'tiles'
            st.rerun()
        
        st.subheader("🔴 Production Agents")
        
        st.markdown("""
        <div class="agent-card">
            <h3>🧪 R&D Research Assistant</h3>
            <p>Specialized in materials research and alloy development</p>
            <p><em>Powered by Vertex AI & Gemini</em></p>
            <p><strong>Status:</strong> ✅ Active | <strong>Uptime:</strong> 99.8%</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Launch R&D Assistant", key="launch_rd"):
            st.balloons()
            st.success("🚀 R&D Assistant launched successfully!")
            st.markdown("**Agent URL:** Your Vertex AI R&D Assistant")
    
    elif st.session_state.agent_view == 'demo':
        # Back button
        if st.button("← Back to Agent Space", key="back_demo"):
            st.session_state.agent_view = 'tiles'
            st.rerun()
        
        st.subheader("🧪 Interactive Demos")
        
        demo_tab1, demo_tab2, demo_tab3 = st.tabs(["📄 Document Intelligence", "🔧 Steel Specs", "📊 Predictive Analytics"])
        
        with demo_tab1:
            st.subheader("📄 Document Intelligence Demo")
            uploaded_file = st.file_uploader("Upload a document to analyze", type=['pdf', 'txt', 'docx'])
            if uploaded_file:
                st.success("✅ Document uploaded! AI analysis complete.")
                st.write("**Key insights:**")
                st.write("- Document type: Technical specification")
                st.write("- Key topics: Steel composition, quality requirements") 
                st.write("- Action items: 3 recommendations identified")
        
        with demo_tab2:
            st.subheader("🔧 Steel Specs Assistant")
            query = st.text_input("Ask about steel specifications:")
            if query:
                st.write(f"🤖 **AI Response:** For {query}, I recommend using high-strength low-alloy steel with specific heat treatment...")
        
        with demo_tab3:
            st.subheader("📊 Predictive Analytics Simulator")
            if st.button("Run Prediction Model"):
                st.write("🎯 **Prediction Results:**")
                st.write("- Equipment failure probability: 15% (next 30 days)")
                st.write("- Recommended action: Schedule maintenance")
                st.write("- Confidence level: 94%")

# USE CASE INTAKE
elif page == "💡 Use Case Intake":
    show_breadcrumb()
    st.title("💡 AI Use Case Submission")
    st.write("Smart intake process to capture and evaluate your AI ideas")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Tell us about your challenge")
        
        business_area = st.selectbox("Business Area", [
            "Production & Operations",
            "Supply Chain",
            "Quality Control", 
            "R&D",
            "Sales & Marketing",
            "Finance",
            "Other"
        ])
        
        problem_description = st.text_area("Describe your business challenge:", 
                                         placeholder="e.g., We struggle with predicting equipment failures...")
        
        current_process = st.text_area("How do you handle this today?",
                                     placeholder="e.g., Manual inspections every 2 weeks...")
        
        expected_outcome = st.text_input("What outcome do you want?",
                                       placeholder="e.g., Reduce downtime by 20%")
        
        urgency = st.selectbox("Priority Level", ["Low", "Medium", "High", "Critical"])
        
        if st.button("🚀 Submit Use Case"):
            st.success("✅ Use case submitted successfully!")
            st.balloons()
            
            # Show AI-generated suggestions
            st.subheader("🤖 AI Recommendations")
            st.info("Based on your input, here are suggested AI approaches:")
            st.write("1. **Predictive Maintenance** - Use sensor data to predict failures")
            st.write("2. **Computer Vision** - Automated defect detection")
            st.write("3. **Time Series Analysis** - Pattern recognition in operational data")
    
    with col2:
        st.subheader("💡 Need inspiration?")
        st.write("**Popular use cases:**")
        example_cases = [
            "Demand forecasting",
            "Quality defect prediction", 
            "Energy optimization",
            "Inventory management",
            "Customer churn prevention"
        ]
        for case in example_cases:
            if st.button(f"📋 {case}", key=case):
                st.info(f"Great choice! {case} is perfect for AI.")

# AI GOVERNANCE
elif page == "📚 AI Governance":
    show_breadcrumb()
    st.title("📚 AI Governance Framework")
    
    tab1, tab2, tab3 = st.tabs(["📋 Policies", "🔒 Security", "📖 Best Practices"])
    
    with tab1:
        st.subheader("AI Governance Policies")
        st.write("**Current Status:** ✅ Approved by Leadership")
        
        policies = [
            "AI Ethics Guidelines",
            "Data Privacy Framework", 
            "Model Validation Standards",
            "Risk Assessment Protocols",
            "Vendor Management Policies"
        ]
        
        for policy in policies:
            with st.expander(f"📄 {policy}"):
                st.write(f"Detailed guidelines for {policy.lower()}...")
                st.download_button(f"Download {policy}", f"{policy}.pdf")
    
    with tab2:
        st.subheader("🔒 Security Requirements")
        st.write("Enterprise-grade security for all AI implementations")
        st.write("- ✅ Azure AD Integration")
        st.write("- ✅ Data Encryption at Rest")
        st.write("- ✅ Audit Logging")
        st.write("- ✅ Role-based Access Control")
    
    with tab3:
        st.subheader("📖 Implementation Best Practices")
        st.write("**Development Guidelines:**")
        st.code("""
        # AI Project Checklist
        □ Business case validation
        □ Data quality assessment  
        □ Model performance benchmarks
        □ Security review completion
        □ Governance compliance check
        """)

# AI NEWS
elif page == "📰 AI News":
    show_breadcrumb()
    st.title("📰 AI News Aggregator")
    st.write("Stay updated with the latest AI developments from industry leaders")
    
    tab1, tab2, tab3 = st.tabs(["🔥 Breaking News", "📰 Weekly Digest", "🏢 Enterprise AI"])
    
    with tab1:
        st.subheader("🔥 Breaking News & Latest Updates")
        
        # Simulated real-time news (you'll replace with actual RSS feeds)
        breaking_news = [
            {
                "title": "Claude 4 Sonnet Released with Enhanced Reasoning",
                "source": "Anthropic",
                "time": "2 hours ago",
                "summary": "Anthropic announces Claude 4 Sonnet with improved reasoning capabilities and enterprise features.",
                "url": "https://anthropic.com"
            },
            {
                "title": "Google Gemini 2.0 Introduces New Multimodal Features", 
                "source": "Google AI",
                "time": "4 hours ago",
                "summary": "Enhanced vision and audio processing capabilities for enterprise applications.",
                "url": "https://ai.google.dev"
            },
            {
                "title": "OpenAI Releases o3 Model with Advanced Reasoning",
                "source": "OpenAI",
                "time": "6 hours ago", 
                "summary": "New reasoning model shows significant improvements in complex problem solving.",
                "url": "https://openai.com"
            }
        ]
        
        for news in breaking_news:
            with st.container():
                st.markdown(f"""
                <div class="demo-card">
                    <h4>🔥 {news['title']}</h4>
                    <p><strong>Source:</strong> {news['source']} | <strong>Time:</strong> {news['time']}</p>
                    <p>{news['summary']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Read More", key=f"news_{news['source']}"):
                    st.info(f"Opening {news['url']}")
    
    with tab2:
        st.subheader("📰 Weekly AI Digest")
        st.write("**Week of July 1-7, 2025**")
        
        weekly_topics = [
            "🤖 **Agentic AI**: Multi-agent systems gaining enterprise adoption",
            "🔗 **MCP Protocol**: New standard for AI model communication",
            "🏭 **Industry AI**: Manufacturing and steel industry AI applications",
            "🔒 **AI Governance**: Latest enterprise AI security frameworks",
            "📊 **AI Analytics**: Performance metrics and ROI measurement tools"
        ]
        
        for topic in weekly_topics:
            st.write(topic)
            
        if st.button("📧 Subscribe to Weekly Digest"):
            st.success("✅ Subscribed to weekly AI digest!")
    
    with tab3:
        st.subheader("🏢 Enterprise AI Focus")
        st.write("**Curated content for enterprise AI implementation**")
        
        enterprise_news = [
            "Microsoft announces AI Copilot for manufacturing",
            "AWS launches new enterprise AI governance tools", 
            "Salesforce integrates advanced AI agents for CRM",
            "IBM releases AI for supply chain optimization"
        ]
        
        for news in enterprise_news:
            st.write(f"• {news}")

# AI ACADEMY  
elif page == "🎓 AI Academy":
    show_breadcrumb()
    st.title("🎓 AI Academy")
    st.write("Learn AI technologies and build expertise across your organization")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📚 Learning Paths")
        
        learning_paths = [
            {
                "title": "🤖 GenAI Fundamentals",
                "level": "Beginner",
                "duration": "2 hours",
                "topics": ["Prompt Engineering", "LLM Basics", "Use Case Identification"]
            },
            {
                "title": "🔗 Agentic AI Systems", 
                "level": "Intermediate",
                "duration": "4 hours",
                "topics": ["Agent Architecture", "Multi-Agent Systems", "MCP Protocol"]
            },
            {
                "title": "🏭 AI for Manufacturing",
                "level": "Advanced", 
                "duration": "6 hours",
                "topics": ["Predictive Maintenance", "Quality Control", "Supply Chain AI"]
            }
        ]
        
        for path in learning_paths:
            with st.expander(f"{path['title']} - {path['level']} ({path['duration']})"):
                st.write("**Topics covered:**")
                for topic in path['topics']:
                    st.write(f"• {topic}")
                if st.button(f"Start Learning", key=f"learn_{path['title']}"):
                    st.success(f"✅ Starting {path['title']} course!")
    
    with col2:
        st.subheader("🎯 Quick Start")
        st.write("**Popular courses:**")
        
        quick_courses = [
            "Prompt Engineering 101",
            "AI Ethics for Business", 
            "Building Your First Agent",
            "AI ROI Measurement"
        ]
        
        for course in quick_courses:
            if st.button(course, key=f"quick_{course}"):
                st.info(f"Loading {course}...")
        
        st.subheader("📊 Your Progress")
        st.progress(0.3)
        st.write("**Completed:** 3/10 courses")
        st.write("**Certificates:** 1 earned")
    
elif page == "📊 Analytics Dashboard":
    show_breadcrumb()    
    st.title("📊 AI Hub Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Usage Trends")
        # Sample data for demo
        chart_data = pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=30, freq='D'),
            'Daily Users': [20, 25, 30, 35, 40, 45, 50, 55, 60, 65] * 3
        })
        st.line_chart(chart_data.set_index('Date'))
    
    with col2:
        st.subheader("🎯 Popular Features")
        feature_data = pd.DataFrame({
            'Feature': ['R&D Agent', 'Document Analysis', 'Use Case Intake', 'Governance Docs'],
            'Usage': [45, 35, 25, 15]
        })
        st.bar_chart(feature_data.set_index('Feature'))
    
    st.subheader("📋 Recent Activity")
    activities = [
        "John D. submitted new use case: Quality prediction",
        "Sarah M. accessed R&D Research Assistant", 
        "Mike R. downloaded AI Ethics Guidelines",
        "Lisa K. completed Document Analysis demo"
    ]
    
    for activity in activities:
        st.write(f"• {activity}")

# Footer
st.markdown("---")
st.markdown("**Aperam AI Hub** | Built with ❤️ by the AI Team | Contact: ai-team@aperam.com")