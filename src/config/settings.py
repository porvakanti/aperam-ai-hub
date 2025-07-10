"""
Configuration management for Aperam AI Hub
"""
import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AppSettings(BaseSettings):
    """Main application settings"""
    
    # Application Info
    name: str = Field(default="Aperam AI Hub", env="APP_NAME")
    version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Streamlit Configuration
    port: int = Field(default=8501, env="STREAMLIT_SERVER_PORT")
    headless: bool = Field(default=True, env="STREAMLIT_SERVER_HEADLESS")
    
    # Theme Configuration
    theme_base: str = Field(default="light", env="STREAMLIT_THEME_BASE")
    primary_color: str = Field(default="#490B42", env="STREAMLIT_THEME_PRIMARY_COLOR")
    background_color: str = Field(default="#ffffff", env="STREAMLIT_THEME_BACKGROUND_COLOR")
    secondary_background_color: str = Field(default="#f0f2f6", env="STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR")
    
    # Security
    secret_key: str = Field(default="dev-secret-key", env="SECRET_KEY")
    encryption_key: Optional[str] = Field(default=None, env="ENCRYPTION_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class AgentSettings(BaseSettings):
    """AI Agent configuration"""
    
    # Current Agent URLs
    vertex_ai_rd_agent_url: str = Field(default="https://vertex-ai-agent.com/rd", env="VERTEX_AI_RD_AGENT_URL")
    agent_timeout: int = Field(default=30, env="AGENT_TIMEOUT")
    
    # Future AI Provider Keys
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class NewsSettings(BaseSettings):
    """News aggregation configuration"""
    
    news_api_key: Optional[str] = Field(default=None, env="NEWS_API_KEY")
    rss_refresh_interval: int = Field(default=300, env="RSS_REFRESH_INTERVAL")  # 5 minutes
    max_news_articles: int = Field(default=50, env="MAX_NEWS_ARTICLES")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class DatabaseSettings(BaseSettings):
    """Database configuration (future)"""
    
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class AzureSettings(BaseSettings):
    """Azure integration configuration (future)"""
    
    client_id: Optional[str] = Field(default=None, env="AZURE_CLIENT_ID")
    client_secret: Optional[str] = Field(default=None, env="AZURE_CLIENT_SECRET")
    tenant_id: Optional[str] = Field(default=None, env="AZURE_TENANT_ID")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class AnalyticsSettings(BaseSettings):
    """Analytics and monitoring configuration"""
    
    enable_analytics: bool = Field(default=True, env="ENABLE_ANALYTICS")
    analytics_endpoint: Optional[str] = Field(default=None, env="ANALYTICS_ENDPOINT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instances
app_settings = AppSettings()
agent_settings = AgentSettings()
news_settings = NewsSettings()
database_settings = DatabaseSettings()
azure_settings = AzureSettings()
analytics_settings = AnalyticsSettings()

# Helper functions
def get_app_config():
    """Get application configuration"""
    return app_settings

def get_agent_config():
    """Get agent configuration"""
    return agent_settings

def get_news_config():
    """Get news configuration"""
    return news_settings

def is_development():
    """Check if running in development mode"""
    return app_settings.debug

def is_production():
    """Check if running in production mode"""
    return not app_settings.debug