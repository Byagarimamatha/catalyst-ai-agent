import streamlit as st
import json
import pandas as pd
from datetime import datetime
from jd_parser import parse_jd_simple
from matcher import calculate_match_score
from outreach import OutreachSimulator

st.set_page_config(
    page_title="Catalyst AI - Talent Scouting",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .gradient-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .candidate-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .badge-high { background-color: #10b981; color: white; padding: 0.25rem 0.75rem; border-radius: 2rem; font-size: 0.8rem; }
    .badge-medium { background-color: #f59e0b; color: white; padding: 0.25rem 0.75rem; border-radius: 2rem; font-size: 0.8rem; }
    .badge-low { background-color: #ef4444; color: white; padding: 0.25rem 0.75rem; border-radius: 2rem; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="gradient-header">
    <h1>🎯 Catalyst AI</h1>
    <h3>Intelligent Talent Scouting & Engagement Agent</h3>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ System Status")
    st.success("✅ Agent Ready")
    st.info("🎯 6 Candidates Available")
    st.info("🔍 Smart Matching Active")
    st.markdown("---")
    st.caption(f"Session: {datetime.now().strftime('%H:%M:%S')}")

# Main
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Job Description")
    jd_input = st.text_area(
        "",
        height=250,
        placeholder="Example:\nPython Developer with 3+ years experience.\nSkills: Python, SQL, React.",
        label_visibility="collapsed"
    )
    
    if st.button("🔍 Find Candidates", type="primary", use_container_width=True):
        if jd_input:
            with st.spinner("Analyzing..."):
                jd_req = parse_jd_simple(jd_input)
                with open("candidates.json", "r") as f:
                    candidates = json.load(f)["candidates"]
                outreach = OutreachSimulator()
                st.session_state['jd_req'] = jd_req
                st.session_state['candidates'] = candidates
                st.session_state['outreach'] = outreach
                st.session_state['processed'] = True
                st.success("✅ Job analyzed!")
                with st.expander("📋 Extracted Requirements"):
                    st.metric("Role", jd_req['role'])
                    st.metric("Experience", f"{jd_req['required_experience']}+ years")
                    st.write("**Skills:**", ", ".join(jd_req['required_skills']))
        else:
            st.error("Please enter a job description")

with col2:
    st.subheader("🎯 Candidate Shortlist")
    if st.session_state.get('processed', False):
        jd_req = st.session_state['jd_req']
        candidates = st.session_state['candidates']
        outreach = st.session_state['outreach']
        
        results = []
        for candidate in candidates:
            match_result = calculate_match_score(candidate, jd_req)
            response = outreach.simulate_candidate_response(candidate['id'], match_result['score'])
            interest_result = outreach.calculate_interest_score(response)
            combined = (match_result['score'] * 0.7) + (interest_result['score'] * 0.3)
            results.append({
                "candidate": candidate,
                "match_score": match_result['score'],
                "interest_score": interest_result['score'],
                "interest_level": interest_result['level'],
                "interest_details": interest_result,
                "combined_score": round(combined, 1),
                "response": response
            })
        
        results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        for idx, r in enumerate(results[:5], 1):
            c = r['candidate']
            if idx == 1:
                medal = "🥇"
            elif idx == 2:
                medal = "🥈"
            elif idx == 3:
                medal = "🥉"
            else:
                medal = f"#{idx}"
            
            if r['interest_level'] == 'High':
                badge = f'<span class="badge-high">🔥 High Interest</span>'
            elif r['interest_level'] == 'Medium':
                badge = f'<span class="badge-medium">📌 Medium Interest</span>'
            else:
                badge = f'<span class="badge-low">💤 Low Interest</span>'
            
            st.markdown(f"""
            <div class="candidate-card">
                <h3>{medal} {c['name']}</h3>
                <p><strong>{c['current_role']}</strong> • {c['experience_years']} years • {c['location']}</p>
                <p>🎯 Match: {r['match_score']}/100 | 💬 Interest: {r['interest_score']}/100 | ⭐ Combined: {r['combined_score']}/100</p>
                <p>{badge}</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("💬 View Conversation"):
                st.text(r['response'])
        
        export_data = [{"name": r['candidate']['name'], "match": r['match_score'], "interest": r['interest_score'], "combined": r['combined_score']} for r in results]
        st.download_button("📥 Export JSON", json.dumps(export_data, indent=2), "shortlist.json")
    else:
        st.info("👈 Paste a job description and click 'Find Candidates'")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>🎯 Catalyst AI - Powered by Smart Matching</p>", unsafe_allow_html=True)
