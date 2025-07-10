"""
Helper utilities for Aperam AI Hub
"""
import streamlit as st
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
import json

def initialize_session_state():
    """Initialize required session state variables"""
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 Home"
    
    if 'agent_view' not in st.session_state:
        st.session_state.agent_view = 'main'
    
    if 'last_sidebar_page' not in st.session_state:
        st.session_state.last_sidebar_page = ""
    
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {}

def reset_agent_view():
    """Reset agent view to default state"""
    if 'agent_view' in st.session_state:
        st.session_state.agent_view = 'main'

def navigate_to_page(page_name: str):
    """Navigate to a specific page"""
    st.session_state.page = page_name
    reset_agent_view()
    st.rerun()

def show_breadcrumb(current_page: str):
    """Show breadcrumb navigation"""
    if current_page != "🏠 Home":
        if st.button("← Back to Home", key="breadcrumb"):
            navigate_to_page("🏠 Home")
        st.markdown("---")

def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = datetime.now(timezone.utc)
    
    # Format as "2 hours ago", "1 day ago", etc.
    now = datetime.now(timezone.utc)
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"

def create_metric_card(title: str, value: str, delta: str = None, help_text: str = None):
    """Create a metric card with optional delta and help text"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.metric(title, value, delta, help=help_text)

def create_status_badge(status: str, badge_type: str = "live") -> str:
    """Create status badge HTML"""
    badge_classes = {
        "live": "live-badge",
        "poc": "poc-badge",
        "development": "dev-badge",
        "inactive": "inactive-badge"
    }
    
    badge_class = badge_classes.get(badge_type, "live-badge")
    return f'<span class="{badge_class}">{status.upper()}</span>'

def display_agent_tile(agent: Dict[str, Any], tile_type: str = "live"):
    """Display an agent tile with proper styling"""
    badge_html = create_status_badge(agent.get('status', 'Unknown'), tile_type)
    
    capabilities = agent.get('capabilities', [])
    capabilities_html = "".join([f"<p>• {cap}</p>" for cap in capabilities[:3]])
    
    tile_html = f"""
    <div class="agent-tile" style="min-height: 250px; cursor: pointer;">
        <h2>{agent.get('name', 'Unknown Agent')}</h2>
        {badge_html}
        <br><br>
        <p>{agent.get('description', 'No description available')}</p>
        <h3>Capabilities:</h3>
        {capabilities_html}
        <br>
        <p><em>Click to access →</em></p>
    </div>
    """
    
    return tile_html

def display_news_card(news_item: Dict[str, Any]):
    """Display a news card with proper styling"""
    card_html = f"""
    <div class="demo-card">
        <h4>🔥 {news_item.get('title', 'No Title')}</h4>
        <p><strong>Source:</strong> {news_item.get('source', 'Unknown')} | <strong>Time:</strong> {news_item.get('time', 'Unknown')}</p>
        <p>{news_item.get('summary', 'No summary available')}</p>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def create_expandable_section(title: str, content: Dict[str, Any], expanded: bool = False):
    """Create an expandable section with content"""
    with st.expander(title, expanded=expanded):
        for key, value in content.items():
            if isinstance(value, list):
                st.write(f"**{key}:**")
                for item in value:
                    st.write(f"• {item}")
            else:
                st.write(f"**{key}:** {value}")

def validate_form_input(input_value: str, field_name: str, required: bool = True, min_length: int = 0) -> bool:
    """Validate form input with error display"""
    if required and not input_value:
        st.error(f"{field_name} is required")
        return False
    
    if input_value and len(input_value) < min_length:
        st.error(f"{field_name} must be at least {min_length} characters long")
        return False
    
    return True

def save_user_progress(user_id: str, progress_data: Dict[str, Any]):
    """Save user progress to session state (future: database)"""
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {}
    
    st.session_state.user_progress[user_id] = progress_data

def get_user_progress(user_id: str) -> Dict[str, Any]:
    """Get user progress from session state (future: database)"""
    return st.session_state.get('user_progress', {}).get(user_id, {})

def create_progress_bar(current: int, total: int, label: str = "Progress"):
    """Create a progress bar with label"""
    progress_percentage = current / total if total > 0 else 0
    st.progress(progress_percentage)
    st.write(f"**{label}:** {current}/{total} ({progress_percentage:.1%})")

def display_feature_coming_soon(feature_name: str):
    """Display a 'coming soon' message for features"""
    st.info(f"🚧 {feature_name} is coming soon! This feature is planned for a future release.")

def create_two_column_layout(left_content_func, right_content_func, left_ratio: int = 2, right_ratio: int = 1):
    """Create a two-column layout with custom ratios"""
    col1, col2 = st.columns([left_ratio, right_ratio])
    
    with col1:
        left_content_func()
    
    with col2:
        right_content_func()

def safe_json_parse(json_string: str, default_value: Any = None) -> Any:
    """Safely parse JSON string with fallback"""
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default_value

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def format_number(number: float, precision: int = 2) -> str:
    """Format number with proper precision"""
    if number >= 1_000_000:
        return f"{number / 1_000_000:.{precision}f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.{precision}f}K"
    else:
        return f"{number:.{precision}f}"

def create_download_button(content: str, filename: str, mime_type: str = "text/plain"):
    """Create a download button for content"""
    st.download_button(
        label=f"Download {filename}",
        data=content,
        file_name=filename,
        mime=mime_type
    )

def log_user_action(action: str, details: Dict[str, Any] = None):
    """Log user action for analytics (future: send to analytics service)"""
    if details is None:
        details = {}
    
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "details": details,
        "page": st.session_state.get('page', 'Unknown')
    }
    
    # For now, just add to session state
    # In production, this would send to an analytics service
    if 'user_actions' not in st.session_state:
        st.session_state.user_actions = []
    
    st.session_state.user_actions.append(log_entry)