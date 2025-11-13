"""Unit tests for storage service datetime parsing edge cases."""

import pytest
import json
from pathlib import Path
from datetime import date, datetime
from unittest.mock import patch

from src.services.storage import _load_experiments_impl, EXPERIMENTS_FILE


def test_load_experiments_with_timezone_datetime(tmp_path):
    """Test loading experiments with timezone-aware datetime strings."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        experiment_data = [{
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2025-01-27T10:30:00Z",  # With Z timezone
            "lead_name": "John Doe",
            "circle": "Data Science",
            "start_date": "2025-01-01",
            "end_date": "2025-03-31",
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
        
        experiments = _load_experiments_impl()
        assert len(experiments) == 1
        assert isinstance(experiments[0].created_at, datetime)


def test_load_experiments_with_non_timezone_datetime(tmp_path):
    """Test loading experiments with datetime strings without timezone."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        experiment_data = [{
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2025-01-27T10:30:00",  # Without timezone
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
        
        experiments = _load_experiments_impl()
        assert len(experiments) == 1
        assert isinstance(experiments[0].created_at, datetime)


def test_load_experiments_with_uuid_already_uuid(tmp_path):
    """Test loading experiments where id is already UUID object."""
    with patch('src.services.storage.EXPERIMENTS_FILE', tmp_path / "experiments.json"):
        from uuid import UUID, uuid4
        
        exp_id = uuid4()
        experiment_data = [{
            "id": str(exp_id),  # String UUID
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
        
        experiments = _load_experiments_impl()
        assert len(experiments) == 1
        assert experiments[0].id == exp_id

