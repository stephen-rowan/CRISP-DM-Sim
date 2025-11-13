"""Unit tests for Experiment model validation."""

import pytest
from datetime import date
from uuid import UUID

from src.models.experiment import Experiment, FilterCriteria


def test_experiment_creation_with_required_fields():
    """Test creating an experiment with all required fields."""
    experiment = Experiment(
        lead_name="John Doe",
        circle="Data Science",
        start_date=date(2025, 1, 1),
        problem_statement="Test problem",
        baseline_statement="Test baseline",
        purpose_objectives="Test objectives",
        who_was_involved="Test team",
        group_size=10,
        method_description="Test method",
        success_criteria="Test criteria",
        analysis_approach="Test approach",
        evaluation_plan="Test plan"
    )
    
    assert experiment.lead_name == "John Doe"
    assert experiment.circle == "Data Science"
    assert isinstance(experiment.id, UUID)
    assert experiment.group_size == 10


def test_experiment_optional_fields():
    """Test creating an experiment with optional fields."""
    experiment = Experiment(
        display_name="Test Experiment",
        lead_name="Jane Smith",
        circle="Engineering",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 3, 31),
        problem_statement="Test problem",
        baseline_statement="Test baseline",
        purpose_objectives="Test objectives",
        who_was_involved="Test team",
        group_size=15,
        method_description="Test method",
        success_criteria="Test criteria",
        analysis_approach="Test approach",
        evaluation_plan="Test plan"
    )
    
    assert experiment.display_name == "Test Experiment"
    assert experiment.end_date == date(2025, 3, 31)


def test_experiment_end_date_validation():
    """Test that end_date must be >= start_date."""
    with pytest.raises(ValueError, match="end_date must be >= start_date"):
        Experiment(
            lead_name="John Doe",
            circle="Data Science",
            start_date=date(2025, 3, 31),
            end_date=date(2025, 1, 1),  # Invalid: before start_date
            problem_statement="Test problem",
            baseline_statement="Test baseline",
            purpose_objectives="Test objectives",
            who_was_involved="Test team",
            group_size=10,
            method_description="Test method",
            success_criteria="Test criteria",
            analysis_approach="Test approach",
            evaluation_plan="Test plan"
        )


def test_experiment_group_size_validation():
    """Test that group_size must be >= 1."""
    with pytest.raises(ValueError):
        Experiment(
            lead_name="John Doe",
            circle="Data Science",
            start_date=date(2025, 1, 1),
            problem_statement="Test problem",
            baseline_statement="Test baseline",
            purpose_objectives="Test objectives",
            who_was_involved="Test team",
            group_size=0,  # Invalid: must be >= 1
            method_description="Test method",
            success_criteria="Test criteria",
            analysis_approach="Test approach",
            evaluation_plan="Test plan"
        )


def test_experiment_character_limits():
    """Test character limit validation."""
    with pytest.raises(ValueError):
        Experiment(
            lead_name="a" * 201,  # Exceeds max_length=200
            circle="Data Science",
            start_date=date(2025, 1, 1),
            problem_statement="Test problem",
            baseline_statement="Test baseline",
            purpose_objectives="Test objectives",
            who_was_involved="Test team",
            group_size=10,
            method_description="Test method",
            success_criteria="Test criteria",
            analysis_approach="Test approach",
            evaluation_plan="Test plan"
        )


def test_experiment_whitespace_trimming():
    """Test that whitespace is trimmed from text fields."""
    experiment = Experiment(
        lead_name="  John Doe  ",
        circle="  Data Science  ",
        start_date=date(2025, 1, 1),
        problem_statement="  Test problem  ",
        baseline_statement="Test baseline",
        purpose_objectives="Test objectives",
        who_was_involved="Test team",
        group_size=10,
        method_description="Test method",
        success_criteria="Test criteria",
        analysis_approach="Test approach",
        evaluation_plan="Test plan"
    )
    
    assert experiment.lead_name == "John Doe"
    assert experiment.circle == "Data Science"
    assert experiment.problem_statement == "Test problem"


def test_filter_criteria_creation():
    """Test creating FilterCriteria."""
    filters = FilterCriteria(
        circles=["Data Science", "Engineering"],
        date_range_start=date(2025, 1, 1),
        date_range_end=date(2025, 12, 31),
        lead_names=["John Doe", "Jane Smith"]
    )
    
    assert filters.circles == ["Data Science", "Engineering"]
    assert filters.date_range_start == date(2025, 1, 1)
    assert filters.date_range_end == date(2025, 12, 31)
    assert filters.lead_names == ["John Doe", "Jane Smith"]


def test_filter_criteria_optional_fields():
    """Test FilterCriteria with optional fields."""
    filters = FilterCriteria()
    
    assert filters.circles is None
    assert filters.date_range_start is None
    assert filters.date_range_end is None
    assert filters.lead_names is None

