"""Main Streamlit application entry point."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st

# Configure page
st.set_page_config(
    page_title="CRISP Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Home page content
st.title("CRISP Analysis Dashboard")
st.markdown("Welcome to the CRISP Analysis Dashboard application.")

# Educational content about CRISP-DM
with st.expander("📚 What is CRISP-DM?", expanded=False):
    st.markdown("""
    **CRISP-DM** (Cross-Industry Standard Process for Data Mining) is a proven methodology for data science projects with six phases:
    
    1. **Business Understanding** - Define objectives and requirements
    2. **Data Understanding** - Explore and assess available data
    3. **Data Preparation** - Clean, transform, and prepare data
    4. **Modeling** - Build and test models
    5. **Evaluation** - Assess results against business objectives
    6. **Deployment** - Implement and monitor the solution
    
    This dashboard helps document experiments following CRISP-DM principles. Each experiment captures the problem statement, baseline, objectives, methodology, and evaluation criteria - key elements of a structured data science process.
    """)

st.markdown("""
### Navigation

Use the navigation links in the sidebar (top-left) to access:

- **📝 Form**: Submit new CRISP experiments following the CRISP-DM framework
- **📊 Dashboard**: View and analyze your experiments with visualizations and data tables

### Getting Started

1. Navigate to the **Dashboard** page to view visualizations and browse experiment details (10 sample experiments are automatically loaded if no data exists)
2. Navigate to the **Form** page to submit your own experiments following CRISP-DM methodology
""")

st.info("💡 **Tip**: Use the navigation links in the top-left sidebar to switch between pages.")

