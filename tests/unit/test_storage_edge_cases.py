"""Unit tests for storage service edge cases and error handling."""

import pytest
import json
from pathlib import Path
from datetime import date
from unittest.mock import patch, mock_open
from uuid import UUID

from src.models.experiment import Experiment
from src.services.storage import (
    _load_experiments_impl,
    save_experiment,
    save_experiments,
    experiment_exists,
    get_experiment_by_id,
    EXPERIMENTS_FILE
)


def test_load_experiments_with_invalid_experiment_skips_it(tmp_path):
    """Test that invalid experiments are skipped during load."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        # Create file with one valid and one invalid experiment
        experiment_data = [
            {
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
            },
            {
                "id": "invalid-uuid",
                "created_at": "invalid-date",
                "lead_name": "",  # Invalid: empty
                "circle": "Data Science",
                "start_date": "2025-01-01",
                "problem_statement": "Test",
                "baseline_statement": "Test",
                "purpose_objectives": "Test",
                "who_was_involved": "Test",
                "group_size": 10,
                "method_description": "Test",
                "success_criteria": "Test",
                "analysis_approach": "Test",
                "evaluation_plan": "Test"
            }
        ]
        
        (tmp_path / "experiments.json").write_text(json.dumps(experiment_data))
        
        experiments = _load_experiments_impl()
        # Should only load the valid experiment
        assert len(experiments) == 1
        assert experiments[0].lead_name == "John Doe"


def test_save_experiment_creates_directory(tmp_path):
    """Test that save_experiment creates directory if it doesn't exist."""
    test_file = tmp_path / "subdir" / "experiments.json"
    with patch('src.services.storage.EXPERIMENTS_FILE', test_file):
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
        
        # Directory should be created
        assert test_file.parent.exists()
        assert test_file.exists()


def test_save_experiment_validation_error():
    """Test that save_experiment raises ValidationError for invalid experiment."""
    with pytest.raises(Exception):  # Should raise ValidationError
        save_experiment("not an experiment")  # type: ignore


def test_experiment_exists_with_empty_file(tmp_path):
    """Test experiment_exists with empty file."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        (tmp_path / "experiments.json").write_text("[]")
        
        from uuid import uuid4
        assert experiment_exists(uuid4()) is False


def test_get_experiment_by_id_with_empty_file(tmp_path):
    """Test get_experiment_by_id with empty file."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        (tmp_path / "experiments.json").write_text("[]")
        
        from uuid import uuid4
        assert get_experiment_by_id(uuid4()) is None


def test_save_experiments_with_empty_list(tmp_path):
    """Test saving empty list of experiments."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        save_experiments([])
        
        experiments = _load_experiments_impl()
        assert len(experiments) == 0


def test_save_experiments_validation_error():
    """Test that save_experiments raises ValidationError for invalid experiments."""
    with pytest.raises(Exception):  # Should raise ValidationError
        save_experiments(["not an experiment"])  # type: ignore


def test_save_experiment_with_none_end_date(tmp_path):
    """Test saving experiment with None end_date doesn't try to isoformat it."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        experiment = Experiment(
            lead_name="John Doe",
            circle="Data Science",
            start_date=date(2025, 1, 1),
            end_date=None,  # Explicitly None
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
        
        # Verify it was saved correctly
        experiments = _load_experiments_impl()
        assert len(experiments) == 1
        assert experiments[0].end_date is None


def test_save_experiments_with_none_end_dates(tmp_path):
    """Test saving multiple experiments with None end_dates."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        experiments = [
            Experiment(
                lead_name=f"Lead {i}",
                circle="Data Science",
                start_date=date(2025, 1, 1),
                end_date=None,
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
            for i in range(2)
        ]
        
        save_experiments(experiments)
        
        loaded = _load_experiments_impl()
        assert len(loaded) == 2
        assert all(exp.end_date is None for exp in loaded)

