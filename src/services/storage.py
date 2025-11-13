"""Storage service for experiment data persistence to JSON file."""

import json
import os
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from pydantic import ValidationError

from src.models.experiment import Experiment

# File path for experiments storage (relative to project root)
# Get project root (parent of src directory)
# __file__ is src/services/storage.py, so:
# parent = src/services, parent.parent = src, parent.parent.parent = project root
_project_root = Path(__file__).parent.parent.parent
EXPERIMENTS_FILE = _project_root / "data" / "experiments.json"

# Try to import streamlit for caching (optional)
# Disable caching in test environments
import sys
import os
IN_TEST = (
    'pytest' in sys.modules or 
    'unittest' in sys.modules or
    os.environ.get('PYTEST_CURRENT_TEST') is not None
)

try:
    import streamlit as st
    # Only enable caching if we're actually in a Streamlit runtime (not in tests)
    # In tests, always disable caching to avoid cache pollution
    HAS_STREAMLIT = not IN_TEST
except ImportError:
    HAS_STREAMLIT = False


def _load_experiments_impl() -> List[Experiment]:
    """
    Load all experiments from the JSON file.

    Returns:
        List[Experiment]: List of Experiment Pydantic models

    Raises:
        FileNotFoundError: If file doesn't exist (creates empty file)
        JSONDecodeError: If JSON file is corrupted
        ValidationError: If any experiment doesn't match Experiment schema
    """
    # Create data directory if it doesn't exist
    EXPERIMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Create empty file if it doesn't exist
    if not EXPERIMENTS_FILE.exists():
        EXPERIMENTS_FILE.write_text("[]")
        return []

    try:
        with open(EXPERIMENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        # Handle corrupted JSON - log error and return empty list
        print(f"Warning: Invalid JSON in {EXPERIMENTS_FILE}: {e}")
        return []

    # Validate and convert to Experiment models
    experiments = []
    for item in data:
        try:
            # Convert UUID strings and datetime strings
            if 'id' in item and isinstance(item['id'], str):
                item['id'] = UUID(item['id'])
            if 'created_at' in item and isinstance(item['created_at'], str):
                from datetime import datetime
                # Handle both with and without timezone
                dt_str = item['created_at'].replace('Z', '+00:00')
                try:
                    item['created_at'] = datetime.fromisoformat(dt_str)
                except ValueError:
                    # Fallback for formats without timezone
                    item['created_at'] = datetime.fromisoformat(item['created_at'])
            if 'start_date' in item and isinstance(item['start_date'], str):
                from datetime import date
                item['start_date'] = date.fromisoformat(item['start_date'])
            if 'end_date' in item and item['end_date'] is not None and isinstance(item['end_date'], str):
                from datetime import date
                item['end_date'] = date.fromisoformat(item['end_date'])

            experiment = Experiment(**item)
            experiments.append(experiment)
        except (ValidationError, ValueError, KeyError) as e:
            # Skip invalid experiments, log warning
            print(f"Warning: Skipping invalid experiment: {e}")
            continue

    return experiments


# Add caching if Streamlit is available and running (not in tests)
# In test environments, caching is disabled to avoid cache pollution
if HAS_STREAMLIT:
    @st.cache_data(ttl=60, show_spinner=False)
    def load_experiments() -> List[Experiment]:
        """Load experiments with Streamlit caching enabled."""
        return _load_experiments_impl()
else:
    # In tests or when Streamlit is not available, use implementation directly
    def load_experiments() -> List[Experiment]:
        """Load experiments without caching."""
        return _load_experiments_impl()


def save_experiment(experiment: Experiment) -> None:
    """
    Save a new experiment to the JSON file.

    Args:
        experiment: Pydantic Experiment model to save

    Raises:
        ValidationError: If experiment doesn't pass Pydantic validation
        IOError: If file write fails
        OSError: If directory creation fails
    """
    # Validate experiment
    if not isinstance(experiment, Experiment):
        raise ValidationError("experiment must be an Experiment instance")

    # Create data directory if it doesn't exist
    EXPERIMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Clear cache if using Streamlit caching
    if HAS_STREAMLIT and hasattr(load_experiments, 'clear'):
        load_experiments.clear()

    # Load existing experiments (use implementation directly to avoid cache)
    experiments = _load_experiments_impl()

    # Append new experiment
    experiments.append(experiment)

    # Write to temporary file first (atomic write)
    temp_file = EXPERIMENTS_FILE.with_suffix('.json.tmp')
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            # Convert to JSON-serializable format
            json_data = []
            for exp in experiments:
                exp_dict = exp.model_dump()
                # Convert UUID and datetime to strings
                exp_dict['id'] = str(exp_dict['id'])
                exp_dict['created_at'] = exp_dict['created_at'].isoformat()
                exp_dict['start_date'] = exp_dict['start_date'].isoformat()
                if exp_dict['end_date']:
                    exp_dict['end_date'] = exp_dict['end_date'].isoformat()
                json_data.append(exp_dict)
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        # Atomic rename
        temp_file.replace(EXPERIMENTS_FILE)
    except (IOError, OSError) as e:
        # Clean up temp file on error
        if temp_file.exists():
            temp_file.unlink()
        raise IOError(f"Failed to save experiment: {e}") from e


def save_experiments(experiments: List[Experiment]) -> None:
    """
    Save multiple experiments to the JSON file (replaces all existing data).

    Args:
        experiments: List of Experiment models to save

    Raises:
        ValidationError: If any experiment doesn't pass validation
        IOError: If file write fails
        OSError: If directory creation fails
    """
    # Validate all experiments
    for experiment in experiments:
        if not isinstance(experiment, Experiment):
            raise ValidationError(f"Invalid experiment: {experiment}")

    # Create data directory if it doesn't exist
    EXPERIMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Clear cache if using Streamlit caching
    if HAS_STREAMLIT and hasattr(load_experiments, 'clear'):
        load_experiments.clear()

    # Write to temporary file first (atomic write)
    temp_file = EXPERIMENTS_FILE.with_suffix('.json.tmp')
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            # Convert to JSON-serializable format
            json_data = []
            for exp in experiments:
                exp_dict = exp.model_dump()
                # Convert UUID and datetime to strings
                exp_dict['id'] = str(exp_dict['id'])
                exp_dict['created_at'] = exp_dict['created_at'].isoformat()
                exp_dict['start_date'] = exp_dict['start_date'].isoformat()
                if exp_dict['end_date']:
                    exp_dict['end_date'] = exp_dict['end_date'].isoformat()
                json_data.append(exp_dict)
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        # Atomic rename
        temp_file.replace(EXPERIMENTS_FILE)
    except (IOError, OSError) as e:
        # Clean up temp file on error
        if temp_file.exists():
            temp_file.unlink()
        raise IOError(f"Failed to save experiments: {e}") from e


def experiment_exists(experiment_id: UUID) -> bool:
    """
    Check if an experiment with the given ID exists.

    Args:
        experiment_id: Experiment ID to check

    Returns:
        bool: True if experiment exists, False otherwise
    """
    try:
        experiments = load_experiments()
        return any(exp.id == experiment_id for exp in experiments)
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def get_experiment_by_id(experiment_id: UUID) -> Optional[Experiment]:
    """
    Retrieve a single experiment by ID.

    Args:
        experiment_id: Experiment ID to retrieve

    Returns:
        Optional[Experiment]: Experiment if found, None otherwise
    """
    try:
        experiments = load_experiments()
        for exp in experiments:
            if exp.id == experiment_id:
                return exp
        return None
    except (FileNotFoundError, json.JSONDecodeError):
        return None

