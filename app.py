import streamlit as st
import json
import pandas as pd
from datetime import datetime
from jd_parser import parse_jd_simple
from matcher import calculate_match_score
from outreach import OutreachSimulator

# Page config MUST be first command
st.set_page_config(
    page_title="Catalyst AI - Talent Scouting Engine",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Gradient header */
    .gradient-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    /* Score cards */
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    
    /* Candidate cards */
    .candidate-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    /* Metric styling */
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* Badge styles */
    .badge-high {
        background-color: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        display: inline-block;
        font-size: 0.875rem;
    }
    
    .badge-medium {
        background-color: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        display: inline-block;
        font-size: 0.875rem;
    }
    
    .badge-low {
        background-color: #ef4444;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        display: inline-block;
        font-size: 0.875rem;
    }
    
    /* Progress bar custom */
    .stProgress > div > div > div > div {
        background-color: #667eea;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Custom button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header with gradient
st.markdown("""
<div class="gradient-header fade-in">
    <h1>🎯 Catalyst AI</h1>
    <h3>Intelligent Talent Scouting & Engagement Agent</h3>
    <p>Powered by Advanced AI Matching | Real-time Interest Detection | Smart Shortlisting</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with modern design
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # Toggle for AI mode
    use_ai = st.toggle("🤖 Enable AI Enhancement", value=False, help="Use OpenAI for better JD parsing")
    
    if use_ai:
        api_key = st.text_input("🔑 OpenAI API Key", type="password", placeholder="sk-...")
        st.caption("🔒 Your key is not stored")
    
    st.markdown("---")
    
    # Stats placeholder
    st.markdown("### 📊 System Status")
    st.info("✅ Agent Ready\n✅ Candidate Pool: 6\n✅ Matching Engine: Active")
    
    st.markdown("---")
    
    # Quick tips
    with st.expander("💡 Pro Tips"):
        st.markdown("""
        - Be specific about required skills
        - Mention years of experience clearly
        - Include role/position title
        - Add location preferences
        """)
    
    st.markdown("---")
    st.caption("🎯 Catalyst AI | Built for Hackathon 2026")
    st.caption(f"🕐 Session Started: {datetime.now().strftime('%H:%M:%S')}")

# Main content area - Two columns for better layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Job Description Input")
    st.markdown("*Paste your job description below and let AI do the magic*")
    
    # Better JD input with examples
    jd_input = st.text_area(
        "",
        height=350,
        placeholder="""
🎯 Example Job Description:

Title: Senior Full Stack Python Developer

We are looking for an experienced Python Developer with:
- 5+ years of Python experience
- Strong knowledge of Django/Flask
- React.js for frontend
- PostgreSQL and MongoDB
- AWS cloud services

Responsibilities:
- Design and develop scalable applications
- Lead technical discussions
- Mentor junior developers

Benefits:
- Remote work options
- Competitive salary
- Health insurance
        """,
        label_visibility="collapsed"
    )
    
    # Example JDs quick buttons
    st.markdown("**Quick Examples:**")
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    
    with ex_col1:
        if st.button("🐍 Python Dev", use_container_width=True):
            jd_input = """Python Developer with 3+ years experience. 
Skills: Python, Django, PostgreSQL, REST APIs. 
Looking for someone who can build scalable applications."""
    
    with ex_col2:
        if st.button("📊 Data Scientist", use_container_width=True):
            jd_input = """Data Scientist with 4+ years experience. 
Skills: Python, Pandas, Scikit-learn, TensorFlow, SQL.
Need experience in machine learning and data analysis."""
    
    with ex_col3:
        if st.button("☁️ DevOps Engineer", use_container_width=True):
            jd_input = """DevOps Engineer with 5+ years experience.
Skills: AWS, Docker, Kubernetes, Jenkins, Terraform.
CI/CD pipeline expertise required."""
    
    st.markdown("---")
    
    # Process button with better styling
    process_clicked = st.button("🚀 Analyze & Shortlist Candidates", type="primary", use_container_width=True)
    
    if process_clicked:
        if jd_input:
            with st.spinner("🔍 Processing job requirements..."):
                # Parse JD
                if use_ai and api_key:
                    jd_req = parse_jd_with_ai(jd_input, api_key)
                else:
                    jd_req = parse_jd_simple(jd_input)
                
                # Load candidates
                with open("candidates.json", "r") as f:
                    data = json.load(f)
                    candidates = data["candidates"]
                
                # Initialize outreach simulator
                outreach = OutreachSimulator()
                
                # Store in session state
                st.session_state['jd_req'] = jd_req
                st.session_state['candidates'] = candidates
                st.session_state['outreach'] = outreach
                st.session_state['processed'] = True
                st.session_state['timestamp'] = datetime.now()
                
                st.success("✅ Job Description Processed Successfully!")
                
                # Show parsed requirements in a nice format
                with st.expander("📋 Parsed Requirements", expanded=False):
                    req_col1, req_col2, req_col3 = st.columns(3)
                    with req_col1:
                        st.metric("🎯 Role", jd_req['role'])
                    with req_col2:
                        st.metric("📅 Required Experience", f"{jd_req['required_experience']}+ years")
                    with req_col3:
                        st.metric("🔧 Skills Required", len(jd_req['required_skills']))
                    
                    if jd_req['required_skills']:
                        st.markdown("**Required Skills:**")
                        skill_chips = " ".join([f"`{skill}`" for skill in jd_req['required_skills']])
                        st.markdown(skill_chips)
        else:
            st.error("⚠️ Please enter a job description")

with col2:
    st.markdown("### 🎯 Candidate Shortlist")
    st.markdown("*Ranked by Match Score + Interest Level*")
    
    if st.session_state.get('processed', False):
        jd_req = st.session_state['jd_req']
        candidates = st.session_state['candidates']
        outreach = st.session_state['outreach']
        
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Calculate match scores
        results = []
        for i, candidate in enumerate(candidates):
            status_text.text(f"Analyzing {candidate['name']}...")
            match_result = calculate_match_score(candidate, jd_req)
            
            # Simulate conversation
            initial_msg = outreach.send_initial_message(candidate, jd_req['role'])
            response = outreach.simulate_candidate_response(candidate['id'], match_result['score'])
            interest_result = outreach.calculate_interest_score(response)
            
            # Combined score (70% match, 30% interest)
            combined_score = (match_result['score'] * 0.7) + (interest_result['score'] * 0.3)
            
            results.append({
                "candidate": candidate,
                "match_score": match_result['score'],
                "match_explanation": match_result['explanation'],
                "matched_skills": match_result['matched_skills'],
                "missing_skills": match_result['missing_skills'],
                "interest_score": interest_result['score'],
                "interest_level": interest_result['level'],
                "interest_details": interest_result,
                "combined_score": round(combined_score, 1),
                "conversation": {
                    "initial_message": initial_msg,
                    "response": response
                }
            })
            progress_bar.progress((i + 1) / len(candidates))
        
        status_text.text("✅ Analysis complete!")
        
        # Sort by combined score
        results.sort(key=lambda x: x['combined_score'], reverse=True)
        st.session_state['results'] = results
        
        # Show summary metrics
        st.markdown("### 📊 Summary")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        with metric_col1:
            st.metric("Total Candidates", len(results))
        with metric_col2:
            st.metric("Avg Match Score", f"{sum(r['match_score'] for r in results)/len(results):.0f}")
        with metric_col3:
            high_interest = len([r for r in results if r['interest_level'] == 'High'])
            st.metric("High Interest", high_interest)
        with metric_col4:
            st.metric("Ready to Contact", len([r for r in results if r['interest_score'] > 60]))
        
        st.markdown("---")
        
        # Display candidates in beautiful cards
        st.markdown("### 🏆 Ranked Shortlist")
        
        for idx, result in enumerate(results[:5], 1):
            candidate = result['candidate']
            
            # Color based on rank
            if idx == 1:
                medal = "🥇"
            elif idx == 2:
                medal = "🥈"
            elif idx == 3:
                medal = "🥉"
            else:
                medal = f"#{idx}"
            
            # Interest badge
            if result['interest_level'] == 'High':
                badge = '<span class="badge-high">🔥 High Interest</span>'
            elif result['interest_level'] == 'Medium':
                badge = '<span class="badge-medium">📌 Medium Interest</span>'
            else:
                badge = '<span class="badge-low">💤 Low Interest</span>'
            
            with st.container():
                st.markdown(f"""
                <div class="candidate-card fade-in">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3>{medal} {candidate['name']}</h3>
                            <p><strong>{candidate['current_role']}</strong> • {candidate['experience_years']} years • {candidate['location']}</p>
                        </div>
                        <div>
                            {badge}
                        </div>
                    </div>
                    <hr>
                    <div style="display: flex; gap: 2rem;">
                        <div style="flex: 1;">
                            <p>🎯 Match Score: <strong>{result['match_score']}/100</strong></p>
                            <div class="stProgress">
                                <div style="background: linear-gradient(90deg, #667eea {result['match_score']}%, #e5e7eb {result['match_score']}%); 
                                            height: 8px; border-radius: 4px; width: 100%;"></div>
                            </div>
                            <p>💬 Interest: <strong>{result['interest_score']}/100</strong></p>
                            <div class="stProgress">
                                <div style="background: linear-gradient(90deg, #10b981 {result['interest_score']}%, #e5e7eb {result['interest_score']}%); 
                                            height: 8px; border-radius: 4px; width: 100%;"></div>
                            </div>
                            <p>⭐ Combined: <strong>{result['combined_score']}/100</strong></p>
                        </div>
                        <div style="flex: 1;">
                            <p>✅ Matched: {', '.join(result['matched_skills'][:3])}</p>
                            <p>❌ Missing: {', '.join(result['missing_skills'][:2])}</p>
                            <p>📅 Availability: {result['interest_details']['availability']}</p>
                            <p>💰 Expected: {result['interest_details']['salary']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Expandable conversation
                with st.expander("💬 View Conversation Details", expanded=False):
                    st.text_area("📨 Initial Outreach:", result['conversation']['initial_message'], 
                                height=150, key=f"msg_{idx}")
                    st.text_area("💬 Candidate Response:", result['conversation']['response'], 
                                height=100, key=f"resp_{idx}")
        
        # Export options
        st.markdown("---")
        st.markdown("### 📤 Export Results")
        
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            # Convert to DataFrame for better display
            df_data = []
            for result in results:
                df_data.append({
                    "Name": result['candidate']['name'],
                    "Email": result['candidate']['email'],
                    "Role": result['candidate']['current_role'],
                    "Match Score": result['match_score'],
                    "Interest Score": result['interest_score'],
                    "Combined Score": result['combined_score'],
                    "Interest Level": result['interest_level'],
                    "Availability": result['interest_details']['availability']
                })
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        with exp_col2:
            if st.button("📥 Download Shortlist (JSON)", use_container_width=True):
                export_data = []
                for result in results:
                    export_data.append({
                        "rank": results.index(result) + 1,
                        "name": result['candidate']['name'],
                        "email": result['candidate']['email'],
                        "current_role": result['candidate']['current_role'],
                        "experience_years": result['candidate']['experience_years'],
                        "match_score": result['match_score'],
                        "interest_score": result['interest_score'],
                        "combined_score": result['combined_score'],
                        "interest_level": result['interest_level'],
                        "availability": result['interest_details']['availability'],
                        "salary_expectation": result['interest_details']['salary'],
                        "full_response": result['conversation']['response'],
                        "timestamp": str(st.session_state.get('timestamp', datetime.now()))
                    })
                
                st.download_button(
                    label="💾 Save JSON File",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"catalyst_shortlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    else:
        # Placeholder when no processing done
        st.info("👈 Start by pasting a job description and clicking 'Analyze & Shortlist Candidates'")
        
        # Show sample output preview
        with st.expander("🔍 Preview: Sample Output", expanded=False):
            st.markdown("""
            **When you run the agent, you'll see:**
            
            1. 📊 Parsed job requirements
            2. 🎯 Match scores for each candidate
            3. 💬 Simulated conversation responses
            4. 📈 Interest scores based on replies
            5. 🏆 Ranked shortlist ready for recruiter
            """)
            
            # Sample visualization
            sample_data = pd.DataFrame({
                'Candidate': ['Sarah J.', 'Mike C.', 'Priya P.'],
                'Match Score': [85, 72, 68],
                'Interest Score': [90, 65, 45],
                'Combined': [87, 70, 61]
            })
            st.bar_chart(sample_data.set_index('Candidate'))

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🚀 Powered by AI Matching Engine | 💬 Conversational Outreach Simulation | 🎯 Real-time Scoring</p>
    <p><small>Catalyst AI - Transforming Recruitment with Intelligent Automation</small></p>
</div>
""", unsafe_allow_html=True)
