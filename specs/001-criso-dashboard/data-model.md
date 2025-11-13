# Data Model: CRISP Analysis Dashboard

**Date**: 2025-01-27  
**Phase**: Phase 1 - Design & Contracts  
**Source**: Feature specification entities and requirements

## Overview

The data model for the CRISP Analysis Dashboard consists of three main entities: Experiment (core data entity), Dashboard View (visualization state), and Visualization (chart representation). The model uses Pydantic for validation and follows the JSON storage structure defined in research.md.

## Core Entities

### 1. Experiment

**Description**: Represents a single CRISP experiment submission with all form data and metadata.

**Attributes**:

| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| `id` | UUID (string) | Yes | Valid UUID v4 format | Universally unique identifier for the experiment |
| `created_at` | ISO-8601 timestamp (string) | Yes | Valid ISO-8601 format | Timestamp when experiment was submitted |
| `display_name` | string | No | Max 200 characters, optional | User-friendly name for identification |
| `lead_name` | string | Yes | Non-empty, max 200 characters | Name of the experiment lead |
| `circle` | string | Yes | Non-empty, max 100 characters | Circle/team name |
| `start_date` | date (YYYY-MM-DD) | Yes | Valid date, required | Experiment start date |
| `end_date` | date (YYYY-MM-DD) or null | No | Valid date, must be >= start_date if provided | Experiment end date (optional) |
| `problem_statement` | string | Yes | Non-empty, max 5000 characters | Problem/question statement |
| `baseline_statement` | string | Yes | Non-empty, max 5000 characters | Baseline statement |
| `purpose_objectives` | string | Yes | Non-empty, max 5000 characters | Purpose and objectives |
| `who_was_involved` | string | Yes | Non-empty, max 1000 characters | Description of who was involved |
| `group_size` | integer | Yes | Positive integer (>= 1) | Number of people in the experiment group |
| `method_description` | string | Yes | Non-empty, max 5000 characters | Method description |
| `success_criteria` | string | Yes | Non-empty, max 5000 characters | Success criteria |
| `analysis_approach` | string | Yes | Non-empty, max 5000 characters | Analysis approach |
| `evaluation_plan` | string | Yes | Non-empty, max 5000 characters | Evaluation plan |

**Relationships**:
- One Experiment can be displayed in multiple Dashboard Views
- One Experiment can be represented in multiple Visualizations

**State Transitions**:
- **Created**: Experiment submitted via form → stored in JSON file
- **No state changes after creation** (as per spec: no editing/deletion in MVP)

**Validation Rules**:
1. All required fields must be present and non-empty (after trimming whitespace)
2. `end_date` must be >= `start_date` if both are provided
3. `group_size` must be a positive integer (>= 1)
4. Text fields must not exceed maximum character limits
5. `id` must be a valid UUID v4
6. `created_at` must be a valid ISO-8601 timestamp
7. Dates must be in YYYY-MM-DD format

**Pydantic Model Structure**:
```python
from pydantic import BaseModel, Field, field_validator
from uuid import UUID, uuid4
from datetime import date, datetime
from typing import Optional

class Experiment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    display_name: Optional[str] = Field(None, max_length=200)
    lead_name: str = Field(..., max_length=200, min_length=1)
    circle: str = Field(..., max_length=100, min_length=1)
    start_date: date
    end_date: Optional[date] = None
    problem_statement: str = Field(..., max_length=5000, min_length=1)
    baseline_statement: str = Field(..., max_length=5000, min_length=1)
    purpose_objectives: str = Field(..., max_length=5000, min_length=1)
    who_was_involved: str = Field(..., max_length=1000, min_length=1)
    group_size: int = Field(..., ge=1)
    method_description: str = Field(..., max_length=5000, min_length=1)
    success_criteria: str = Field(..., max_length=5000, min_length=1)
    analysis_approach: str = Field(..., max_length=5000, min_length=1)
    evaluation_plan: str = Field(..., max_length=5000, min_length=1)
    
    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, info):
        if v is not None and 'start_date' in info.data:
            if v < info.data['start_date']:
                raise ValueError('end_date must be >= start_date')
        return v
```

### 2. Dashboard View

**Description**: Represents the visualization state of the dashboard, including selected experiments and filter criteria.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `selected_experiments` | List[UUID] | Yes | List of experiment IDs currently selected for visualization |
| `active_visualizations` | List[str] | Yes | List of visualization types currently displayed (e.g., ["timeline", "comparison"]) |
| `filter_criteria` | FilterCriteria | No | Current filter settings (circle, date range, etc.) |
| `time_range` | TimeRange | No | Selected time range for visualization |

**Relationships**:
- Many-to-many with Experiment (via selected_experiments)
- One-to-many with Visualization (one view can have multiple visualizations)

**State Transitions**:
- **Initial**: Empty selection, default visualizations
- **Filtered**: User applies filters → view updates
- **Selected**: User selects experiments → view updates
- **No persistence**: Dashboard view state is session-based (not stored)

**FilterCriteria Structure**:
```python
class FilterCriteria(BaseModel):
    circles: Optional[List[str]] = None  # Filter by circle names
    date_range_start: Optional[date] = None
    date_range_end: Optional[date] = None
    lead_names: Optional[List[str]] = None  # Filter by lead names
```

**Note**: Dashboard View is a transient entity (not persisted). It represents the current state of the user's dashboard session.

### 3. Visualization

**Description**: Represents a specific chart or visual representation of experiment data.

**Attributes**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `visualization_type` | string | Yes | Type of visualization (e.g., "timeline", "bar_chart", "comparison", "distribution") |
| `data_source` | List[UUID] | Yes | Experiment IDs used as data source |
| `metrics_displayed` | List[str] | Yes | Metrics shown in visualization (e.g., ["group_size", "experiment_count"]) |
| `time_range` | TimeRange | No | Time range for visualization data |
| `chart_config` | dict | No | Visualization-specific configuration (colors, axes, etc.) |

**Relationships**:
- Many-to-many with Experiment (via data_source)
- Belongs to Dashboard View (via active_visualizations)

**Visualization Types** (from SC-005: at least 3 distinct types):

1. **Timeline**: Shows experiments over time (x-axis: date, y-axis: experiment count or metrics)
2. **Comparison Chart**: Compares metrics across selected experiments (bar chart, grouped bars)
3. **Distribution Chart**: Shows distribution of metrics (e.g., group size distribution, circle distribution)

**Note**: Visualization is a transient entity (not persisted). It represents the current chart configuration and is regenerated on each dashboard render.

## Data Storage Structure

### JSON File Format

The experiments are stored in a single JSON array in `data/experiments.json`:

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-01-27T10:30:00Z",
    "display_name": "Q1 Experiment",
    "lead_name": "John Doe",
    "circle": "Data Science",
    "start_date": "2025-01-01",
    "end_date": "2025-03-31",
    "problem_statement": "How can we improve model accuracy?",
    "baseline_statement": "Current accuracy is 85%",
    "purpose_objectives": "Increase accuracy to 90%",
    "who_was_involved": "Data team, Engineering team",
    "group_size": 15,
    "method_description": "A/B testing with new features",
    "success_criteria": "Accuracy >= 90%",
    "analysis_approach": "Statistical significance testing",
    "evaluation_plan": "Weekly reviews, monthly reports"
  }
]
```

### Data Access Patterns

1. **Read All Experiments**: Load entire JSON array
2. **Filter Experiments**: Filter in-memory after loading
3. **Add Experiment**: Load array, append new experiment, write back
4. **No Update/Delete**: Not supported in MVP (per spec)

## Data Validation Flow

1. **Form Submission**: User fills form → Form data dictionary
2. **Pydantic Validation**: Dictionary → Pydantic Experiment model (validates all rules)
3. **Metadata Addition**: Add `id` (UUID) and `created_at` (timestamp)
4. **Storage**: Serialize to JSON, append to array, write to file
5. **Load**: Deserialize JSON → Validate with Pydantic → Return list of Experiment models

## Data Quality Constraints

From research.md Data Quality Assessment:

- **Completeness**: 100% required field completion (enforced by validation)
- **Correctness**: 
  - Date logic: end_date >= start_date
  - Group size: positive integer
  - Text fields: non-empty after trimming
- **Consistency**: 
  - UUID format validation
  - ISO-8601 timestamp format
  - YYYY-MM-DD date format
- **Character Limits**: Enforced per field (see attribute table above)

## Relationships Summary

```
Experiment (1) ──< (many) Dashboard View (via selected_experiments)
Experiment (1) ──< (many) Visualization (via data_source)
Dashboard View (1) ──< (many) Visualization (via active_visualizations)
```

**Note**: Dashboard View and Visualization are transient (session-based), only Experiment is persisted.

