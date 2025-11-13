"""Unit tests for form validation logic."""

import pytest
from datetime import date

from src.pages.form_page import validate_form_data, create_experiment_from_form


def test_validate_form_data_character_limits():
    """Test form validation with character limit violations."""
    form_data = {
        "lead_name": "a" * 201,  # Exceeds 200
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
    assert any("Lead Name" in error and "200" in error for error in errors)


def test_validate_form_data_group_size_zero():
    """Test form validation with group size = 0."""
    form_data = {
        "lead_name": "John Doe",
        "circle": "Data Science",
        "start_date": date(2025, 1, 1),
        "problem_statement": "Test problem",
        "baseline_statement": "Test baseline",
        "purpose_objectives": "Test objectives",
        "who_was_involved": "Test team",
        "group_size": 0,  # Invalid
        "method_description": "Test method",
        "success_criteria": "Test criteria",
        "analysis_approach": "Test approach",
        "evaluation_plan": "Test plan"
    }
    
    is_valid, errors = validate_form_data(form_data)
    assert is_valid is False
    assert any("Group size" in error for error in errors)


def test_validate_form_data_all_character_limits():
    """Test all character limit validations."""
    long_string_5001 = "a" * 5001
    
    form_data = {
        "lead_name": "John Doe",
        "circle": "Data Science",
        "start_date": date(2025, 1, 1),
        "problem_statement": long_string_5001,  # Exceeds 5000
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
    assert any("Problem Statement" in error and "5000" in error for error in errors)


def test_create_experiment_from_form_with_all_fields():
    """Test creating experiment from form with all fields including optional."""
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
        "group_size": 15,
        "method_description": "Test method",
        "success_criteria": "Test criteria",
        "analysis_approach": "Test approach",
        "evaluation_plan": "Test plan"
    }
    
    experiment = create_experiment_from_form(form_data)
    assert experiment.display_name == "Test Experiment"
    assert experiment.end_date == date(2025, 3, 31)
    assert experiment.group_size == 15


def test_create_experiment_from_form_without_optional_fields():
    """Test creating experiment from form without optional fields."""
    form_data = {
        "lead_name": "Jane Smith",
        "circle": "Engineering",
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
    
    experiment = create_experiment_from_form(form_data)
    assert experiment.display_name is None
    assert experiment.end_date is None
    assert experiment.lead_name == "Jane Smith"

