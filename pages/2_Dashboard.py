"""Dashboard page for visualizing CRISP experiments."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
from src.pages.dashboard_page import render_dashboard

# Set page config
st.set_page_config(
    page_title="CRISP Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

render_dashboard()

