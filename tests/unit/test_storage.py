"""Unit tests for Storage Service."""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import date
from unittest.mock import patch, mock_open

from src.models.experiment import Experiment
from src.services.storage import (
    load_experiments,
    save_experiment,
    save_experiments,
    experiment_exists,
    get_experiment_by_id,
    EXPERIMENTS_FILE
)


def test_load_experiments_empty_file(tmp_path):
    """Test loading experiments from empty file."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        # Create empty file
        (tmp_path / "experiments.json").write_text("[]")
        
        experiments = load_experiments()
        assert experiments == []


def test_load_experiments_valid_data(tmp_path):
    """Test loading experiments with valid data."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        # Create file with valid experiment data
        experiment_data = [{
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2025-01-27T10:30:00",
            "lead_name": "John Doe",
            "circle": "Data Science",
            "start_date": "2025-01-01",
            "end_date": None,
            "problem_statement": "Test problem",
            "baseline_statement": "Test baseline",
            "purpose_objectives": "Test objectives",
            "who_was_involved": "Test team",
            "group_size": 10,
            "method_description": "Test method",
            "success_criteria": "Test criteria",
            "analysis_approach": "Test approach",
            "evaluation_plan": "Test plan"
        }]
        
        (tmp_path / "experiments.json").write_text(json.dumps(experiment_data))
        
        experiments = load_experiments()
        assert len(experiments) == 1
        assert experiments[0].lead_name == "John Doe"
        assert experiments[0].circle == "Data Science"


def test_load_experiments_corrupted_json(tmp_path):
    """Test loading experiments from corrupted JSON file."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        # Create file with invalid JSON
        (tmp_path / "experiments.json").write_text("{ invalid json }")
        
        experiments = load_experiments()
        assert experiments == []


def test_save_experiment(tmp_path):
    """Test saving a single experiment."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        experiment = Experiment(
            lead_name="Jane Smith",
            circle="Engineering",
            start_date=date(2025, 1, 1),
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
        
        save_experiment(experiment)
        
        # Verify file was created and contains the experiment
        assert (tmp_path / "experiments.json").exists()
        experiments = load_experiments()
        assert len(experiments) == 1
        assert experiments[0].lead_name == "Jane Smith"


def test_save_experiments(tmp_path):
    """Test saving multiple experiments."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        experiments = [
            Experiment(
                lead_name=f"Lead {i}",
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
            for i in range(3)
        ]
        
        save_experiments(experiments)
        
        # Verify all experiments were saved
        loaded = load_experiments()
        assert len(loaded) == 3
        assert all(exp.lead_name.startswith("Lead") for exp in loaded)


def test_experiment_exists(tmp_path):
    """Test checking if experiment exists."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        from uuid import uuid4
        
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
        
        save_experiment(experiment)
        
        # Check existing experiment
        assert experiment_exists(experiment.id) is True
        
        # Check non-existing experiment
        assert experiment_exists(uuid4()) is False


def test_get_experiment_by_id(tmp_path):
    """Test retrieving experiment by ID."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        experiment = Experiment(
            lead_name="Jane Smith",
            circle="Engineering",
            start_date=date(2025, 1, 1),
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
        
        save_experiment(experiment)
        
        # Retrieve existing experiment
        retrieved = get_experiment_by_id(experiment.id)
        assert retrieved is not None
        assert retrieved.lead_name == "Jane Smith"
        
        # Retrieve non-existing experiment
        from uuid import uuid4
        assert get_experiment_by_id(uuid4()) is None

