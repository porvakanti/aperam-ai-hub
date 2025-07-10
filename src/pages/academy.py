"""
AI Academy Page
Learning paths and curated AI education content
"""

import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime
from src.config.settings import get_app_config
from src.utils.helpers import log_user_action

def render_academy_page():
    """Render the AI Academy page"""
    # Back to home button
    if st.button("← Back to Home", key="back_to_home_academy"):
        st.session_state.page = "🏠 Home"
        st.rerun()
    
    st.title("🎓 AI Academy")
    
    # Welcome section
    st.markdown("""
    **Welcome to the Aperam AI Academy!**
    
    Your journey to AI mastery starts here. Whether you're a beginner or an expert, 
    we have curated learning paths to help you build AI skills relevant to your role and industry.
    """)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Learning Paths", 
        "📚 Course Catalog", 
        "🏆 My Progress", 
        "💡 Interactive Labs"
    ])
    
    with tab1:
        render_learning_paths()
    
    with tab2:
        render_course_catalog()
    
    with tab3:
        render_progress_tracking()
    
    with tab4:
        render_interactive_labs()

def render_learning_paths():
    """Render learning paths section"""
    st.markdown("### 🎯 Personalized Learning Paths")
    
    # Role-based recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Select Your Role")
        user_role = st.selectbox("Choose your role:", [
            "Select Role",
            "Executive/Manager",
            "Engineer/Technical",
            "Operations/Production",
            "Quality Control",
            "Data Analyst",
            "Business Analyst",
            "New to AI"
        ])
        
        experience_level = st.selectbox("Experience Level:", [
            "Beginner",
            "Intermediate",
            "Advanced",
            "Expert"
        ])
        
        if st.button("🚀 Get Personalized Recommendations"):
            show_personalized_path(user_role, experience_level)
    
    with col2:
        st.markdown("#### 🎯 Quick Start Options")
        
        quick_paths = [
            {
                "title": "AI Basics for Everyone",
                "duration": "2-3 hours",
                "description": "Perfect introduction to AI concepts",
                "icon": "🌟"
            },
            {
                "title": "AI in Manufacturing",
                "duration": "4-6 hours", 
                "description": "Industry-specific AI applications",
                "icon": "🏭"
            },
            {
                "title": "Data Science Fundamentals",
                "duration": "8-10 hours",
                "description": "Build your data analysis skills",
                "icon": "📊"
            },
            {
                "title": "AI Ethics & Governance",
                "duration": "3-4 hours",
                "description": "Responsible AI implementation",
                "icon": "🛡️"
            }
        ]
        
        for path in quick_paths:
            with st.expander(f"{path['icon']} {path['title']} ({path['duration']})"):
                st.markdown(path['description'])
                if st.button(f"Start Path", key=f"start_{path['title'].replace(' ', '_')}"):
                    start_learning_path(path)
    
    # Featured learning paths
    st.markdown("### 🌟 Featured Learning Paths")
    
    featured_paths = get_featured_learning_paths()
    
    for path in featured_paths:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"### {path['icon']} {path['title']}")
                st.markdown(f"**Target Audience:** {path['target_audience']}")
                st.markdown(f"**Description:** {path['description']}")
                st.markdown(f"**Skills You'll Learn:** {', '.join(path['skills'])}")
            
            with col2:
                st.markdown(f"**Duration:** {path['duration']}")
                st.markdown(f"**Difficulty:** {path['difficulty']}")
                st.markdown(f"**Modules:** {path['modules']}")
                st.markdown(f"**Certificate:** {'Yes' if path['certificate'] else 'No'}")
            
            with col3:
                st.markdown(f"**Rating:** {path['rating']}/5")
                st.markdown(f"**Enrolled:** {path['enrolled']}")
                
                if st.button("📚 Enroll Now", key=f"enroll_{path['title'].replace(' ', '_')}"):
                    enroll_in_path(path)
                
                if st.button("👁️ Preview", key=f"preview_{path['title'].replace(' ', '_')}"):
                    show_path_preview(path)
            
            st.markdown("---")

def render_course_catalog():
    """Render course catalog section"""
    st.markdown("### 📚 Course Catalog")
    
    # Search and filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search courses", placeholder="e.g., machine learning, Python")
    
    with col2:
        category_filter = st.selectbox("Category", [
            "All Categories",
            "AI Fundamentals",
            "Machine Learning",
            "Deep Learning",
            "Data Science",
            "AI Ethics",
            "Industry Applications",
            "Programming",
            "Business Applications"
        ])
    
    with col3:
        difficulty_filter = st.selectbox("Difficulty", [
            "All Levels",
            "Beginner",
            "Intermediate",
            "Advanced",
            "Expert"
        ])
    
    # Course grid
    courses = get_course_catalog(search_query, category_filter, difficulty_filter)
    
    # Display courses in grid format
    cols = st.columns(3)
    for i, course in enumerate(courses):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"### {course['title']}")
                st.markdown(f"**Instructor:** {course['instructor']}")
                st.markdown(f"**Duration:** {course['duration']}")
                st.markdown(f"**Difficulty:** {course['difficulty']}")
                st.markdown(f"**Rating:** {course['rating']}/5 ({course['reviews']} reviews)")
                st.markdown(f"**Price:** {course['price']}")
                
                if st.button("📖 Learn More", key=f"learn_{course['title'].replace(' ', '_')}"):
                    show_course_details(course)
                
                if st.button("🎓 Enroll", key=f"enroll_course_{course['title'].replace(' ', '_')}"):
                    enroll_in_course(course)
            
            st.markdown("---")

def render_progress_tracking():
    """Render progress tracking section"""
    st.markdown("### 🏆 My Learning Progress")
    
    # Overall progress metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Courses Completed", "12", "+2")
    
    with col2:
        st.metric("Hours Learned", "48", "+6")
    
    with col3:
        st.metric("Certificates Earned", "5", "+1")
    
    with col4:
        st.metric("Skill Points", "2,450", "+150")
    
    # Progress visualization
    st.markdown("#### 📊 Learning Progress")
    
    # Mock progress data
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Learning Hours by Month", "Skill Development"),
        specs=[[{"secondary_y": False}, {"type": "polar"}]]
    )
    
    # Learning hours trend
    months = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    hours = [5, 8, 12, 15, 18]
    
    fig.add_trace(
        go.Scatter(x=months, y=hours, mode='lines+markers', name='Learning Hours'),
        row=1, col=1
    )
    
    # Skill radar chart
    skills = ['AI Fundamentals', 'Machine Learning', 'Data Science', 'Programming', 'Ethics', 'Business']
    skill_levels = [85, 70, 75, 90, 80, 65]
    
    fig.add_trace(
        go.Scatterpolar(
            r=skill_levels,
            theta=skills,
            fill='toself',
            name='Skill Level'
        ),
        row=1, col=2
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Current enrollments
    st.markdown("#### 📚 Current Enrollments")
    
    current_courses = get_current_enrollments()
    
    for course in current_courses:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{course['title']}**")
                st.markdown(f"Instructor: {course['instructor']}")
                st.progress(course['progress'] / 100)
                st.markdown(f"Progress: {course['progress']}%")
            
            with col2:
                st.markdown(f"**Due:** {course['due_date']}")
                st.markdown(f"**Time Left:** {course['time_left']}")
            
            with col3:
                if st.button("Continue", key=f"continue_{course['title'].replace(' ', '_')}"):
                    continue_course(course)
                
                if st.button("Resources", key=f"resources_{course['title'].replace(' ', '_')}"):
                    show_course_resources(course)
        
        st.markdown("---")
    
    # Achievements and badges
    st.markdown("#### 🏅 Achievements & Badges")
    
    achievements = get_user_achievements()
    
    cols = st.columns(4)
    for i, achievement in enumerate(achievements):
        with cols[i % 4]:
            st.markdown(f"### {achievement['icon']}")
            st.markdown(f"**{achievement['title']}**")
            st.markdown(f"*{achievement['description']}*")
            if achievement['earned']:
                st.success("✅ Earned")
            else:
                st.info(f"📊 {achievement['progress']}%")

def render_interactive_labs():
    """Render interactive labs section"""
    st.markdown("### 💡 Interactive AI Labs")
    
    st.markdown("""
    **Hands-on Learning Experience**
    
    Practice your AI skills with real-world scenarios and interactive exercises.
    These labs provide safe environments to experiment and learn.
    """)
    
    # Lab categories
    lab_categories = [
        {
            "title": "🧠 Machine Learning Playground",
            "description": "Interactive ML experiments and visualizations",
            "labs": [
                "Linear Regression Visualization",
                "Decision Tree Explorer",
                "Neural Network Trainer",
                "Clustering Algorithm Comparison"
            ]
        },
        {
            "title": "📊 Data Analysis Workshop",
            "description": "Practice data analysis with real datasets",
            "labs": [
                "Steel Production Data Analysis",
                "Quality Control Statistics",
                "Supply Chain Optimization",
                "Predictive Maintenance Models"
            ]
        },
        {
            "title": "🤖 AI Ethics Simulator",
            "description": "Navigate ethical AI decision-making scenarios",
            "labs": [
                "Bias Detection Challenge",
                "Fairness in Hiring AI",
                "Privacy Protection Scenarios",
                "Transparency in AI Decisions"
            ]
        },
        {
            "title": "🏭 Industry Applications",
            "description": "Steel and manufacturing-specific AI use cases",
            "labs": [
                "Quality Prediction Model",
                "Process Optimization Simulator",
                "Energy Efficiency Calculator",
                "Maintenance Schedule Optimizer"
            ]
        }
    ]
    
    for category in lab_categories:
        with st.expander(f"{category['title']} - {category['description']}"):
            st.markdown("**Available Labs:**")
            
            for lab in category['labs']:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"• {lab}")
                
                with col2:
                    if st.button("🚀 Launch", key=f"launch_{lab.replace(' ', '_')}"):
                        launch_interactive_lab(lab)
    
    # Featured lab
    st.markdown("### 🌟 Featured Lab: Steel Quality Prediction")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Learn to build AI models for steel quality prediction**
        
        In this interactive lab, you'll:
        - Explore real steel production data
        - Build and train a quality prediction model
        - Evaluate model performance
        - Deploy your model for testing
        
        **Prerequisites:** Basic understanding of machine learning
        **Estimated Time:** 45 minutes
        **Difficulty:** Intermediate
        """)
    
    with col2:
        st.markdown("**Lab Features:**")
        st.markdown("• Interactive code editor")
        st.markdown("• Real-time results")
        st.markdown("• Step-by-step guidance")
        st.markdown("• Performance metrics")
        st.markdown("• Save and share results")
        
        if st.button("🎯 Start Featured Lab", use_container_width=True):
            launch_featured_lab()

def get_featured_learning_paths():
    """Get featured learning paths"""
    return [
        {
            "title": "AI for Manufacturing Leaders",
            "icon": "👑",
            "target_audience": "Executives, Managers, Department Heads",
            "description": "Strategic AI implementation for manufacturing excellence",
            "duration": "6-8 hours",
            "difficulty": "Beginner",
            "modules": 8,
            "certificate": True,
            "rating": 4.8,
            "enrolled": "245 learners",
            "skills": ["AI Strategy", "ROI Analysis", "Change Management", "Digital Transformation"]
        },
        {
            "title": "Machine Learning for Engineers",
            "icon": "⚙️",
            "target_audience": "Engineers, Technical Staff",
            "description": "Practical ML implementation for engineering applications",
            "duration": "12-15 hours",
            "difficulty": "Intermediate",
            "modules": 12,
            "certificate": True,
            "rating": 4.7,
            "enrolled": "189 learners",
            "skills": ["Python Programming", "ML Algorithms", "Model Deployment", "Data Engineering"]
        },
        {
            "title": "AI in Quality Control",
            "icon": "🔍",
            "target_audience": "Quality Control, Operations",
            "description": "AI-powered quality assurance and defect detection",
            "duration": "8-10 hours",
            "difficulty": "Intermediate",
            "modules": 10,
            "certificate": True,
            "rating": 4.9,
            "enrolled": "156 learners",
            "skills": ["Computer Vision", "Statistical Analysis", "Process Optimization", "Quality Metrics"]
        },
        {
            "title": "Data Science Fundamentals",
            "icon": "📊",
            "target_audience": "Analysts, Data Professionals",
            "description": "Complete data science toolkit for business insights",
            "duration": "15-20 hours",
            "difficulty": "Beginner to Intermediate",
            "modules": 15,
            "certificate": True,
            "rating": 4.6,
            "enrolled": "312 learners",
            "skills": ["Statistics", "Data Visualization", "Predictive Analytics", "Business Intelligence"]
        }
    ]

def get_course_catalog(search_query: str, category_filter: str, difficulty_filter: str):
    """Get course catalog with filters"""
    courses = [
        {
            "title": "Introduction to Artificial Intelligence",
            "instructor": "Dr. Sarah Johnson",
            "duration": "4 hours",
            "difficulty": "Beginner",
            "rating": 4.8,
            "reviews": 234,
            "price": "Free",
            "category": "AI Fundamentals"
        },
        {
            "title": "Machine Learning with Python",
            "instructor": "Prof. Michael Chen",
            "duration": "12 hours",
            "difficulty": "Intermediate",
            "rating": 4.7,
            "reviews": 189,
            "price": "Free",
            "category": "Machine Learning"
        },
        {
            "title": "Deep Learning for Computer Vision",
            "instructor": "Dr. Emily Rodriguez",
            "duration": "16 hours",
            "difficulty": "Advanced",
            "rating": 4.9,
            "reviews": 156,
            "price": "Free",
            "category": "Deep Learning"
        },
        {
            "title": "AI Ethics and Responsible AI",
            "instructor": "Dr. David Kim",
            "duration": "6 hours",
            "difficulty": "Beginner",
            "rating": 4.6,
            "reviews": 298,
            "price": "Free",
            "category": "AI Ethics"
        },
        {
            "title": "Data Science for Business",
            "instructor": "Prof. Lisa Wang",
            "duration": "10 hours",
            "difficulty": "Intermediate",
            "rating": 4.5,
            "reviews": 145,
            "price": "Free",
            "category": "Data Science"
        },
        {
            "title": "AI in Manufacturing",
            "instructor": "Dr. Robert Taylor",
            "duration": "8 hours",
            "difficulty": "Intermediate",
            "rating": 4.8,
            "reviews": 87,
            "price": "Free",
            "category": "Industry Applications"
        }
    ]
    
    # Apply filters (simplified for demo)
    filtered_courses = courses
    
    if search_query:
        filtered_courses = [c for c in filtered_courses if search_query.lower() in c['title'].lower()]
    
    if category_filter != "All Categories":
        filtered_courses = [c for c in filtered_courses if c['category'] == category_filter]
    
    if difficulty_filter != "All Levels":
        filtered_courses = [c for c in filtered_courses if c['difficulty'] == difficulty_filter]
    
    return filtered_courses

def get_current_enrollments():
    """Get user's current course enrollments"""
    return [
        {
            "title": "Machine Learning with Python",
            "instructor": "Prof. Michael Chen",
            "progress": 75,
            "due_date": "2024-02-15",
            "time_left": "3 days"
        },
        {
            "title": "AI Ethics and Responsible AI",
            "instructor": "Dr. David Kim",
            "progress": 45,
            "due_date": "2024-02-20",
            "time_left": "8 days"
        },
        {
            "title": "AI in Manufacturing",
            "instructor": "Dr. Robert Taylor",
            "progress": 20,
            "due_date": "2024-02-25",
            "time_left": "13 days"
        }
    ]

def get_user_achievements():
    """Get user achievements and badges"""
    return [
        {
            "title": "AI Fundamentals",
            "icon": "🎯",
            "description": "Completed basic AI concepts",
            "earned": True,
            "progress": 100
        },
        {
            "title": "Code Master",
            "icon": "💻",
            "description": "Completed 10 programming exercises",
            "earned": True,
            "progress": 100
        },
        {
            "title": "Data Detective",
            "icon": "🔍",
            "description": "Analyzed 5 datasets successfully",
            "earned": False,
            "progress": 60
        },
        {
            "title": "Ethics Champion",
            "icon": "🛡️",
            "description": "Completed AI ethics certification",
            "earned": False,
            "progress": 80
        }
    ]

def show_personalized_path(role: str, experience: str):
    """Show personalized learning path recommendations"""
    st.success(f"🎯 Personalized path generated for {role} ({experience} level)")
    
    # Mock personalized recommendations
    recommendations = {
        "Executive/Manager": [
            "AI Strategy and Leadership",
            "AI ROI and Business Value",
            "Digital Transformation",
            "AI Ethics and Governance"
        ],
        "Engineer/Technical": [
            "Machine Learning Fundamentals",
            "Python Programming",
            "Model Deployment",
            "Technical AI Implementation"
        ],
        "Operations/Production": [
            "AI in Manufacturing",
            "Process Optimization",
            "Predictive Maintenance",
            "Quality Control AI"
        ]
    }
    
    path = recommendations.get(role, ["AI Fundamentals", "Industry Applications"])
    
    st.markdown("**Recommended Learning Path:**")
    for i, course in enumerate(path, 1):
        st.markdown(f"{i}. {course}")
    
    if st.button("📚 Start This Path"):
        st.success("Learning path started! Check your progress in the 'My Progress' tab.")

def start_learning_path(path: Dict):
    """Start a learning path"""
    st.success(f"🚀 Started learning path: {path['title']}")
    log_user_action("learning_path_started", {"path": path['title']})

def enroll_in_path(path: Dict):
    """Enroll in a learning path"""
    st.success(f"✅ Enrolled in: {path['title']}")
    log_user_action("learning_path_enrolled", {"path": path['title']})

def show_path_preview(path: Dict):
    """Show learning path preview"""
    st.subheader(f"📚 Preview: {path['title']}")
    st.markdown(f"**Description:** {path['description']}")
    st.markdown(f"**Duration:** {path['duration']}")
    st.markdown(f"**Modules:** {path['modules']}")
    st.markdown("**Module Overview:**")
    st.markdown("1. Introduction and Fundamentals")
    st.markdown("2. Core Concepts and Theory")
    st.markdown("3. Practical Applications")
    st.markdown("4. Hands-on Projects")
    st.markdown("5. Assessment and Certification")

def show_course_details(course: Dict):
    """Show detailed course information"""
    st.subheader(f"📖 Course Details: {course['title']}")
    st.markdown(f"**Instructor:** {course['instructor']}")
    st.markdown(f"**Duration:** {course['duration']}")
    st.markdown(f"**Difficulty:** {course['difficulty']}")
    st.markdown(f"**Rating:** {course['rating']}/5 based on {course['reviews']} reviews")
    st.markdown("**Course Description:**")
    st.markdown("This comprehensive course covers all essential topics with hands-on exercises and real-world examples.")

def enroll_in_course(course: Dict):
    """Enroll in a course"""
    st.success(f"🎓 Enrolled in: {course['title']}")
    log_user_action("course_enrolled", {"course": course['title']})

def continue_course(course: Dict):
    """Continue a course"""
    st.info(f"📚 Continuing: {course['title']}")
    log_user_action("course_continued", {"course": course['title']})

def show_course_resources(course: Dict):
    """Show course resources"""
    st.subheader(f"📚 Resources: {course['title']}")
    st.markdown("**Available Resources:**")
    st.markdown("• Lecture notes and slides")
    st.markdown("• Video recordings")
    st.markdown("• Practice exercises")
    st.markdown("• Additional reading materials")
    st.markdown("• Discussion forums")

def launch_interactive_lab(lab_name: str):
    """Launch an interactive lab"""
    st.success(f"🚀 Launching lab: {lab_name}")
    st.info("Interactive lab environment would open in a new window or embedded iframe.")
    log_user_action("lab_launched", {"lab": lab_name})

def launch_featured_lab():
    """Launch the featured lab"""
    st.success("🎯 Launching Featured Lab: Steel Quality Prediction")
    st.info("Interactive lab environment loading...")
    
    # Mock lab interface
    st.markdown("### 🧪 Lab Environment")
    st.code("""
# Steel Quality Prediction Lab
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load sample steel production data
data = pd.read_csv('steel_production_data.csv')
print(f"Data shape: {data.shape}")
print(data.head())

# Your task: Build a quality prediction model
# TODO: Complete the model training code
    """, language="python")
    
    if st.button("▶️ Run Code"):
        st.success("Code executed successfully!")
        st.markdown("**Output:**")
        st.markdown("Data shape: (1000, 15)")
        st.markdown("Model accuracy: 0.87")
    
    log_user_action("featured_lab_launched", {"lab": "Steel Quality Prediction"})