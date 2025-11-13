"""Integration tests for sample data generation flow."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from src.services.storage import EXPERIMENTS_FILE, load_experiments
from src.services.sample_data import generate_sample_experiments, load_sample_data


def test_generate_sample_experiments():
    """Test generating sample experiments."""
    experiments = generate_sample_experiments(count=5)
    
    assert len(experiments) == 5
    assert all(isinstance(exp, type(experiments[0])) for exp in experiments)
    
    # Verify all experiments have valid data
    for exp in experiments:
        assert exp.lead_name
        assert exp.circle
        assert exp.group_size >= 1
        assert exp.problem_statement


def test_generate_sample_experiments_varied_data():
    """Test that generated experiments have varied data."""
    experiments = generate_sample_experiments(count=10)
    
    # Check for variety in circles
    circles = set(exp.circle for exp in experiments)
    assert len(circles) > 1  # Should have multiple circles
    
    # Check for variety in group sizes
    group_sizes = [exp.group_size for exp in experiments]
    assert min(group_sizes) != max(group_sizes)  # Should have different sizes


def test_load_sample_data_flow(tmp_path):
    """Test complete sample data generation and loading flow."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        # Generate and save sample data
        load_sample_data()
        
        # Verify data was saved
        experiments = load_experiments()
        assert len(experiments) == 10
        
        # Verify experiments are valid
        for exp in experiments:
            assert exp.lead_name
            assert exp.circle
            assert exp.group_size >= 1


def test_load_sample_data_replaces_existing(tmp_path):
    """Test that load_sample_data replaces existing data."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        # Generate first batch
        load_sample_data()
        first_batch = load_experiments()
        assert len(first_batch) == 10
        
        # Generate second batch (should replace first)
        load_sample_data()
        second_batch = load_experiments()
        assert len(second_batch) == 10
        
        # Verify they're different (different IDs)
        first_ids = {exp.id for exp in first_batch}
        second_ids = {exp.id for exp in second_batch}
        # IDs should be different (new experiments generated)
        assert first_ids != second_ids or len(first_ids) == 5

