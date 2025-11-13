"""Experiment data model using Pydantic for validation."""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from uuid import UUID, uuid4
from datetime import date, datetime, timezone
from typing import Optional, List


class Experiment(BaseModel):
    """Represents a single CRISP experiment submission with all form data and metadata."""

    model_config = ConfigDict()

    id: UUID = Field(default_factory=uuid4, description="Universally unique identifier for the experiment")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp when experiment was submitted")
    display_name: Optional[str] = Field(None, max_length=200, description="User-friendly name for identification")
    lead_name: str = Field(..., max_length=200, min_length=1, description="Name of the experiment lead")
    circle: str = Field(..., max_length=100, min_length=1, description="Circle/team name")
    start_date: date = Field(..., description="Experiment start date")
    end_date: Optional[date] = Field(None, description="Experiment end date (optional)")
    problem_statement: str = Field(..., max_length=5000, min_length=1, description="Problem/question statement")
    baseline_statement: str = Field(..., max_length=5000, min_length=1, description="Baseline statement")
    purpose_objectives: str = Field(..., max_length=5000, min_length=1, description="Purpose and objectives")
    who_was_involved: str = Field(..., max_length=1000, min_length=1, description="Description of who was involved")
    group_size: int = Field(..., ge=1, description="Number of people in the experiment group")
    method_description: str = Field(..., max_length=5000, min_length=1, description="Method description")
    success_criteria: str = Field(..., max_length=5000, min_length=1, description="Success criteria")
    analysis_approach: str = Field(..., max_length=5000, min_length=1, description="Analysis approach")
    evaluation_plan: str = Field(..., max_length=5000, min_length=1, description="Evaluation plan")

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v: Optional[date], info) -> Optional[date]:
        """Validate that end_date is >= start_date if both are provided."""
        if v is not None:
            # In Pydantic v2, access data via info.data
            if hasattr(info, 'data') and 'start_date' in info.data:
                start_date = info.data['start_date']
                if v < start_date:
                    raise ValueError('end_date must be >= start_date')
        return v

    @field_validator('lead_name', 'circle', 'problem_statement', 'baseline_statement', 
                     'purpose_objectives', 'who_was_involved', 'method_description',
                     'success_criteria', 'analysis_approach', 'evaluation_plan', mode='before')
    @classmethod
    def trim_whitespace(cls, v: str) -> str:
        """Trim whitespace from text fields."""
        if isinstance(v, str):
            return v.strip()
        return v


class FilterCriteria(BaseModel):
    """Filter criteria for dashboard filtering."""

    circles: Optional[List[str]] = Field(None, description="Filter by circle names")
    date_range_start: Optional[date] = Field(None, description="Start date for date range filter")
    date_range_end: Optional[date] = Field(None, description="End date for date range filter")
    lead_names: Optional[List[str]] = Field(None, description="Filter by lead names")

