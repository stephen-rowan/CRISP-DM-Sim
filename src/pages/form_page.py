"""Form page for submitting CRISP experiments."""

import streamlit as st
from datetime import date
from typing import Optional, Tuple, List

from src.models.experiment import Experiment
from src.services.storage import save_experiment


def render_form() -> Optional[Experiment]:
    """
    Render the Streamlit form interface and handle form submission.

    Returns:
        Optional[Experiment]: Experiment model if form was submitted and validated, None otherwise
    """
    st.title("CRISP Experiment Form")
    st.markdown("Complete the form below to submit a new CRISP experiment following the CRISP-DM methodology.")
    
    # Educational content
    with st.expander("📚 About CRISP-DM Form Sections", expanded=False):
        st.markdown("""
        This form aligns with CRISP-DM phases:
        
        - **Experiment Details** - Project metadata and team information
        - **Question/Problem Statement** - Business Understanding phase: What problem are we solving?
        - **Baseline Statement** - Data Understanding phase: What is the current state?
        - **Purpose/Objectives** - Business Understanding phase: What are our goals?
        - **Design and Execution** - Data Preparation & Modeling phases: How will we approach this?
        - **Evaluation and Outcome** - Evaluation & Deployment phases: How will we measure success?
        
        Each field helps document your data science experiment following industry best practices.
        """)

    with st.form("experiment_form"):
        # Experiment Details Section
        st.header("Experiment Details")
        display_name = st.text_input("Display Name (optional)", max_chars=200, help="User-friendly name for identification")
        lead_name = st.text_input("Lead Name *", max_chars=200, help="Name of the experiment lead")
        circle = st.text_input("Circle *", max_chars=100, help="Circle/team name")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date *", value=date.today())
        with col2:
            end_date = st.date_input("End Date (optional)", value=None)

        # Question/Problem Statement Section
        st.header("Question/Problem Statement")
        problem_statement = st.text_area(
            "Problem Statement *",
            max_chars=5000,
            help="Describe the problem or question being addressed"
        )

        # Baseline Statement Section
        st.header("Baseline Statement")
        baseline_statement = st.text_area(
            "Baseline Statement *",
            max_chars=5000,
            help="Describe the current state or baseline"
        )

        # Purpose/Objectives Section
        st.header("Purpose/Objectives")
        purpose_objectives = st.text_area(
            "Purpose/Objectives *",
            max_chars=5000,
            help="Describe the goals and objectives of the experiment"
        )

        # Design and Execution Section
        st.header("Design and Execution")
        who_was_involved = st.text_input(
            "Who Was Involved *",
            max_chars=1000,
            help="Description of who was involved in the experiment"
        )
        group_size = st.number_input(
            "Group Size *",
            min_value=1,
            value=1,
            help="Number of people in the experiment group"
        )
        method_description = st.text_area(
            "Method Description *",
            max_chars=5000,
            help="Describe the method used in the experiment"
        )

        # Evaluation and Outcome Section
        st.header("Evaluation and Outcome")
        success_criteria = st.text_area(
            "Success Criteria *",
            max_chars=5000,
            help="Define the success criteria for the experiment"
        )
        analysis_approach = st.text_area(
            "Analysis Approach *",
            max_chars=5000,
            help="Describe the analysis approach used"
        )
        evaluation_plan = st.text_area(
            "Evaluation Plan *",
            max_chars=5000,
            help="Describe the evaluation plan"
        )

        submitted = st.form_submit_button("Submit Experiment")

        if submitted:
            # Collect form data
            form_data = {
                "display_name": display_name.strip() if display_name else None,
                "lead_name": lead_name.strip(),
                "circle": circle.strip(),
                "start_date": start_date,
                "end_date": end_date,
                "problem_statement": problem_statement.strip(),
                "baseline_statement": baseline_statement.strip(),
                "purpose_objectives": purpose_objectives.strip(),
                "who_was_involved": who_was_involved.strip(),
                "group_size": group_size,
                "method_description": method_description.strip(),
                "success_criteria": success_criteria.strip(),
                "analysis_approach": analysis_approach.strip(),
                "evaluation_plan": evaluation_plan.strip(),
            }

            # Validate form data
            is_valid, errors = validate_form_data(form_data)

            if not is_valid:
                # Display validation errors
                st.error("Please correct the following errors:")
                for error in errors:
                    st.error(f"• {error}")
                return None

            # Create experiment from form data
            try:
                experiment = create_experiment_from_form(form_data)
                
                # Save experiment
                save_experiment(experiment)
                
                st.success("Experiment saved successfully!")
                st.balloons()
                
                # Offer navigation to dashboard
                if st.button("View Dashboard"):
                    st.switch_page("pages/2_Dashboard.py")
                
                return experiment
            except Exception as e:
                st.error(f"Error saving experiment: {str(e)}")
                return None

    return None


def validate_form_data(form_data: dict) -> Tuple[bool, List[str]]:
    """
    Validate form data dictionary against Experiment schema.

    Args:
        form_data: Dictionary of form field values

    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_error_messages)
    """
    errors = []

    # Required field checks
    required_fields = [
        "lead_name", "circle", "start_date", "problem_statement",
        "baseline_statement", "purpose_objectives", "who_was_involved",
        "group_size", "method_description", "success_criteria",
        "analysis_approach", "evaluation_plan"
    ]

    for field in required_fields:
        value = form_data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"{field.replace('_', ' ').title()} is required")

    # Date validation
    if form_data.get("start_date") and form_data.get("end_date"):
        if form_data["end_date"] < form_data["start_date"]:
            errors.append("End date must be >= start date")

    # Group size validation
    if form_data.get("group_size") is not None:
        if form_data["group_size"] < 1:
            errors.append("Group size must be >= 1")

    # Character limit checks (handled by Streamlit, but double-check)
    text_fields = {
        "display_name": 200,
        "lead_name": 200,
        "circle": 100,
        "problem_statement": 5000,
        "baseline_statement": 5000,
        "purpose_objectives": 5000,
        "who_was_involved": 1000,
        "method_description": 5000,
        "success_criteria": 5000,
        "analysis_approach": 5000,
        "evaluation_plan": 5000,
    }

    for field, max_length in text_fields.items():
        value = form_data.get(field)
        if value and isinstance(value, str) and len(value) > max_length:
            errors.append(f"{field.replace('_', ' ').title()} exceeds maximum length of {max_length} characters")

    return len(errors) == 0, errors


def create_experiment_from_form(form_data: dict) -> Experiment:
    """
    Create Experiment Pydantic model from validated form data.

    Args:
        form_data: Validated form data dictionary

    Returns:
        Experiment: Pydantic Experiment model

    Raises:
        ValidationError: If form_data doesn't pass Pydantic validation
    """
    # Create experiment (Pydantic will add id and created_at automatically)
    experiment = Experiment(**form_data)
    return experiment

