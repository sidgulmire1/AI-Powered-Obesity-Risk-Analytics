import streamlit as st
import os
import textwrap

from services.predictor_service import PredictionService
from services.data_service import DataService

st.set_page_config(
    page_title="AI Obesity Risk Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Base CSS overrides to match the exact visual reference
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 1500px !important;
}
.stApp {
    background-color: #EEF3F8 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Header */
.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}
.th-left { display: flex; align-items: center; gap: 1rem; }
.th-title h1 {
    font-size: 1.8rem;
    font-weight: 700;
    color: #142A46;
    margin: 0;
    line-height: 1.2;
}
.th-title p {
    font-size: 0.9rem;
    color: #5F7189;
    margin: 0;
}
.th-badge {
    background-color: #F1F6FF;
    color: #2563EB;
    border: 1px solid #D6E3FA;
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    font-size: 0.9rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Base Card Style */
.card-base {
    background-color: #FFFFFF;
    border: 1px solid #D8E2EE;
    border-radius: 14px;
    box-shadow: 0 4px 16px rgba(30, 60, 90, 0.06);
}

/* Left Column Card (Native overrides) */
[data-testid="column"]:nth-of-type(1) > div {
    background-color: #FFFFFF;
    border: 1px solid #D8E2EE;
    border-radius: 14px;
    padding: 1.25rem 1.25rem !important;
    box-shadow: 0 4px 16px rgba(30, 60, 90, 0.06);
}

/* Input Controls Customization */
.stSelectbox div[data-baseweb="select"] > div,
.stNumberInput input {
    background-color: #F7F9FC !important;
    border: 1px solid #D5DFEA !important;
    color: #172B46 !important;
    border-radius: 6px !important;
}

.left-card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.25rem;
}
.left-card-header h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #142A46;
}
.left-card-header p {
    margin: 0 0 1.5rem 0;
    font-size: 0.85rem;
    color: #5F7189;
}
.sec-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Button */
.stButton>button {
    background-color: #2563EB !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.75rem !important;
    width: 100% !important;
    margin-top: 1rem;
    border: none !important;
    transition: background-color 0.2s ease;
}
.stButton>button:hover { background-color: #1D4ED8 !important; }

/* Right Column Cards */
.rcard {
    background-color: #FFFFFF;
    border: 1px solid #D8E2EE;
    border-radius: 14px;
    padding: 1.25rem;
    box-shadow: 0 4px 16px rgba(30, 60, 90, 0.06);
    margin-bottom: 1.25rem;
}
.rcard-title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.25rem;
}
.rcard-title h3 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: #142A46;
}
.rcard-sub {
    font-size: 0.85rem;
    color: #5F7189;
    margin-bottom: 1.5rem;
}

/* Hero Content */
.hero-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #F3F7FF;
    border: 1px solid #D5E2F8;
    border-radius: 12px;
    padding: 1.5rem;
}
.hero-left h4 {
    font-size: 0.8rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.25rem 0;
}
.hero-val {
    font-size: 4rem;
    font-weight: 700;
    color: #2563EB;
    line-height: 1;
    margin-bottom: 0.25rem;
}
.hero-desc {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #475569;
    max-width: 250px;
}
.hero-ring {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    position: relative;
    background: #E2E8F0;
    display: flex;
    justify-content: center;
    align-items: center;
}
.hero-ring::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
}
.hero-ring-inner {
    width: 116px;
    height: 116px;
    background: #FFFFFF;
    border-radius: 50%;
    z-index: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.ring-v { font-size: 1.25rem; font-weight: 700; color: #2563EB; }
.ring-l { font-size: 0.75rem; color: #64748B; }

/* Grid */
.pop-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    background-color: #FAFCFF;
    padding: 1.25rem;
    border-radius: 12px;
}
.pop-cell {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    background-color: #F5F8FC;
    border: 1px solid #E1E8F0;
    padding: 0.75rem 1rem;
    border-radius: 8px;
}
.pop-lbl {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.7rem;
    color: #5F7189;
    font-weight: 500;
}
.pop-val {
    font-size: 0.95rem;
    color: #142A46;
    font-weight: 600;
    padding-left: 1.4rem;
}

/* Pipeline */
.pipe-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1rem;
    background-color: #F4F7FB;
    border: 1px solid #D8E2EE;
    border-radius: 12px;
}
.pipe-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    flex: 1;
}
.pipe-icon {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background-color: #FFFFFF;
    border: 1px solid #D8E2EE;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.75rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}
.pipe-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #142A46;
    margin-bottom: 0.25rem;
}
.pipe-sub {
    font-size: 0.7rem;
    color: #5F7189;
    max-width: 120px;
}
.pipe-arrow {
    color: #94A3B8;
    font-size: 1.25rem;
    margin-top: -30px;
}

/* Bottom Banner */
.bottom-banner {
    background-color: #EEF5FF;
    border: 1px solid #C9DCFA;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #365A88;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_services():
    return PredictionService(), DataService()

service, data_service = get_services()

# Header SVGs
heart_svg = '<svg width="40" height="40" viewBox="0 0 24 24" fill="#2563EB" xmlns="http://www.w3.org/2000/svg"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/><path d="M7 11h2.5l2-4 3 8 1.5-4H18" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>'
spark_badge_svg = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/></svg>'
params_icon = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18m6-18v18M3 9h18M3 15h18"/></svg>'
pred_icon = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18 9l-5 5-4-4-4 4"/></svg>'
prof_icon = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
pipe_icon = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'

# --- HEADER ---
st.markdown(f"""
<div class="top-header">
    <div class="th-left">
        {heart_svg}
        <div class="th-title">
            <h1>AI Obesity Risk Analytics</h1>
            <p>Population-level obesity prevalence analysis powered by machine learning</p>
        </div>
    </div>
    <div class="th-badge">
        {spark_badge_svg} ML + PySpark
    </div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([0.43, 0.57], gap="large")

with col_left:
    st.markdown(f"""
    <div class="left-card-header">
        {params_icon}
        <div>
            <h2>Analysis Parameters</h2>
            <p>Configure population characteristics to estimate obesity prevalence</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('''<div class='sec-title' style='color: #3B82F6;'><svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> DEMOGRAPHICS</div>''', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: age = st.selectbox("Age Group", data_service.get_unique("Age(years)"), index=None, placeholder="Select age group", key="param_age")
    with c2: sex = st.selectbox("Sex", data_service.get_unique("Sex"), index=None, placeholder="Select sex", key="param_sex")
    race = st.selectbox("Race / Ethnicity", data_service.get_unique("Race/Ethnicity"), index=None, placeholder="Select race / ethnicity", key="param_race")

    st.markdown('''<div class='sec-title' style='color: #10B981;'><svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg> SOCIOECONOMIC FACTORS</div>''', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3: education = st.selectbox("Education", data_service.get_unique("Education"), index=None, placeholder="Select education level", key="param_edu")
    with c4: income = st.selectbox("Income", data_service.get_unique("Income"), index=None, placeholder="Select income range", key="param_inc")

    st.markdown('''<div class='sec-title' style='color: #8B5CF6;'><svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg> GEOGRAPHY & TIMELINE</div>''', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5: location_desc = st.selectbox("State", data_service.get_unique("LocationDesc"), index=None, placeholder="Select state", key="param_state")
    with c6: year = st.number_input("Year", min_value=2011, max_value=2030, value=None, placeholder="Enter year", key="param_year")

    st.markdown('''<div class='sec-title' style='color: #F97316;'><svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg> SURVEY METRIC</div>''', unsafe_allow_html=True)
    question = st.selectbox("Question / Survey Metric", data_service.get_unique("Question"), index=None, placeholder="Select survey metric", key="param_question")
    
    if st.button("Analyze Prevalence"):
        if None in [age, sex, race, education, income, location_desc, year, question]:
            st.error("Please fill in all required fields before analyzing prevalence.")
        else:
            try:
                location_abbr = data_service.get_state_abbreviation(location_desc)
                pred_val = service.predict(year, location_abbr, location_desc, question, age, education, sex, income, race)
                
                st.session_state["prediction_result"] = pred_val
                st.session_state["prediction_profile"] = {
                    "State": location_desc, "Year": str(int(year)), "Age Group": age,
                    "Sex": sex, "Race": race, "Education": education,
                    "Income": income, "Survey Metric": question
                }
            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")
            
    st.markdown("<div style='text-align: center; font-size: 0.75rem; color: #64748B; margin-top: 0.5rem;'><svg width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' style='vertical-align: middle; margin-right: 4px;'><rect x='3' y='11' width='18' height='11' rx='2' ry='2'/><path d='M7 11V7a5 5 0 0 1 10 0v4'/></svg>Your selections are used only for analysis and are not stored.</div>", unsafe_allow_html=True)

with col_right:
    if "prediction_result" in st.session_state:
        p_val = st.session_state["prediction_result"]
        prof = st.session_state["prediction_profile"]
        
        # Calculate dynamic conic gradient ring
        ring_css = f"background: conic-gradient(#2563EB {p_val}%, #E2E8F0 0);"
        
        # Define small grid icons
        i_loc = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
        i_cal = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
        i_age = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
        i_sex = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#EC4899" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>'
        i_rac = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>'
        i_edu = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>'
        i_inc = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>'
        i_sur = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>'
        i_info = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'

        # Pipeline icons
        p_db = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'
        p_sp = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F97316" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
        p_fe = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>'
        p_ml = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#A855F7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>'
        p_pr = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
        
        html_output = f"""
<div class="rcard">
<div class="rcard-title">{pred_icon} <h3>Prediction & Analytics</h3></div>
<div class="rcard-sub">Model prediction for the selected population</div>
<div class="hero-content">
<div class="hero-left">
<h4>PREDICTED OBESITY PREVALENCE</h4>
<div class="hero-val">{p_val:.2f}%</div>
<div class="hero-desc">{i_info} Estimated percentage of adults with obesity for the selected population</div>
</div>
<div class="hero-right">
<div class="hero-ring" style="{ring_css}">
<div class="hero-ring-inner">
<span class="ring-v">{p_val:.2f}%</span>
<span class="ring-l">Prevalence</span>
</div>
</div>
</div>
</div>
</div>

<div class="rcard">
<div class="rcard-title">{prof_icon} <h3 style="font-size: 1rem;">Population Profile</h3></div>
<div class="rcard-sub" style="margin-bottom: 1rem;">Summary of selected population characteristics</div>
<div class="pop-grid">
<div class="pop-cell"><div class="pop-lbl">{i_loc} State</div><div class="pop-val">{prof['State']}</div></div>
<div class="pop-cell"><div class="pop-lbl">{i_cal} Year</div><div class="pop-val">{prof['Year']}</div></div>
<div class="pop-cell"><div class="pop-lbl">{i_age} Age Group</div><div class="pop-val">{prof['Age Group']}</div></div>
<div class="pop-cell"><div class="pop-lbl">{i_sex} Sex</div><div class="pop-val">{prof['Sex']}</div></div>
<div class="pop-cell"><div class="pop-lbl">{i_rac} Race / Ethnicity</div><div class="pop-val">{prof['Race']}</div></div>
<div class="pop-cell"><div class="pop-lbl">{i_edu} Education</div><div class="pop-val">{prof['Education']}</div></div>
<div class="pop-cell" style="grid-column: span 1;"><div class="pop-lbl">{i_inc} Income</div><div class="pop-val">{prof['Income']}</div></div>
<div class="pop-cell" style="grid-column: span 2;"><div class="pop-lbl">{i_sur} Survey Metric</div><div class="pop-val">{prof['Survey Metric']}</div></div>
</div>
</div>

<div class="rcard">
<div class="rcard-title">{pipe_icon} <h3 style="font-size: 1rem;">ML Pipeline Overview</h3></div>
<div class="rcard-sub" style="margin-bottom: 0.5rem;">How the prediction is generated</div>
<div class="pipe-row">
<div class="pipe-node"><div class="pipe-icon">{p_db}</div><div class="pipe-title">Data Source</div><div class="pipe-sub">Processed Survey Data</div></div>
<div class="pipe-arrow">&rarr;</div>
<div class="pipe-node"><div class="pipe-icon">{p_sp}</div><div class="pipe-title">PySpark Processing</div><div class="pipe-sub">Distributed Data Processing</div></div>
<div class="pipe-arrow">&rarr;</div>
<div class="pipe-node"><div class="pipe-icon">{p_fe}</div><div class="pipe-title">Feature Preparation</div><div class="pipe-sub">Encoding & Feature Engineering</div></div>
<div class="pipe-arrow">&rarr;</div>
<div class="pipe-node"><div class="pipe-icon">{p_ml}</div><div class="pipe-title">ML Model</div><div class="pipe-sub">Trained Regression Model</div></div>
<div class="pipe-arrow">&rarr;</div>
<div class="pipe-node"><div class="pipe-icon" style="border-color: #EF4444;">{p_pr}</div><div class="pipe-title">Prediction</div><div class="pipe-sub">Obesity Prevalence (Percentage)</div></div>
</div>
</div>
"""
        st.markdown(html_output, unsafe_allow_html=True)
    else:
        st.markdown("""
<div class="rcard" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 400px; text-align: center; color: #64748B;">
<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 1rem;"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
<h3 style="color: #0F172A; margin: 0 0 0.5rem 0;">Awaiting Analysis</h3>
<p style="max-width: 300px; margin: 0;">Configure the population parameters on the left and click <strong>Analyze Prevalence</strong> to view the model's predictions.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="bottom-banner">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
    This model predicts population-level obesity prevalence based on selected demographic and socioeconomic characteristics.
</div>
""", unsafe_allow_html=True)