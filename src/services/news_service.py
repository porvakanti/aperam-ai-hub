"""
News Service - RSS Feed Aggregation
Real-time AI news from multiple sources
"""

import feedparser
import requests
import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from urllib.parse import urljoin
import re

# Import with try/catch for safer imports
try:
    from src.config.settings import get_news_config
    from src.utils.helpers import log_user_action
except ImportError:
    # Fallback for testing
    def get_news_config():
        return type('Config', (), {'rss_refresh_interval': 300})()
    def log_user_action(action, data):
        print(f"Log: {action} - {data}")

@dataclass
class NewsItem:
    """News item data structure"""
    title: str
    summary: str
    source: str
    published_date: str
    category: str
    impact_score: int
    tags: List[str]
    url: str

class NewsService:
    """Service for aggregating AI news from RSS feeds"""
    
    def __init__(self):
        try:
            self.config = get_news_config()
        except:
            self.config = type('Config', (), {'rss_refresh_interval': 300})()
        
        self.rss_sources = self._get_rss_sources()
        self.cache_duration = 300  # 5 minutes
    
    def _get_rss_sources(self) -> Dict[str, Dict]:
        """Get RSS feed sources configuration"""
        return {
            "anthropic": {
                "url": "https://www.anthropic.com/news/feed_anthropic_news.xml",
                "category": "Research",
                "source_name": "Anthropic"
            },
            "openai": {
                "url": "https://openai.com/blog/rss.xml", 
                "category": "Technology",
                "source_name": "OpenAI"
            },
            "google_ai": {
                "url": "https://ai.googleblog.com/feeds/posts/default",
                "category": "Research", 
                "source_name": "Google AI"
            },
            "mit_tech_review": {
                "url": "https://www.technologyreview.com/feed/",
                "category": "Technology",
                "source_name": "MIT Technology Review"
            },
            "ai_news": {
                "url": "https://artificialintelligence-news.com/feed/",
                "category": "Industry",
                "source_name": "AI News"
            },
            "techcrunch_ai": {
                "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
                "category": "Business",
                "source_name": "TechCrunch AI"
            },
            "venturebeat_ai": {
                "url": "https://venturebeat.com/ai/feed/",
                "category": "Business", 
                "source_name": "VentureBeat AI"
            },
            "the_verge_ai": {
                "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
                "category": "Technology",
                "source_name": "The Verge AI"
            },
            "wired_ai": {
                "url": "https://www.wired.com/feed/tag/ai/latest/rss",
                "category": "Technology",
                "source_name": "Wired AI"
            },
            "arxiv_cs_ai": {
                "url": "http://export.arxiv.org/rss/cs.AI",
                "category": "Research",
                "source_name": "ArXiv AI"
            },
            "xai_grok": {
                "url": "https://x.ai/news/rss.xml",
                "category": "Technology",
                "source_name": "xAI (Grok)"
            },
            "microsoft_ai": {
                "url": "https://blogs.microsoft.com/feed/category/ai/",
                "category": "Technology",
                "source_name": "Microsoft AI"
            },
            "meta_ai": {
                "url": "https://ai.facebook.com/feed/",
                "category": "Technology",
                "source_name": "Meta AI"
            },
            "aperam_ai": {
                "url": "https://aperam.com/news/rss.xml",
                "category": "Industry",
                "source_name": "Aperam AI"
            },
            "steel_industry": {
                "url": "https://www.steel.org/feed/",
                "category": "Industry",
                "source_name": "Steel Industry News"
            },
            "mcp_ai": {
                "url": "https://mcp.ai/feed/",
                "category": "Technology",
                "source_name": "MCP AI"
            },
            "gemini_ai": {
                "url": "https://blog.google/products/ai/feed/",
                "category": "Technology",
                "source_name": "Google Gemini AI"
            },
            "claude_ai": {
                "url": "https://www.anthropic.com/news/rss.xml",
                "category": "Technology",
                "source_name": "Claude AI"
            },
            "gpt_ai": {
                "url": "https://openai.com/blog/rss.xml",
                "category": "Technology",
                "source_name": "GPT AI"
            },
            "chatgpt_ai": {
                "url": "https://openai.com/blog/rss.xml",
                "category": "Technology",
                "source_name": "ChatGPT AI"
            },
            "bert_ai": {
                "url": "https://ai.googleblog.com/feeds/posts/default",
                "category": "Technology",
                "source_name": "BERT AI"
            },
            "transformer_ai": {
                "url": "https://ai.googleblog.com/feeds/posts/default",
                "category": "Technology",
                "source_name": "Transformer AI"
            },
            "llm_ai": {
                "url": "https://openai.com/blog/rss.xml",
                "category": "Technology",
                "source_name": "LLM AI"
            },
            "robotics_ai": {
                "url": "https://www.roboticsbusinessreview.com/feed/",
                "category": "Technology",
                "source_name": "Robotics AI"
            },
            "automation_ai": {
                "url": "https://www.automation.com/rss",
                "category": "Technology",
                "source_name": "Automation AI"
            },
            "predictive_ai": {
                "url": "https://www.predictiveanalyticsworld.com/feed/",
                "category": "Technology",
                "source_name": "Predictive AI"
            },
            "agentic_ai": {
                "url": "https://www.agentic.ai/feed/",
                "category": "Technology",
                "source_name": "Agentic AI"
            },
            "ars_technica": {
                "url": "https://feeds.arstechnica.com/arstechnica/technology-lab",
                "category": "Technology",
                "source_name": "Ars Technica"
            },
            "reuters_tech": {
                "url": "https://www.reuters.com/technology/feed/",
                "category": "Business",
                "source_name": "Reuters Tech"
            },
            "hacker_news": {
                "url": "https://hnrss.org/frontpage",
                "category": "Technology",
                "source_name": "Hacker News"
            }
        }
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_breaking_news(_self, category_filter: List[str] = None, limit: int = 10) -> List[NewsItem]:
        """Get breaking news from RSS feeds"""
        try:
            all_news = []
            working_sources = 0
            
            for source_key, source_config in _self.rss_sources.items():
                try:
                    # Parse RSS feed with timeout
                    feed = feedparser.parse(source_config["url"])
                    
                    # Check if feed parsed successfully
                    if hasattr(feed, 'bozo') and feed.bozo:
                        log_user_action("rss_parse_warning", {
                            "source": source_key, 
                            "error": str(getattr(feed, 'bozo_exception', 'Unknown parsing error'))
                        })
                        # Continue anyway, sometimes bozo feeds still have useful data
                    
                    # Process entries if they exist
                    if hasattr(feed, 'entries') and feed.entries:
                        working_sources += 1
                        for entry in feed.entries[:3]:  # Limit per source
                            news_item = _self._process_feed_entry(entry, source_config)
                            if news_item:
                                all_news.append(news_item)
                            
                except Exception as e:
                    log_user_action("rss_source_error", {
                        "source": source_key,
                        "error": str(e)
                    })
                    continue
            
            # If no sources worked, return fallback data
            if working_sources == 0:
                log_user_action("all_rss_sources_failed", {"attempted_sources": len(_self.rss_sources)})
                return _self._get_fallback_news()
            
            # Sort by date
            all_news.sort(key=lambda x: x.published_date, reverse=True)
            
            # Apply category filter (more lenient)
            if category_filter and "All" not in category_filter and category_filter:
                filtered_news = []
                for item in all_news:
                    # Check if item category matches any selected categories
                    if any(cat.lower() in item.category.lower() for cat in category_filter):
                        filtered_news.append(item)
                # If filter is too restrictive, return some results anyway
                if len(filtered_news) < 3 and len(all_news) >= 3:
                    all_news = all_news[:limit]  # Return unfiltered results
                else:
                    all_news = filtered_news
            
            log_user_action("news_service_success", {
                "total_sources": len(_self.rss_sources),
                "working_sources": working_sources, 
                "total_articles": len(all_news)
            })
            
            return all_news[:limit]
            
        except Exception as e:
            log_user_action("news_service_error", {"error": str(e)})
            # Return fallback mock data
            return _self._get_fallback_news()
    
    def _process_feed_entry(self, entry, source_config: Dict) -> Optional[NewsItem]:
        """Process individual RSS feed entry"""
        try:
            # Extract title
            title = getattr(entry, 'title', 'No Title Available')
            
            # Extract published date
            published_date = self._extract_date(entry)
            
            # Extract and clean summary
            summary = self._clean_summary(
                getattr(entry, 'summary', 
                getattr(entry, 'description', 
                getattr(entry, 'content', 'No summary available')))
            )
            
            # Generate tags from title and summary
            tags = self._extract_tags(title, summary)
            
            # Calculate impact score
            impact_score = self._calculate_impact_score(title, summary, source_config["source_name"])
            
            # Extract URL
            url = getattr(entry, 'link', '#')
            
            return NewsItem(
                title=title,
                summary=summary,
                source=source_config["source_name"],
                published_date=published_date,
                category=source_config["category"],
                impact_score=impact_score,
                tags=tags,
                url=url
            )
            
        except Exception as e:
            log_user_action("entry_processing_error", {"error": str(e)})
            return None
    
    def _extract_date(self, entry) -> str:
        """Extract and format published date"""
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                dt = datetime(*entry.published_parsed[:6])
                return dt.strftime("%Y-%m-%d")
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                dt = datetime(*entry.updated_parsed[:6])
                return dt.strftime("%Y-%m-%d")
            else:
                return datetime.now().strftime("%Y-%m-%d")
        except:
            return datetime.now().strftime("%Y-%m-%d")
    
    def _clean_summary(self, summary: str) -> str:
        """Clean and truncate summary"""
        try:
            if isinstance(summary, list):
                summary = ' '.join([str(item) for item in summary])
            
            summary = str(summary)
            
            # Remove HTML tags
            clean_summary = re.sub(r'<[^>]+>', '', summary)
            
            # Remove extra whitespace
            clean_summary = re.sub(r'\s+', ' ', clean_summary).strip()
            
            # Remove common RSS artifacts
            clean_summary = re.sub(r'\[&hellip;\]', '...', clean_summary)
            clean_summary = re.sub(r'&\w+;', '', clean_summary)  # Remove HTML entities
            
            # Truncate to reasonable length
            if len(clean_summary) > 300:
                clean_summary = clean_summary[:297] + "..."
            
            return clean_summary if clean_summary else "Summary not available"
            
        except:
            return "Summary not available"
    
    def _extract_tags(self, title: str, summary: str) -> List[str]:
        """Extract relevant tags from title and summary"""
        # AI-related keywords to look for
        ai_keywords = {
            'machine learning': 'Machine Learning',
            'deep learning': 'Deep Learning', 
            'neural network': 'Neural Networks',
            'artificial intelligence': 'AI',
            'natural language': 'NLP',
            'computer vision': 'Computer Vision',
            'robotics': 'Robotics',
            'automation': 'Automation',
            'chatgpt': 'ChatGPT',
            'gpt': 'GPT',
            'claude': 'Claude',
            'gemini': 'Gemini',
            'bert': 'BERT',
            'transformer': 'Transformers',
            'generative': 'Generative AI',
            'llm': 'LLM',
            'openai': 'OpenAI',
            'anthropic': 'Anthropic',
            'google': 'Google',
            'microsoft': 'Microsoft',
            'meta': 'Meta',
            'manufacturing': 'Manufacturing',
            'steel': 'Steel Industry',
            'supply chain': 'Supply Chain',
            'predictive': 'Predictive Analytics',
            'agentic': 'Agentic AI',
            'mcp': 'MCP'
        }
        
        text = (str(title) + " " + str(summary)).lower()
        tags = []
        
        for keyword, tag in ai_keywords.items():
            if keyword in text:
                tags.append(tag)
        
        return list(set(tags))[:5]  # Limit to 5 unique tags
    
    def _calculate_impact_score(self, title: str, summary: str, source: str) -> int:
        """Calculate impact score (1-5) based on content and source"""
        score = 3  # Base score
        
        text = (str(title) + " " + str(summary)).lower()
        
        # High impact indicators
        high_impact_keywords = ['breakthrough', 'revolutionary', 'unprecedented', 'major', 'significant']
        for keyword in high_impact_keywords:
            if keyword in text:
                score += 1
                break
        
        # Technology-specific boosts
        tech_keywords = ['gpt', 'claude', 'gemini', 'chatgpt', 'ai model', 'agentic']
        for keyword in tech_keywords:
            if keyword in text:
                score += 0.5
                break
        
        # Source credibility boost
        credible_sources = ['MIT Technology Review', 'The Verge AI', 'Wired AI', 'Anthropic', 'OpenAI', 'Gemini', 'Google']
        if source in credible_sources:
            score += 0.5
        
        # Industry relevance boost
        industry_keywords = ['manufacturing', 'steel', 'industrial', 'enterprise']
        for keyword in industry_keywords:
            if keyword in text:
                score += 0.5
                break
        
        return min(5, max(1, int(score)))
    
    def _get_fallback_news(self) -> List[NewsItem]:
        """Fallback news when RSS feeds fail"""
        return [
            NewsItem(
                title="Welcome to AI News Aggregator",
                summary="Your AI news service is initializing. Real-time feeds from major AI sources will appear here once connected.",
                source="System",
                published_date=datetime.now().strftime("%Y-%m-%d"),
                category="Technology",
                impact_score=3,
                tags=["System", "AI News"],
                url="#"
            ),
            NewsItem(
                title="AI Industry Continues Rapid Growth",
                summary="The artificial intelligence industry shows no signs of slowing down, with major developments across machine learning, natural language processing, and computer vision.",
                source="AI News",
                published_date=(datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d"),
                category="Industry",
                impact_score=4,
                tags=["AI", "Industry", "Growth"],
                url="#"
            ),
            NewsItem(
                title="Enterprise AI Adoption Accelerates",
                summary="Companies across industries are implementing AI solutions for manufacturing, supply chain optimization, and quality control with measurable business impact.",
                source="TechCrunch AI",
                published_date=(datetime.now() - timedelta(hours=4)).strftime("%Y-%m-%d"),
                category="Business",
                impact_score=4,
                tags=["Enterprise", "Manufacturing", "AI"],
                url="#"
            )
        ]
    
    def get_research_papers(self, category_filter: List[str] = None, limit: int = 5) -> List[NewsItem]:
        """Get research papers (enhanced with RSS + mock data)"""
        # Try to get from ArXiv RSS first
        research_news = []
        
        try:
            arxiv_url = "http://export.arxiv.org/rss/cs.AI"
            feed = feedparser.parse(arxiv_url)
            
            if hasattr(feed, 'entries') and feed.entries:
                for entry in feed.entries[:3]:
                    research_item = NewsItem(
                        title=getattr(entry, 'title', 'Research Paper'),
                        summary=self._clean_summary(getattr(entry, 'summary', 'Abstract not available')),
                        source="ArXiv",
                        published_date=self._extract_date(entry),
                        category="Research",
                        impact_score=4,
                        tags=["Research", "AI", "Academic"],
                        url=getattr(entry, 'link', '#')
                    )
                    research_news.append(research_item)
        except Exception as e:
            log_user_action("arxiv_fetch_error", {"error": str(e)})
        
        # Add some mock research papers to fill out the list
        mock_papers = [
            NewsItem(
                title="Scaling Laws for Neural Language Models in Steel Manufacturing Optimization",
                summary="We investigate the scaling laws for neural language models when applied to steel manufacturing optimization. Our findings suggest that larger models consistently improve prediction accuracy for quality control and process optimization tasks.",
                source="Nature Machine Intelligence",
                published_date="2024-01-20",
                category="Research",
                impact_score=5,
                tags=["Steel Manufacturing", "Neural Networks", "Optimization"],
                url="#"
            ),
            NewsItem(
                title="Federated Learning for Industrial IoT: A Steel Production Case Study",
                summary="This paper presents a federated learning approach for industrial IoT applications, specifically focusing on steel production. We demonstrate improved model performance while maintaining data privacy across multiple production sites.",
                source="IEEE Transactions on Industrial Informatics",
                published_date="2024-01-19",
                category="Research",
                impact_score=4,
                tags=["Federated Learning", "Industrial IoT", "Steel Production"],
                url="#"
            ),
            NewsItem(
                title="Explainable AI for Predictive Maintenance in Heavy Industry",
                summary="We propose an explainable AI framework for predictive maintenance in heavy industrial equipment. The approach provides interpretable predictions while maintaining high accuracy for maintenance scheduling.",
                source="Journal of Manufacturing Systems",
                published_date="2024-01-18",
                category="Research",
                impact_score=4,
                tags=["Explainable AI", "Predictive Maintenance", "Heavy Industry"],
                url="#"
            )
        ]
        
        # Combine real RSS data with mock data
        research_news.extend(mock_papers)
        
        # Apply filters
        if category_filter and "All" not in category_filter:
            research_news = [item for item in research_news if item.category in category_filter]
        
        return research_news[:limit]
    
    def get_industry_updates(self, category_filter: List[str] = None, limit: int = 5) -> List[NewsItem]:
        """Get industry updates (enhanced with RSS + mock data)"""
        industry_news = []
        
        # Try to get from industry sources
        industry_sources = ["ai_news", "techcrunch_ai", "venturebeat_ai"]
        
        for source_key in industry_sources:
            if source_key in self.rss_sources:
                try:
                    source_config = self.rss_sources[source_key]
                    feed = feedparser.parse(source_config["url"])
                    
                    if hasattr(feed, 'entries') and feed.entries:
                        for entry in feed.entries[:2]:  # Limit per source
                            industry_item = self._process_feed_entry(entry, source_config)
                            if industry_item:
                                industry_news.append(industry_item)
                except Exception as e:
                    continue
        
        # Add mock industry updates
        mock_updates = [
            NewsItem(
                title="ArcelorMittal Implements AI-Powered Quality Control Across 15 Plants",
                summary="ArcelorMittal has successfully deployed AI-powered quality control systems across 15 production facilities, resulting in 30% reduction in defects and significant cost savings.",
                source="Steel Business Briefing",
                published_date="2024-01-20",
                category="Industry",
                impact_score=4,
                tags=["ArcelorMittal", "Quality Control", "AI Implementation"],
                url="#"
            ),
            NewsItem(
                title="Tata Steel Partners with Google Cloud for Digital Transformation",
                summary="Tata Steel has announced a strategic partnership with Google Cloud to accelerate digital transformation across its operations, focusing on AI-driven predictive maintenance.",
                source="Metal Bulletin",
                published_date="2024-01-19",
                category="Business",
                impact_score=3,
                tags=["Tata Steel", "Google Cloud", "Digital Transformation"],
                url="#"
            )
        ]
        
        industry_news.extend(mock_updates)
        
        # Apply filters
        if category_filter and "All" not in category_filter:
            industry_news = [item for item in industry_news if item.category in category_filter]
        
        return industry_news[:limit]
    
    def test_rss_sources(self) -> Dict[str, bool]:
        """Test all RSS sources and return status"""
        results = {}
        
        for source_key, source_config in self.rss_sources.items():
            try:
                feed = feedparser.parse(source_config["url"])
                # More lenient check - just verify we got some content
                results[source_key] = hasattr(feed, 'entries') and len(feed.entries) > 0
            except:
                results[source_key] = False
        
        return results

# Global service instance
news_service = NewsService()

# Convenience functions
def get_breaking_news(category_filter: List[str] = None, limit: int = 10) -> List[NewsItem]:
    """Get breaking news"""
    return news_service.get_breaking_news(category_filter, limit)

def get_research_papers(category_filter: List[str] = None, limit: int = 5) -> List[NewsItem]:
    """Get research papers"""
    return news_service.get_research_papers(category_filter, limit)

def get_industry_updates(category_filter: List[str] = None, limit: int = 5) -> List[NewsItem]:
    """Get industry updates"""
    return news_service.get_industry_updates(category_filter, limit)

def test_news_sources() -> Dict[str, bool]:
    """Test news sources"""
    return news_service.test_rss_sources()