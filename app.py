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

# Sidebar - CLEAN (no OpenAI)
with st.sidebar:
    st.markdown("### ⚙️ System Status")
    st.success("✅ Agent Ready")
    st.info("🎯 6 Candidates Available")
    st.info("🔍 Smart Matching Active")
    st.markdown("---")
    st.caption(f"Session: {datetime.now().strftime('%H:%M:%S')}")

# Main columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Job Description")
    jd_input = st.text_area(
        "Paste job description here",
        height=250,
        placeholder="Example:\nPython Developer with 3+ years experience.\nSkills: Python, SQL, React.",
        label_visibility="collapsed"
    )
    
    if st.button("🔍 Find Candidates", type="primary", use_container_width=True):
        if jd_input:
            with st.spinner("Analyzing job requirements..."):
                jd_req = parse_jd_simple(jd_input)
                
                with open("candidates.json", "r") as f:
                    candidates = json.load(f)["candidates"]
                
                outreach = OutreachSimulator()
                
                st.session_state['jd_req'] = jd_req
                st.session_state['candidates'] = candidates
                st.session_state['outreach'] = outreach
                st.session_state['processed'] = True
                
                st.success("✅ Job analyzed successfully!")
                
                with st.expander("📋 Extracted Requirements"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Role", jd_req['role'])
                        st.metric("Required Experience", f"{jd_req['required_experience']}+ years")
                    with col_b:
                        st.write("**Required Skills:**")
                        st.write(", ".join(jd_req['required_skills']) if jd_req['required_skills'] else "None detected")
        else:
            st.error("⚠️ Please enter a job description")

with col2:
    st.subheader("🎯 Candidate Shortlist")
    st.markdown("*Ranked by Match Score + Interest Level*")
    
    if st.session_state.get('processed', False):
        jd_req = st.session_state['jd_req']
        candidates = st.session_state['candidates']
        outreach = st.session_state['outreach']
        
        results = []
        progress_bar = st.progress(0)
        for i, candidate in enumerate(candidates):
            match_result = calculate_match_score(candidate, jd_req)
            response = outreach.simulate_candidate_response(candidate['id'], match_result['score'])
            interest_result = outreach.calculate_interest_score(response)
            combined = (match_result['score'] * 0.7) + (interest_result['score'] * 0.3)
            
            results.append({
                "candidate": candidate,
                "match_score": match_result['score'],
                "match_explanation": match_result['explanation'],
                "matched_skills": match_result.get('matched_skills', []),
                "missing_skills": match_result.get('missing_skills', []),
                "interest_score": interest_result['score'],
                "interest_level": interest_result['level'],
                "interest_details": interest_result,
                "combined_score": round(combined, 1),
                "response": response
            })
            progress_bar.progress((i + 1) / len(candidates))
        
        results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        # Summary metrics
        st.markdown("### 📊 Summary")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total", len(results))
        with m2:
            st.metric("Avg Match", f"{sum(r['match_score'] for r in results)/len(results):.0f}")
        with m3:
            high = len([r for r in results if r['interest_level'] == 'High'])
            st.metric("High Interest", high)
        with m4:
            ready = len([r for r in results if r['interest_score'] > 60])
            st.metric("Ready to Contact", ready)
        
        st.markdown("---")
        st.markdown("### 🏆 Ranked Shortlist")
        
        for idx, r in enumerate(results[:5], 1):
           c = r['candidate']
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
            badge = f'<span class="badge-{"high" if r["interest_level"]=="High" else "medium" if r["interest_level"]=="Medium" else "low"}">{r["interest_level"]} Interest</span>'
            
            st.markdown(f"""
            <div class="candidate-card">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <h3>{medal} {c['name']}</h3>
                        <p><strong>{c['current_role']}</strong> • {c['experience_years']} years • {c['location']}</p>
                    </div>
                    <div>{badge}</div>
                </div>
                <hr>
                <div style="display: flex; gap: 2rem;">
                    <div>
                        <p>🎯 Match: <strong>{r['match_score']}/100</strong></p>
                        <p>💬 Interest: <strong>{r['interest_score']}/100</strong></p>
                        <p>⭐ Combined: <strong>{r['combined_score']}/100</strong></p>
                    </div>
                    <div>
                        <p>✅ Matched: {', '.join(r['matched_skills'][:3]) if r['matched_skills'] else 'None'}</p>
                        <p>❌ Missing: {', '.join(r['missing_skills'][:2]) if r['missing_skills'] else 'None'}</p>
                        <p>📅 Available: {r['interest_details']['availability']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("💬 View Conversation"):
                st.text_area("Candidate Response:", r['response'], height=100, key=f"resp_{idx}")
        
        # Export
        st.markdown("---")
        export_data = [{
            "rank": i+1,
            "name": r['candidate']['name'],
            "email": r['candidate']['email'],
            "match_score": r['match_score'],
            "interest_score": r['interest_score'],
            "combined_score": r['combined_score'],
            "interest_level": r['interest_level'],
            "availability": r['interest_details']['availability']
        } for i, r in enumerate(results)]
        
        st.download_button(
            "📥 Export Shortlist (JSON)",
            json.dumps(export_data, indent=2),
            f"shortlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            use_container_width=True
        )
    else:
        st.info("👈 Paste a job description and click 'Find Candidates'")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>🎯 Catalyst AI - Powered by Smart Matching | Built for Hackathon 2026</p>", unsafe_allow_html=True)
