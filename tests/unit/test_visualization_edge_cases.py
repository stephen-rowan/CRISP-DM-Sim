"""Unit tests for visualization service edge cases."""

import pytest
from datetime import date

from src.models.experiment import Experiment, FilterCriteria
from src.services.visualization import (
    create_timeline_chart,
    create_comparison_chart,
    create_distribution_chart,
    create_circle_distribution_chart,
    filter_experiments,
    get_experiment_summary_stats
)


def create_sample_experiment(lead_name: str, circle: str, start_date: date, group_size: int = 10, end_date: date = None) -> Experiment:
    """Helper to create a sample experiment."""
    return Experiment(
        lead_name=lead_name,
        circle=circle,
        start_date=start_date,
        end_date=end_date,
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


def test_create_timeline_chart_single_experiment():
    """Test timeline chart with single experiment."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1))
    ]
    
    fig = create_timeline_chart(experiments)
    assert fig is not None
    assert len(fig.data) > 0


def test_create_comparison_chart_empty():
    """Test comparison chart with empty experiments."""
    fig = create_comparison_chart([], metric="group_size")
    assert fig is not None


def test_create_comparison_chart_single_experiment():
    """Test comparison chart with single experiment."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=15)
    ]
    
    fig = create_comparison_chart(experiments, metric="group_size")
    assert fig is not None


def test_create_distribution_chart_empty():
    """Test distribution chart with empty experiments."""
    fig = create_distribution_chart([], field="group_size")
    assert fig is not None


def test_create_distribution_chart_single_value():
    """Test distribution chart with single value."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=10),
        create_sample_experiment("Jane Smith", "Data Science", date(2025, 2, 1), group_size=10),
    ]
    
    fig = create_distribution_chart(experiments, field="group_size")
    assert fig is not None


def test_create_circle_distribution_chart_single_circle():
    """Test circle distribution chart with single circle."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1)),
        create_sample_experiment("Jane Smith", "Data Science", date(2025, 2, 1)),
    ]
    
    fig = create_circle_distribution_chart(experiments)
    assert fig is not None


def test_filter_experiments_no_filters():
    """Test filtering with no filter criteria."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1)),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 2, 1)),
    ]
    
    filters = FilterCriteria()
    filtered = filter_experiments(experiments, filters)
    
    assert len(filtered) == 2


def test_filter_experiments_partial_date_range():
    """Test filtering with only start date."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1)),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 6, 1)),
    ]
    
    filters = FilterCriteria(date_range_start=date(2025, 5, 1))
    filtered = filter_experiments(experiments, filters)
    
    assert len(filtered) == 1
    assert filtered[0].lead_name == "Jane Smith"


def test_filter_experiments_only_end_date():
    """Test filtering with only end date."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1)),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 6, 1)),
    ]
    
    filters = FilterCriteria(date_range_end=date(2025, 3, 1))
    filtered = filter_experiments(experiments, filters)
    
    assert len(filtered) == 1
    assert filtered[0].lead_name == "John Doe"


def test_get_experiment_summary_stats_with_end_dates():
    """Test summary stats with experiments that have end dates."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=10, end_date=date(2025, 3, 31)),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 2, 1), group_size=15, end_date=date(2025, 4, 30)),
    ]
    
    stats = get_experiment_summary_stats(experiments)
    
    assert stats["total_count"] == 2
    assert stats["avg_group_size"] == 12.5
    assert stats["date_range"]["end"] is not None


def test_get_experiment_summary_stats_no_end_dates():
    """Test summary stats with experiments without end dates."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=10),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 2, 1), group_size=15),
    ]
    
    stats = get_experiment_summary_stats(experiments)
    
    assert stats["total_count"] == 2
    assert stats["date_range"]["end"] is None  # No end dates


def test_filter_experiments_multiple_criteria():
    """Test filtering with multiple criteria (AND logic)."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1)),
        create_sample_experiment("Jane Smith", "Data Science", date(2025, 6, 1)),
        create_sample_experiment("Bob Wilson", "Engineering", date(2025, 3, 1)),
    ]
    
    filters = FilterCriteria(
        circles=["Data Science"],
        date_range_start=date(2025, 5, 1),
        lead_names=["Jane Smith"]
    )
    filtered = filter_experiments(experiments, filters)
    
    assert len(filtered) == 1
    assert filtered[0].lead_name == "Jane Smith"


def test_create_comparison_chart_unknown_metric():
    """Test comparison chart with unknown metric."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=10)
    ]
    
    fig = create_comparison_chart(experiments, metric="unknown_metric")
    assert fig is not None


def test_create_comparison_chart_unknown_group_by():
    """Test comparison chart with unknown group_by value."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=10)
    ]
    
    fig = create_comparison_chart(experiments, metric="group_size", group_by="unknown_field")
    assert fig is not None


def test_create_distribution_chart_unknown_field():
    """Test distribution chart with unknown field."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1))
    ]
    
    fig = create_distribution_chart(experiments, field="unknown_field")
    assert fig is not None
    # Should show "No data for field" message


def test_create_timeline_chart_with_metrics_parameter():
    """Test timeline chart with metrics parameter."""
    experiments = [
        create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=10),
        create_sample_experiment("Jane Smith", "Engineering", date(2025, 2, 1), group_size=15),
    ]
    
    fig = create_timeline_chart(experiments, metrics=["group_size"])
    assert fig is not None

