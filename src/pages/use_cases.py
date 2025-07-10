"""
Use Case Management Page
Handles AI use case intake, tracking, and management
"""

import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime
from src.config.settings import get_app_config
from src.utils.helpers import log_user_action
from src.services.sheets_service import submit_use_case_to_sheets, test_sheets_connection

def render_use_cases_page():
    """Render the use cases page"""
    # Back to home button
    if st.button("← Back to Home", key="back_to_home_use_cases"):
        st.session_state.page = "🏠 Home"
        st.rerun()
    
    st.title("💡 AI Use Case Intake")
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["📝 Submit New Use Case", "💡 Existing Ideas", "📊 My Submissions"])
    
    with tab1:
        render_use_case_form()
    
    with tab2:
        render_existing_ideas()
    
    with tab3:
        render_my_submissions()

def render_use_case_form():
    """Render the use case submission form"""
    st.markdown("### 🚀 Have an AI idea? Let's make it happen!")
    
    st.markdown("""
    **Why submit your AI use case?**
    - Get expert guidance from the AI team
    - Access to enterprise AI tools and resources
    - Priority support for high-impact initiatives
    - Join our innovation community
    """)
    
    # Call-to-action section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📋 Use Case Submission Form")
        
        with st.form("use_case_form"):
            # Basic Information
            st.subheader("Basic Information")
            
            col_form1, col_form2 = st.columns(2)
            with col_form1:
                submitter_name = st.text_input("Your Name *", placeholder="John Doe")
                submitter_email = st.text_input("Email Address *", placeholder="john.doe@aperam.com")
                department = st.selectbox("Department *", [
                    "Select Department",
                    "Research & Development",
                    "Production",
                    "Quality Control",
                    "Supply Chain",
                    "Finance",
                    "Sales & Marketing",
                    "IT",
                    "HR",
                    "Other"
                ])
            
            with col_form2:
                business_unit = st.selectbox("Business Unit *", [
                    "Select Business Unit",
                    "Stainless Steel",
                    "Carbon Steel",
                    "Alloys & Specialties",
                    "Services",
                    "Corporate",
                    "Other"
                ])
                priority = st.selectbox("Priority Level", [
                    "High - Critical for operations",
                    "Medium - Important improvement",
                    "Low - Nice to have"
                ])
                timeline = st.selectbox("Desired Timeline", [
                    "ASAP (1-2 weeks)",
                    "Short-term (1-3 months)",
                    "Medium-term (3-6 months)",
                    "Long-term (6+ months)"
                ])
            
            # Use Case Details
            st.subheader("Use Case Details")
            
            use_case_title = st.text_input("Use Case Title *", placeholder="e.g., Automated Quality Control for Steel Production")
            
            problem_description = st.text_area(
                "Problem Description *",
                placeholder="Describe the current challenge or opportunity...",
                height=100
            )
            
            proposed_solution = st.text_area(
                "Proposed AI Solution *",
                placeholder="How do you envision AI solving this problem?",
                height=100
            )
            
            expected_benefits = st.text_area(
                "Expected Benefits",
                placeholder="What outcomes do you expect? (cost savings, efficiency gains, etc.)",
                height=80
            )
            
            # Technical Information
            st.subheader("Technical Context")
            
            col_tech1, col_tech2 = st.columns(2)
            with col_tech1:
                data_availability = st.selectbox("Data Availability", [
                    "Extensive data available",
                    "Limited data available",
                    "No data available",
                    "Unsure"
                ])
                
                technical_complexity = st.selectbox("Technical Complexity", [
                    "Simple automation",
                    "Moderate AI/ML required",
                    "Complex AI/ML required",
                    "Cutting-edge research needed"
                ])
            
            with col_tech2:
                integration_needs = st.selectbox("Integration Requirements", [
                    "Standalone solution",
                    "Integration with existing systems",
                    "Complete system overhaul",
                    "Unsure"
                ])
                
                budget_range = st.selectbox("Budget Range", [
                    "< €10K",
                    "€10K - €50K",
                    "€50K - €100K",
                    "€100K - €500K",
                    "> €500K",
                    "To be determined"
                ])
            
            # Additional Information
            st.subheader("Additional Information")
            
            stakeholders = st.text_area(
                "Key Stakeholders",
                placeholder="Who would be involved in this project? (names, roles, departments)",
                height=80
            )
            
            additional_notes = st.text_area(
                "Additional Notes",
                placeholder="Any other relevant information, constraints, or requirements...",
                height=80
            )
            
            # Submit button
            submitted = st.form_submit_button("🚀 Submit Use Case", use_container_width=True)
            
            if submitted:
                # Validate required fields
                if not all([submitter_name, submitter_email, department != "Select Department", 
                           business_unit != "Select Business Unit", use_case_title, 
                           problem_description, proposed_solution]):
                    st.error("Please fill in all required fields marked with *")
                else:
                    # Process submission
                    success = process_use_case_submission({
                        "submitter_name": submitter_name,
                        "submitter_email": submitter_email,
                        "department": department,
                        "business_unit": business_unit,
                        "priority": priority,
                        "timeline": timeline,
                        "use_case_title": use_case_title,
                        "problem_description": problem_description,
                        "proposed_solution": proposed_solution,
                        "expected_benefits": expected_benefits,
                        "data_availability": data_availability,
                        "technical_complexity": technical_complexity,
                        "integration_needs": integration_needs,
                        "budget_range": budget_range,
                        "stakeholders": stakeholders,
                        "additional_notes": additional_notes,
                        "submission_date": datetime.now().isoformat()
                    })
                    
                    if success:
                        st.success("✅ Use case submitted successfully! Our AI team will review it and get back to you within 48 hours.")
                        st.balloons()
                        log_user_action("use_case_submitted", {"title": use_case_title, "department": department})
                    else:
                        st.error("❌ There was an error submitting your use case. Please try again or contact the AI team.")
    
    with col2:
        st.markdown("#### 🤝 Need Help?")
        st.markdown("""
        **AI Team Contacts:**
        - 📧 ai-team@aperam.com
        - 💬 Teams: AI Innovation
        - 📞 Ext: 2024
        
        **Office Hours:**
        - Mon-Fri: 9:00-17:00
        - Quick questions: Anytime
        """)
        
        st.markdown("#### 📈 Success Stories")
        st.markdown("""
        **Recent Wins:**
        - 🏭 Quality Control AI: 30% defect reduction
        - 📊 Demand Forecasting: 25% inventory optimization
        - 🔧 Predictive Maintenance: 40% downtime reduction
        """)
        
        if st.button("📞 Schedule AI Consultation", use_container_width=True):
            st.info("Calendly integration coming soon! Email ai-team@aperam.com to schedule.")
        
        # Google Sheets integration status
        st.markdown("#### 🔧 Integration Status")
        connection_status = test_sheets_connection()
        if connection_status["success"]:
            st.success(f"✅ {connection_status['method']} integration active")
        else:
            st.warning(f"⚠️ Using fallback method: {connection_status.get('error', 'No external integration')}")
        
        if st.button("🔄 Test Connection", use_container_width=True):
            with st.spinner("Testing connection..."):
                status = test_sheets_connection()
                if status["success"]:
                    st.success("✅ Connection successful!")
                else:
                    st.error(f"❌ Connection failed: {status.get('error', 'Unknown error')}")

def render_existing_ideas():
    """Render the existing ideas showcase"""
    st.markdown("### 💡 Existing AI Ideas & Inspirations")
    
    st.markdown("""
    Explore ideas from your colleagues and discover what's possible with AI at Aperam.
    These examples can inspire your own submissions or help you refine your concepts.
    """)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_department = st.selectbox("Filter by Department", [
            "All Departments",
            "Research & Development",
            "Production",
            "Quality Control",
            "Supply Chain",
            "Finance",
            "Sales & Marketing",
            "IT",
            "HR"
        ])
    
    with col2:
        filter_status = st.selectbox("Filter by Status", [
            "All Statuses",
            "Under Review",
            "In Development",
            "Completed",
            "On Hold"
        ])
    
    with col3:
        filter_complexity = st.selectbox("Filter by Complexity", [
            "All Complexities",
            "Simple automation",
            "Moderate AI/ML required",
            "Complex AI/ML required",
            "Cutting-edge research needed"
        ])
    
    # Sample existing ideas
    existing_ideas = get_sample_use_cases()
    
    # Apply filters
    filtered_ideas = apply_filters(existing_ideas, filter_department, filter_status, filter_complexity)
    
    # Display ideas in cards
    for i, idea in enumerate(filtered_ideas):
        with st.expander(f"💡 {idea['title']} - {idea['department']} ({idea['status']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Problem:** {idea['problem']}")
                st.markdown(f"**Solution:** {idea['solution']}")
                st.markdown(f"**Expected Benefits:** {idea['benefits']}")
                st.markdown(f"**Timeline:** {idea['timeline']}")
            
            with col2:
                st.markdown(f"**Priority:** {idea['priority']}")
                st.markdown(f"**Complexity:** {idea['complexity']}")
                st.markdown(f"**Budget:** {idea['budget']}")
                
                if idea['status'] == "Completed":
                    st.success("✅ Completed")
                elif idea['status'] == "In Development":
                    st.info("🔄 In Development")
                elif idea['status'] == "Under Review":
                    st.warning("⏳ Under Review")
                else:
                    st.error("⏸️ On Hold")
            
            # Action buttons
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                if st.button(f"👍 Like", key=f"like_{i}"):
                    st.success("Liked!")
            with col_btn2:
                if st.button(f"💬 Comment", key=f"comment_{i}"):
                    st.info("Comment feature coming soon!")
            with col_btn3:
                if st.button(f"🔄 Similar Idea", key=f"similar_{i}"):
                    st.session_state.similar_idea = idea
                    st.info("Use this as template for your submission!")

def render_my_submissions():
    """Render user's submissions tracking"""
    st.markdown("### 📊 My Submissions")
    
    # This would typically fetch from a database
    user_submissions = get_user_submissions()
    
    if not user_submissions:
        st.info("No submissions yet. Submit your first AI use case to get started!")
        return
    
    # Display submissions
    for submission in user_submissions:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{submission['title']}**")
                st.markdown(f"Submitted: {submission['date']}")
                st.markdown(f"Department: {submission['department']}")
            
            with col2:
                if submission['status'] == "Approved":
                    st.success("✅ Approved")
                elif submission['status'] == "Under Review":
                    st.warning("⏳ Under Review")
                elif submission['status'] == "In Development":
                    st.info("🔄 In Development")
                else:
                    st.error("❌ Declined")
            
            with col3:
                if st.button(f"View Details", key=f"view_{submission['id']}"):
                    show_submission_details(submission)
            
            st.markdown("---")

def process_use_case_submission(submission_data: Dict) -> bool:
    """Process and store use case submission"""
    try:
        # 1. Validate the data
        if not _validate_submission_data(submission_data):
            return False
        
        # 2. Submit to Google Sheets
        sheets_success = submit_use_case_to_sheets(submission_data)
        
        # 3. Log the action
        log_user_action("use_case_submitted", {
            "title": submission_data.get('use_case_title'),
            "department": submission_data.get('department'),
            "sheets_success": sheets_success
        })
        
        # 4. Return success status
        return sheets_success
        
    except Exception as e:
        st.error(f"Error processing submission: {str(e)}")
        log_user_action("use_case_submission_error", {"error": str(e)})
        return False

def _validate_submission_data(data: Dict) -> bool:
    """Validate submission data"""
    required_fields = [
        'submitter_name', 'submitter_email', 'department', 
        'business_unit', 'use_case_title', 'problem_description', 
        'proposed_solution'
    ]
    
    for field in required_fields:
        if not data.get(field) or data.get(field) == f"Select {field.replace('_', ' ').title()}":
            st.error(f"Please fill in the {field.replace('_', ' ').title()} field")
            return False
    
    # Email validation
    email = data.get('submitter_email', '')
    if '@' not in email or '.' not in email:
        st.error("Please enter a valid email address")
        return False
    
    return True

def get_sample_use_cases() -> List[Dict]:
    """Get sample use cases for demonstration"""
    return [
        {
            "title": "Automated Steel Quality Grading",
            "department": "Quality Control",
            "status": "In Development",
            "priority": "High",
            "complexity": "Moderate AI/ML required",
            "budget": "€50K - €100K",
            "timeline": "Short-term (1-3 months)",
            "problem": "Manual quality grading is time-consuming and inconsistent across different inspectors",
            "solution": "Computer vision system to automatically grade steel products based on visual inspection",
            "benefits": "50% reduction in inspection time, consistent quality standards, reduced human error"
        },
        {
            "title": "Predictive Maintenance for Rolling Mills",
            "department": "Production",
            "status": "Completed",
            "priority": "High",
            "complexity": "Complex AI/ML required",
            "budget": "€100K - €500K",
            "timeline": "Medium-term (3-6 months)",
            "problem": "Unexpected equipment failures cause costly downtime and production delays",
            "solution": "ML model using sensor data to predict equipment failures 2-4 weeks in advance",
            "benefits": "40% reduction in unplanned downtime, 25% maintenance cost savings, improved safety"
        },
        {
            "title": "Demand Forecasting Optimization",
            "department": "Supply Chain",
            "status": "Under Review",
            "priority": "Medium",
            "complexity": "Moderate AI/ML required",
            "budget": "€10K - €50K",
            "timeline": "Short-term (1-3 months)",
            "problem": "Current forecasting methods are inaccurate, leading to overstock or stockouts",
            "solution": "Advanced ML model incorporating market trends, seasonality, and external factors",
            "benefits": "15% improvement in forecast accuracy, 20% reduction in inventory costs"
        },
        {
            "title": "Automated Invoice Processing",
            "department": "Finance",
            "status": "Completed",
            "priority": "Medium",
            "complexity": "Simple automation",
            "budget": "< €10K",
            "timeline": "ASAP (1-2 weeks)",
            "problem": "Manual processing of invoices is slow and error-prone",
            "solution": "OCR and NLP to automatically extract and validate invoice data",
            "benefits": "80% reduction in processing time, 95% accuracy improvement"
        },
        {
            "title": "Customer Behavior Analytics",
            "department": "Sales & Marketing",
            "status": "On Hold",
            "priority": "Low",
            "complexity": "Complex AI/ML required",
            "budget": "€50K - €100K",
            "timeline": "Long-term (6+ months)",
            "problem": "Limited insights into customer preferences and buying patterns",
            "solution": "ML model to analyze customer data and predict buying behavior",
            "benefits": "Improved customer targeting, increased sales conversion, better product recommendations"
        },
        {
            "title": "Energy Consumption Optimization",
            "department": "Production",
            "status": "In Development",
            "priority": "High",
            "complexity": "Moderate AI/ML required",
            "budget": "€100K - €500K",
            "timeline": "Medium-term (3-6 months)",
            "problem": "High energy costs and carbon footprint from inefficient energy usage",
            "solution": "AI system to optimize energy consumption based on production schedules and grid prices",
            "benefits": "15% reduction in energy costs, 20% carbon footprint reduction"
        }
    ]

def apply_filters(ideas: List[Dict], department: str, status: str, complexity: str) -> List[Dict]:
    """Apply filters to the ideas list"""
    filtered = ideas
    
    if department != "All Departments":
        filtered = [idea for idea in filtered if idea['department'] == department]
    
    if status != "All Statuses":
        filtered = [idea for idea in filtered if idea['status'] == status]
    
    if complexity != "All Complexities":
        filtered = [idea for idea in filtered if idea['complexity'] == complexity]
    
    return filtered

def get_user_submissions() -> List[Dict]:
    """Get user's submissions (mock data)"""
    # In a real implementation, this would fetch from database based on user ID
    return [
        {
            "id": "1",
            "title": "Automated Report Generation",
            "department": "Finance",
            "status": "Under Review",
            "date": "2024-01-15",
            "priority": "Medium"
        },
        {
            "id": "2",
            "title": "Customer Sentiment Analysis",
            "department": "Sales & Marketing",
            "status": "Approved",
            "date": "2024-01-10",
            "priority": "High"
        }
    ]

def show_submission_details(submission: Dict):
    """Show detailed view of a submission"""
    st.modal("Submission Details")
    st.markdown(f"**Title:** {submission['title']}")
    st.markdown(f"**Department:** {submission['department']}")
    st.markdown(f"**Status:** {submission['status']}")
    st.markdown(f"**Priority:** {submission['priority']}")
    st.markdown(f"**Submitted:** {submission['date']}")