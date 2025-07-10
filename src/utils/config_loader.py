"""
Configuration loader utilities for YAML files
"""
import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigLoader:
    """Load and manage YAML configuration files"""
    
    def __init__(self, config_dir: str = "src/config"):
        # Get the absolute path relative to the project root
        project_root = Path(__file__).parent.parent.parent
        self.config_dir = project_root / config_dir
        self._cache = {}
    
    def load_config(self, config_file: str, use_cache: bool = True) -> Dict[str, Any]:
        """Load configuration from YAML file with caching"""
        if use_cache and config_file in self._cache:
            return self._cache[config_file]
        
        config_path = self.config_dir / config_file
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                
            if use_cache:
                self._cache[config_file] = config
                
            return config
            
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file {config_file}: {e}")
    
    def get_agents_config(self) -> Dict[str, Any]:
        """Get agents configuration"""
        return self.load_config("agents.yaml")
    
    def get_news_sources_config(self) -> Dict[str, Any]:
        """Get news sources configuration"""
        return self.load_config("news_sources.yaml")
    
    def get_learning_paths_config(self) -> Dict[str, Any]:
        """Get learning paths configuration"""
        return self.load_config("learning_paths.yaml")
    
    def get_live_agents(self) -> list:
        """Get list of live agents"""
        config = self.get_agents_config()
        return config.get("live_agents", [])
    
    def get_demo_agents(self) -> list:
        """Get list of demo agents"""
        config = self.get_agents_config()
        return config.get("demo_agents", [])
    
    def get_agent_by_id(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get specific agent by ID"""
        config = self.get_agents_config()
        
        # Search in live agents
        for agent in config.get("live_agents", []):
            if agent.get("id") == agent_id:
                return agent
        
        # Search in demo agents
        for agent in config.get("demo_agents", []):
            if agent.get("id") == agent_id:
                return agent
        
        return None
    
    def get_news_sources_by_category(self, category: str) -> list:
        """Get news sources filtered by category"""
        config = self.get_news_sources_config()
        sources = []
        
        for source_category in ["primary_sources", "industry_sources", "research_sources", "social_sources", "enterprise_sources"]:
            for source in config.get(source_category, []):
                if source.get("category") == category:
                    sources.append(source)
        
        return sources
    
    def get_learning_path_by_id(self, path_id: str) -> Optional[Dict[str, Any]]:
        """Get specific learning path by ID"""
        config = self.get_learning_paths_config()
        
        for path in config.get("learning_paths", []):
            if path.get("id") == path_id:
                return path
        
        return None
    
    def get_quick_courses(self) -> list:
        """Get list of quick courses"""
        config = self.get_learning_paths_config()
        return config.get("quick_courses", [])
    
    def reload_config(self, config_file: str):
        """Reload configuration file and clear cache"""
        if config_file in self._cache:
            del self._cache[config_file]
        return self.load_config(config_file, use_cache=False)
    
    def clear_cache(self):
        """Clear all cached configurations"""
        self._cache.clear()

# Global instance
config_loader = ConfigLoader()

# Convenience functions
def get_agents_config():
    return config_loader.get_agents_config()

def get_news_sources_config():
    return config_loader.get_news_sources_config()

def get_learning_paths_config():
    return config_loader.get_learning_paths_config()

def get_live_agents():
    return config_loader.get_live_agents()

def get_demo_agents():
    return config_loader.get_demo_agents()

def get_agent_by_id(agent_id: str):
    return config_loader.get_agent_by_id(agent_id)

def get_learning_path_by_id(path_id: str):
    return config_loader.get_learning_path_by_id(path_id)

def get_quick_courses():
    return config_loader.get_quick_courses()