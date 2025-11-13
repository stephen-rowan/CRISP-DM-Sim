"""Integration tests for comparative analysis flow."""

import pytest
import tempfile
from pathlib import Path
from datetime import date
from unittest.mock import patch

from src.models.experiment import Experiment, FilterCriteria
from src.services.storage import EXPERIMENTS_FILE, save_experiments, load_experiments
from src.services.visualization import (
    filter_experiments,
    create_comparison_chart,
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


def test_comparative_analysis_flow(tmp_path):
    """Test complete comparative analysis flow: load -> filter -> display."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        # Create multiple experiments
        experiments = [
            create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=10),
            create_sample_experiment("Jane Smith", "Engineering", date(2025, 2, 1), group_size=15),
            create_sample_experiment("Bob Wilson", "Data Science", date(2025, 3, 1), group_size=20),
            create_sample_experiment("Alice Brown", "Engineering", date(2025, 4, 1), group_size=12),
        ]
        
        # Save experiments
        save_experiments(experiments)
        
        # Load experiments
        loaded = load_experiments()
        assert len(loaded) == 4
        
        # Filter by circle
        filters = FilterCriteria(circles=["Data Science"])
        filtered = filter_experiments(loaded, filters)
        assert len(filtered) == 2
        assert all(exp.circle == "Data Science" for exp in filtered)
        
        # Create comparison chart
        comparison_fig = create_comparison_chart(filtered, metric="group_size", group_by="circle")
        assert comparison_fig is not None
        
        # Get summary statistics
        stats = get_experiment_summary_stats(filtered)
        assert stats["total_count"] == 2
        assert stats["avg_group_size"] == 15.0


def test_filter_and_compare_multiple_experiments(tmp_path):
    """Test filtering and comparing multiple experiments."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        # Create experiments with varied data
        experiments = [
            create_sample_experiment("John Doe", "Data Science", date(2025, 1, 1), group_size=10),
            create_sample_experiment("Jane Smith", "Data Science", date(2025, 2, 1), group_size=15),
            create_sample_experiment("Bob Wilson", "Engineering", date(2025, 3, 1), group_size=20),
            create_sample_experiment("Alice Brown", "Engineering", date(2025, 4, 1), group_size=12),
            create_sample_experiment("Charlie Davis", "Product", date(2025, 5, 1), group_size=18),
        ]
        
        save_experiments(experiments)
        loaded = load_experiments()
        
        # Filter by date range
        filters = FilterCriteria(
            date_range_start=date(2025, 2, 1),
            date_range_end=date(2025, 4, 1)
        )
        filtered = filter_experiments(loaded, filters)
        assert len(filtered) == 3
        
        # Compare filtered experiments
        comparison_fig = create_comparison_chart(filtered, metric="group_size", group_by="circle")
        assert comparison_fig is not None
        
        # Verify statistics
        stats = get_experiment_summary_stats(filtered)
        assert stats["total_count"] == 3
        assert "Data Science" in stats["circles"]
        assert "Engineering" in stats["circles"]

