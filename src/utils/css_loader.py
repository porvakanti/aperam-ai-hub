"""
CSS loader utilities for Streamlit
"""
import streamlit as st
from pathlib import Path
from typing import Optional

class CSSLoader:
    """Load and inject CSS styles into Streamlit"""
    
    def __init__(self, css_dir: str = "static/css"):
        # Get the absolute path relative to the project root
        project_root = Path(__file__).parent.parent.parent
        self.css_dir = project_root / css_dir
    
    def load_css_file(self, css_file: str) -> str:
        """Load CSS content from file"""
        css_path = self.css_dir / css_file
        
        if not css_path.exists():
            raise FileNotFoundError(f"CSS file not found: {css_path}")
        
        try:
            with open(css_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Error reading CSS file {css_file}: {e}")
    
    def inject_css(self, css_content: str, unsafe_allow_html: bool = True):
        """Inject CSS into Streamlit app"""
        st.markdown(
            f"<style>{css_content}</style>",
            unsafe_allow_html=unsafe_allow_html
        )
    
    def load_and_inject_css(self, css_file: str):
        """Load CSS file and inject into Streamlit"""
        css_content = self.load_css_file(css_file)
        self.inject_css(css_content)
    
    def load_main_css(self):
        """Load main CSS file"""
        try:
            self.load_and_inject_css("main.css")
        except Exception as e:
            # If CSS fails to load, continue without styling
            print(f"Warning: Could not load main CSS: {e}")
            pass
    
    def inject_custom_css(self, css_rules: str):
        """Inject custom CSS rules"""
        self.inject_css(css_rules)

# Global instance
css_loader = CSSLoader()

# Convenience functions
def load_main_css():
    """Load main CSS styles"""
    css_loader.load_main_css()

def inject_custom_css(css_rules: str):
    """Inject custom CSS rules"""
    css_loader.inject_custom_css(css_rules)

def load_css_file(css_file: str) -> str:
    """Load CSS content from file"""
    return css_loader.load_css_file(css_file)

# Common CSS utilities
def get_branded_header_css(title: str, subtitle: str = None) -> str:
    """Generate branded header CSS"""
    subtitle_html = f"<h3>{subtitle}</h3>" if subtitle else ""
    
    return f"""
    <div class="main-header">
        <h1>{title}</h1>
        {subtitle_html}
    </div>
    """

def get_agent_card_css(agent: dict) -> str:
    """Generate agent card CSS"""
    return f"""
    <div class="agent-card">
        <h3>{agent.get('name', 'Unknown Agent')}</h3>
        <p>{agent.get('description', 'No description available')}</p>
        <p><em>Powered by {agent.get('provider', 'Unknown')} & {agent.get('model', 'Unknown')}</em></p>
        <p><strong>Status:</strong> ✅ {agent.get('status', 'Unknown')} | <strong>Uptime:</strong> {agent.get('uptime', 'N/A')}</p>
    </div>
    """

def get_demo_card_css(title: str, content: str) -> str:
    """Generate demo card CSS"""
    return f"""
    <div class="demo-card">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """