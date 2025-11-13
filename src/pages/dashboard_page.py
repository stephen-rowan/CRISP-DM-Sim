"""Dashboard page for visualizing CRISP experiments."""

import streamlit as st
import pandas as pd
from datetime import date
from typing import List, Optional

from src.models.experiment import Experiment, FilterCriteria
from src.services.storage import load_experiments
from src.services.visualization import (
    create_timeline_chart,
    create_comparison_chart,
    create_distribution_chart,
    create_circle_distribution_chart,
    filter_experiments,
    get_experiment_summary_stats
)


def render_experiment_details(experiment: Experiment) -> None:
    """Render detailed view of an experiment matching the form structure."""
    st.divider()
    
    # Experiment Details Section
    st.subheader("Experiment Details")
    col1, col2 = st.columns(2)
    with col1:
        if experiment.display_name:
            st.markdown(f"**Display Name:** {experiment.display_name}")
        st.markdown(f"**Lead Name:** {experiment.lead_name}")
        st.markdown(f"**Circle:** {experiment.circle}")
    with col2:
        st.markdown(f"**Start Date:** {experiment.start_date}")
        if experiment.end_date:
            st.markdown(f"**End Date:** {experiment.end_date}")
        else:
            st.markdown("**End Date:** Not specified")
        st.markdown(f"**Created At:** {experiment.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    # Question/Problem Statement Section
    st.subheader("Question/Problem Statement")
    st.markdown(experiment.problem_statement)
    
    # Baseline Statement Section
    st.subheader("Baseline Statement")
    st.markdown(experiment.baseline_statement)
    
    # Purpose/Objectives Section
    st.subheader("Purpose/Objectives")
    st.markdown(experiment.purpose_objectives)
    
    # Design and Execution Section
    st.subheader("Design and Execution")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"**Who Was Involved:** {experiment.who_was_involved}")
    with col2:
        st.markdown(f"**Group Size:** {experiment.group_size}")
    st.markdown(f"**Method Description:**")
    st.markdown(experiment.method_description)
    
    # Evaluation and Outcome Section
    st.subheader("Evaluation and Outcome")
    st.markdown(f"**Success Criteria:**")
    st.markdown(experiment.success_criteria)
    st.markdown(f"**Analysis Approach:**")
    st.markdown(experiment.analysis_approach)
    st.markdown(f"**Evaluation Plan:**")
    st.markdown(experiment.evaluation_plan)
    
    st.divider()


def experiments_to_dataframe(experiments: List[Experiment]) -> pd.DataFrame:
    """
    Convert a list of experiments to a pandas DataFrame for table display.
    
    Args:
        experiments: List of Experiment models
        
    Returns:
        pd.DataFrame: DataFrame with key experiment fields
    """
    data = []
    for exp in experiments:
        data.append({
            "Display Name": exp.display_name or "",
            "Lead Name": exp.lead_name,
            "Circle": exp.circle,
            "Start Date": exp.start_date.strftime("%Y-%m-%d"),
            "End Date": exp.end_date.strftime("%Y-%m-%d") if exp.end_date else "",
            "Group Size": exp.group_size,
            "Created": exp.created_at.strftime("%Y-%m-%d"),
        })
    
    df = pd.DataFrame(data)
    return df


def render_dashboard() -> None:
    """Render the dashboard page with visualizations."""
    st.title("CRISP Analysis Dashboard")
    st.markdown("View and analyze your CRISP experiments following the CRISP-DM methodology.")
    
    # Educational content
    with st.expander("📚 Understanding Your CRISP-DM Experiments", expanded=False):
        st.markdown("""
        The dashboard visualizes experiments structured by CRISP-DM principles:
        
        - **Summary Statistics** - Overview of your data science project portfolio
        - **Data Table** - Quick reference of all experiments with key metrics
        - **Experiment Details** - Full documentation of each experiment's CRISP-DM phases
        - **Visualizations** - Timeline, comparisons, and distributions to identify patterns
        
        **Sample Data**: The 10 sample experiments demonstrate various CRISP-DM scenarios:
        - Different problem types (accuracy, engagement, performance, etc.)
        - Various circles/teams applying the methodology
        - Different time periods showing project evolution
        - Varied group sizes and methodologies
        
        Use filters to explore specific experiments and identify trends in your data science work.
        """)

    # Load experiments
    try:
        experiments = load_experiments()
    except Exception as e:
        st.error(f"Error loading experiments: {str(e)}")
        return

    # Auto-initialize sample data if no experiments exist or if any have blank display names
    needs_regeneration = False
    has_blank_display_names = False
    
    if not experiments:
        needs_regeneration = True
    else:
        # Check if any experiments have blank display names
        blank_display_names = [exp for exp in experiments if not exp.display_name or exp.display_name.strip() == ""]
        if blank_display_names:
            needs_regeneration = True
            has_blank_display_names = True
    
    if needs_regeneration:
        from src.services.sample_data import load_sample_data
        try:
            load_sample_data()
            if has_blank_display_names:
                st.info("📊 Sample data has been regenerated to ensure all display names are populated.")
            else:
                st.info("📊 Sample data has been automatically loaded. The dashboard now contains 10 sample experiments.")
            # Reload experiments after initialization
            experiments = load_experiments()
            st.rerun()
        except Exception as e:
            st.error(f"Error initializing sample data: {str(e)}")
            st.info("💡 **Tip**: Use the navigation links in the top-left sidebar to go to the **Form** page to submit your first experiment.")
            return

    # Filters section
    st.sidebar.header("Filters")
    
    # Circle filter
    all_circles = sorted(set(exp.circle for exp in experiments))
    selected_circles = st.sidebar.multiselect("Filter by Circle", all_circles, default=all_circles)
    
    # Date range filter
    if experiments:
        min_date = min(exp.start_date for exp in experiments)
        max_date = max(exp.start_date for exp in experiments)
        date_range = st.sidebar.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        if isinstance(date_range, tuple) and len(date_range) == 2:
            date_start, date_end = date_range
        else:
            date_start, date_end = None, None
    else:
        date_start, date_end = None, None
    
    # Lead name filter
    all_leads = sorted(set(exp.lead_name for exp in experiments))
    selected_leads = st.sidebar.multiselect("Filter by Lead Name", all_leads, default=all_leads)
    
    # Apply filters
    filter_criteria = FilterCriteria(
        circles=selected_circles if selected_circles else None,
        date_range_start=date_start,
        date_range_end=date_end,
        lead_names=selected_leads if selected_leads else None
    )
    
    filtered_experiments = filter_experiments(experiments, filter_criteria)
    
    # Summary statistics
    st.header("Summary Statistics")
    stats = get_experiment_summary_stats(filtered_experiments)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Experiments", stats["total_count"])
    with col2:
        st.metric("Average Group Size", stats["avg_group_size"])
    with col3:
        if stats["date_range"]["start"]:
            st.metric("Earliest Start", stats["date_range"]["start"])
    with col4:
        if stats["date_range"]["end"]:
            st.metric("Latest End", stats["date_range"]["end"])
    
    # Data table section
    st.header("Data")
    st.markdown("View all experiments in a compact table format.")
    
    if filtered_experiments:
        # Convert experiments to DataFrame
        df = experiments_to_dataframe(filtered_experiments)
        
        # Display table with options
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Display Name": st.column_config.TextColumn(
                    "Display Name",
                    width="medium",
                ),
                "Lead Name": st.column_config.TextColumn(
                    "Lead Name",
                    width="medium",
                ),
                "Circle": st.column_config.TextColumn(
                    "Circle",
                    width="small",
                ),
                "Start Date": st.column_config.TextColumn(
                    "Start Date",
                    width="small",
                ),
                "End Date": st.column_config.TextColumn(
                    "End Date",
                    width="small",
                ),
                "Group Size": st.column_config.NumberColumn(
                    "Group Size",
                    width="small",
                ),
                "Created": st.column_config.TextColumn(
                    "Created",
                    width="small",
                ),
            }
        )
        
        # Show count
        st.caption(f"Showing {len(filtered_experiments)} of {len(experiments)} total experiments")
    else:
        st.info("No experiments match the current filters. Adjust filters to see data in the table.")
    
    # Experiment detail view
    st.header("Experiment Details")
    st.markdown("Browse through individual experiment details below.")
    
    # Create experiment selection dropdown
    if filtered_experiments:
        experiment_detail_options = {
            f"{exp.display_name or exp.lead_name} - {exp.start_date} ({exp.circle})": exp.id
            for exp in filtered_experiments
        }
        selected_detail_key = st.selectbox(
            "Select an experiment to view details",
            options=[""] + list(experiment_detail_options.keys()),
            index=0,
            help="Choose an experiment to view its complete details"
        )
        
        if selected_detail_key:
            selected_detail_id = experiment_detail_options[selected_detail_key]
            selected_experiment = next(
                (exp for exp in filtered_experiments if exp.id == selected_detail_id),
                None
            )
            
            if selected_experiment:
                render_experiment_details(selected_experiment)
    else:
        st.info("No experiments match the current filters. Adjust filters to see experiment details.")
    
    # Experiment list/timeline display
    st.header("Experiments")
    
    # Experiment selection
    experiment_options = {
        f"{exp.display_name or exp.lead_name} - {exp.start_date}": exp.id
        for exp in filtered_experiments
    }
    selected_experiment_ids = st.multiselect(
        "Select experiments to compare",
        options=list(experiment_options.keys()),
        default=[]
    )
    
    selected_experiments = [
        exp for exp in filtered_experiments
        if experiment_options.get(f"{exp.display_name or exp.lead_name} - {exp.start_date}") in [
            experiment_options[key] for key in selected_experiment_ids
        ]
    ]
    
    # Visualizations
    st.header("Visualizations")
    
    # Timeline chart
    st.subheader("Timeline")
    timeline_fig = create_timeline_chart(filtered_experiments)
    st.plotly_chart(timeline_fig, use_container_width=True)
    
    # Comparison chart (if experiments selected)
    if selected_experiments:
        st.subheader("Comparison")
        comparison_fig = create_comparison_chart(selected_experiments, metric="group_size", group_by="circle")
        st.plotly_chart(comparison_fig, use_container_width=True)
    
    # Distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Group Size Distribution")
        group_size_fig = create_distribution_chart(filtered_experiments, field="group_size")
        st.plotly_chart(group_size_fig, use_container_width=True)
    
    with col2:
        st.subheader("Circle Distribution")
        circle_fig = create_circle_distribution_chart(filtered_experiments)
        st.plotly_chart(circle_fig, use_container_width=True)

