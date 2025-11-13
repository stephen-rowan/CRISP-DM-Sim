"""Integration tests for form submission flow."""

import pytest
import tempfile
from pathlib import Path
from datetime import date
from unittest.mock import patch

from src.models.experiment import Experiment
from src.services.storage import EXPERIMENTS_FILE, save_experiment, load_experiments
from src.pages.form_page import validate_form_data, create_experiment_from_form


def test_form_validation_valid_data():
    """Test form validation with valid data."""
    form_data = {
        "lead_name": "John Doe",
        "circle": "Data Science",
        "start_date": date(2025, 1, 1),
        "end_date": date(2025, 3, 31),
        "problem_statement": "Test problem",
        "baseline_statement": "Test baseline",
        "purpose_objectives": "Test objectives",
        "who_was_involved": "Test team",
        "group_size": 10,
        "method_description": "Test method",
        "success_criteria": "Test criteria",
        "analysis_approach": "Test approach",
        "evaluation_plan": "Test plan"
    }
    
    is_valid, errors = validate_form_data(form_data)
    assert is_valid is True
    assert len(errors) == 0


def test_form_validation_missing_required_field():
    """Test form validation with missing required field."""
    form_data = {
        "lead_name": "",  # Missing required field
        "circle": "Data Science",
        "start_date": date(2025, 1, 1),
        "problem_statement": "Test problem",
        "baseline_statement": "Test baseline",
        "purpose_objectives": "Test objectives",
        "who_was_involved": "Test team",
        "group_size": 10,
        "method_description": "Test method",
        "success_criteria": "Test criteria",
        "analysis_approach": "Test approach",
        "evaluation_plan": "Test plan"
    }
    
    is_valid, errors = validate_form_data(form_data)
    assert is_valid is False
    assert len(errors) > 0
    assert any("Lead Name" in error for error in errors)


def test_form_validation_invalid_date_range():
    """Test form validation with invalid date range."""
    form_data = {
        "lead_name": "John Doe",
        "circle": "Data Science",
        "start_date": date(2025, 3, 31),
        "end_date": date(2025, 1, 1),  # Invalid: before start_date
        "problem_statement": "Test problem",
        "baseline_statement": "Test baseline",
        "purpose_objectives": "Test objectives",
        "who_was_involved": "Test team",
        "group_size": 10,
        "method_description": "Test method",
        "success_criteria": "Test criteria",
        "analysis_approach": "Test approach",
        "evaluation_plan": "Test plan"
    }
    
    is_valid, errors = validate_form_data(form_data)
    assert is_valid is False
    assert any("End date" in error for error in errors)


def test_create_experiment_from_form(tmp_path):
    """Test creating experiment from form data."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        form_data = {
            "display_name": "Test Experiment",
            "lead_name": "John Doe",
            "circle": "Data Science",
            "start_date": date(2025, 1, 1),
            "end_date": date(2025, 3, 31),
            "problem_statement": "Test problem",
            "baseline_statement": "Test baseline",
            "purpose_objectives": "Test objectives",
            "who_was_involved": "Test team",
            "group_size": 10,
            "method_description": "Test method",
            "success_criteria": "Test criteria",
            "analysis_approach": "Test approach",
            "evaluation_plan": "Test plan"
        }
        
        experiment = create_experiment_from_form(form_data)
        
        assert isinstance(experiment, Experiment)
        assert experiment.lead_name == "John Doe"
        assert experiment.circle == "Data Science"
        assert experiment.display_name == "Test Experiment"


def test_form_submission_flow(tmp_path):
    """Test complete form submission flow: validation -> creation -> save."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        form_data = {
            "lead_name": "Jane Smith",
            "circle": "Engineering",
            "start_date": date(2025, 1, 1),
            "problem_statement": "Test problem",
            "baseline_statement": "Test baseline",
            "purpose_objectives": "Test objectives",
            "who_was_involved": "Test team",
            "group_size": 15,
            "method_description": "Test method",
            "success_criteria": "Test criteria",
            "analysis_approach": "Test approach",
            "evaluation_plan": "Test plan"
        }
        
        # Validate
        is_valid, errors = validate_form_data(form_data)
        assert is_valid is True
        
        # Create experiment
        experiment = create_experiment_from_form(form_data)
        assert isinstance(experiment, Experiment)
        
        # Save
        save_experiment(experiment)
        
        # Verify saved
        experiments = load_experiments()
        assert len(experiments) == 1
        assert experiments[0].lead_name == "Jane Smith"
        assert experiments[0].circle == "Engineering"

