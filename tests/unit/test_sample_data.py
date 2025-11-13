"""Unit tests for Sample Data Service."""

import pytest
from datetime import date, timedelta

from src.services.sample_data import generate_realistic_experiment, generate_sample_experiments, load_sample_data
from src.models.experiment import Experiment


def test_generate_realistic_experiment():
    """Test generating a single realistic experiment."""
    experiment = generate_realistic_experiment(
        circle="Data Science",
        start_date=date(2025, 1, 1),
        lead_name="John Doe"
    )
    
    assert isinstance(experiment, Experiment)
    assert experiment.circle == "Data Science"
    assert experiment.start_date == date(2025, 1, 1)
    assert experiment.lead_name == "John Doe"
    assert experiment.group_size >= 1
    assert experiment.end_date is not None
    assert experiment.end_date >= experiment.start_date


def test_generate_realistic_experiment_valid_dates():
    """Test that generated experiment has valid date logic."""
    experiment = generate_realistic_experiment(
        circle="Engineering",
        start_date=date(2025, 1, 1),
        lead_name="Jane Smith"
    )
    
    # End date should be after start date
    assert experiment.end_date >= experiment.start_date
    # End date should be within reasonable range (1-3 months)
    days_diff = (experiment.end_date - experiment.start_date).days
    assert 30 <= days_diff <= 90


def test_generate_realistic_experiment_coherent_text():
    """Test that generated experiment has coherent text fields."""
    experiment = generate_realistic_experiment(
        circle="Product",
        start_date=date(2025, 1, 1),
        lead_name="Bob Wilson"
    )
    
    # All text fields should be non-empty
    assert experiment.problem_statement
    assert experiment.baseline_statement
    assert experiment.purpose_objectives
    assert experiment.who_was_involved
    assert experiment.method_description
    assert experiment.success_criteria
    assert experiment.analysis_approach
    assert experiment.evaluation_plan


def test_generate_sample_experiments_count():
    """Test generating correct count of sample experiments."""
    experiments = generate_sample_experiments(count=5)
    
    assert len(experiments) == 5
    assert all(isinstance(exp, Experiment) for exp in experiments)


def test_generate_sample_experiments_all_valid():
    """Test that all generated experiments pass validation."""
    experiments = generate_sample_experiments(count=10)
    
    for exp in experiments:
        # All should be valid Experiment instances
        assert isinstance(exp, Experiment)
        # All should have valid dates
        assert exp.start_date is not None
        if exp.end_date:
            assert exp.end_date >= exp.start_date
        # All should have valid group size
        assert exp.group_size >= 1


def test_generate_sample_experiments_varied_data():
    """Test that generated experiments have varied data."""
    experiments = generate_sample_experiments(count=10)
    
    # Check for variety in circles
    circles = set(exp.circle for exp in experiments)
    assert len(circles) > 1  # Should have multiple circles
    
    # Check for variety in group sizes
    group_sizes = [exp.group_size for exp in experiments]
    assert min(group_sizes) != max(group_sizes)  # Should have different sizes
    
    # Check for variety in dates
    start_dates = [exp.start_date for exp in experiments]
    assert min(start_dates) != max(start_dates)  # Should span different dates


def test_load_sample_data(tmp_path, monkeypatch):
    """Test loading sample data (replaces existing data)."""
    import src.services.sample_data as sample_data_module
    from pathlib import Path
    
    # Patch the EXPERIMENTS_FILE path
    test_file = tmp_path / "experiments.json"
    original_file = sample_data_module.save_experiments.__globals__['EXPERIMENTS_FILE']
    
    # Temporarily patch
    monkeypatch.setattr('src.services.storage.EXPERIMENTS_FILE', test_file)
    
    # Generate and save sample data
    load_sample_data()
    
    # Verify file was created
    assert test_file.exists()
    
    # Verify data was saved (10 experiments)
    from src.services.storage import load_experiments
    experiments = load_experiments()
    assert len(experiments) == 10
    
    # Restore original
    monkeypatch.setattr('src.services.storage.EXPERIMENTS_FILE', original_file)

