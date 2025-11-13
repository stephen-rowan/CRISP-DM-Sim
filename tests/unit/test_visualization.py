"""Unit tests for Visualization Service."""

import pytest
from datetime import date
from typing import List

from src.models.experiment import Experiment, FilterCriteria
from src.services.visualization import (
    create_timeline_chart,
    create_comparison_chart,
    create_distribution_chart,
    create_circle_distribution_chart,
    filter_experiments,
    get_experiment_summary_stats
)


def create_sample_experiment(lead_name: str, circle: str, start_date: date, group_size: int = 10) -> Experiment:
    """Helper to create a sample experiment."""
    return Experiment(
        lead_name=lead_name,
        circle=circle,
        start_date=start_date,
        problem_statement="Test problem",
        baseline_statement="Test baseline",
        purpose_objectives="Test objectives",
        who_was_involved="Test team",
        group_size=group_size,
        method_description="Test method",
        success_criteria="Test criteria",
        analysis_approach="Test approach",
        evaluation_plan="Test plan"
    )


def test_create_timeline_chart_empty():
    """Test timeline chart with empty experiments."""
    fig = create_timeline_chart([])
    assert fig is not None


def test_create_timeline_chart_with_data():
    """Test timeline chart with experiment data."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1)),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 2, 1)),
    ]
    
    fig = create_timeline_chart(experiments)
    assert fig is not None
    assert len(fig.data) > 0


def test_create_comparison_chart():
    """Test comparison chart creation."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=10),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 2, 1), group_size=15),
    ]
    
    fig = create_comparison_chart(experiments, metric="group_size", group_by="circle")
    assert fig is not None


def test_create_distribution_chart():
    """Test distribution chart creation."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=10),
        create_sample_experiment("Jane Smith", "Data Science", date(2025, 2, 1), group_size=15),
    ]
    
    fig = create_distribution_chart(experiments, field="group_size")
    assert fig is not None


def test_create_circle_distribution_chart():
    """Test circle distribution chart creation."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1)),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 2, 1)),
        create_sample_experiment("Bob Wilson", "Data Science", date(2025, 3, 1)),
    ]
    
    fig = create_circle_distribution_chart(experiments)
    assert fig is not None


def test_filter_experiments_by_circle():
    """Test filtering experiments by circle."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1)),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 2, 1)),
        create_sample_experiment("Bob Wilson", "Data Science", date(2025, 3, 1)),
    ]
    
    filters = FilterCriteria(circles=["Data Science"])
    filtered = filter_experiments(experiments, filters)
    
    assert len(filtered) == 2
    assert all(exp.circle == "Data Science" for exp in filtered)


def test_filter_experiments_by_date_range():
    """Test filtering experiments by date range."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1)),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 6, 1)),
        create_sample_experiment("Bob Wilson", "Data Science", date(2025, 12, 1)),
    ]
    
    filters = FilterCriteria(
        date_range_start=date(2025, 5, 1),
        date_range_end=date(2025, 7, 1)
    )
    filtered = filter_experiments(experiments, filters)
    
    assert len(filtered) == 1
    assert filtered[0].lead_name == "Jane Smith"


def test_filter_experiments_by_lead_name():
    """Test filtering experiments by lead name."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1)),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 2, 1)),
        create_sample_experiment("Bob Wilson", "Data Science", date(2025, 3, 1)),
    ]
    
    filters = FilterCriteria(lead_names=["John Doe", "Bob Wilson"])
    filtered = filter_experiments(experiments, filters)
    
    assert len(filtered) == 2
    assert all(exp.lead_name in ["John Doe", "Bob Wilson"] for exp in filtered)


def test_get_experiment_summary_stats():
    """Test getting summary statistics."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=10),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 2, 1), group_size=15),
        create_sample_experiment("Bob Wilson", "Data Science", date(2025, 3, 1), group_size=20),
    ]
    
    stats = get_experiment_summary_stats(experiments)
    
    assert stats["total_count"] == 3
    assert stats["avg_group_size"] == 15.0
    assert "Data Science" in stats["circles"]
    assert stats["circles"]["Data Science"] == 2
    assert stats["circles"]["Engineering"] == 1


def test_get_experiment_summary_stats_empty():
    """Test summary statistics with empty experiments."""
    stats = get_experiment_summary_stats([])
    
    assert stats["total_count"] == 0
    assert stats["avg_group_size"] == 0
    assert stats["circles"] == {}

