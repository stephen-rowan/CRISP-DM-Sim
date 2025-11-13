# Sample Data Service Contract

**Service**: Sample Experiment Data Generation  
**Type**: Data Generation Utility  
**File**: `src/services/sample_data.py`

## Overview

The Sample Data Service generates realistic sample experiment data for demonstration and testing purposes. It creates multiple experiments with varied data across different circles, time periods, and experiment types.

## Interface

### `generate_sample_experiments(count: int = 5) -> List[Experiment]`

**Description**: Generates a list of sample experiments with realistic data.

**Parameters**:
- `count` (int): Number of sample experiments to generate. Default: 5 (minimum per SC-006).

**Returns**:
- `List[Experiment]`: List of Experiment models with sample data

**Behavior**:
- Generates experiments with varied:
  - Circles (Data Science, Engineering, Product, Analytics, etc.)
  - Time periods (spanning different months/quarters)
  - Group sizes (varied realistic values)
  - Problem statements (diverse experiment types)
  - Lead names (varied names)
- All experiments pass validation (valid dates, required fields, etc.)
- Experiments have realistic relationships (e.g., related problem statements)

**Sample Data Characteristics**:
- **Circles**: Rotate through predefined list (Data Science, Engineering, Product, Analytics, Operations)
- **Dates**: Span last 6-12 months with varied start/end dates
- **Group Sizes**: Range from 5 to 30 people (realistic team sizes)
- **Problem Statements**: Varied topics (model accuracy, user engagement, cost reduction, etc.)
- **Lead Names**: Varied realistic names
- **Display Names**: Optional, some experiments have them, some don't

**Example**:
```python
sample_experiments = generate_sample_experiments(count=5)
# Returns: [Experiment(...), Experiment(...), ...] (5 experiments)
```

---

### `load_sample_data() -> None`

**Description**: Generates sample experiments and saves them to the JSON file (replaces existing data).

**Returns**: None

**Raises**:
- `IOError`: If file write fails

**Behavior**:
- Generates 5 sample experiments (per SC-006)
- Saves them using `save_experiments()` from storage service
- Replaces all existing data (as per user story US3)

**Warning**: This function replaces all existing experiment data. Should show confirmation in UI.

**Example**:
```python
load_sample_data()
# Generates and saves 5 sample experiments to data/experiments.json
```

---

### `generate_realistic_experiment(circle: str, start_date: date, lead_name: str) -> Experiment`

**Description**: Generates a single realistic experiment with specified parameters.

**Parameters**:
- `circle` (str): Circle name for the experiment
- `start_date` (date): Start date for the experiment
- `lead_name` (str): Lead name for the experiment

**Returns**:
- `Experiment`: Single Experiment model with realistic sample data

**Behavior**:
- Generates realistic text for all text fields
- Calculates appropriate end_date (typically 1-3 months after start_date)
- Generates realistic group_size (5-30 range)
- Creates coherent problem statement, baseline, objectives, etc.

**Use Case**: Used internally by `generate_sample_experiments()` to create individual experiments.

**Example**:
```python
experiment = generate_realistic_experiment(
    circle="Data Science",
    start_date=date(2025, 1, 1),
    lead_name="Jane Smith"
)
```

## Sample Data Templates

**Problem Statement Templates**:
- "How can we improve [metric] by [percentage]?"
- "What is the impact of [change] on [outcome]?"
- "Can we reduce [cost/time] while maintaining [quality]?"

**Baseline Statement Templates**:
- "Current [metric] is [value]"
- "Baseline performance shows [characteristic]"
- "Initial measurements indicate [finding]"

**Method Description Templates**:
- "A/B testing with [variation]"
- "Controlled experiment with [group] and [control]"
- "Observational study of [phenomenon]"

## Data Quality

All generated sample data:
- ✅ Passes Pydantic validation
- ✅ Has valid date logic (end_date >= start_date)
- ✅ Has realistic values (group sizes, dates, text lengths)
- ✅ Has varied content (not all identical)
- ✅ Includes optional fields (some experiments have display_name, some don't)

## Integration with UI

**User Story US3**: User can click "Generate Sample Data" button to populate dashboard.

**UI Flow**:
1. User clicks "Generate Sample Data" button
2. System shows confirmation dialog (warning: replaces existing data)
3. User confirms
4. System calls `load_sample_data()`
5. System shows success message
6. Dashboard refreshes with sample data

**Alternative Flow** (non-destructive):
- Generate sample data without replacing existing
- Append sample data to existing experiments
- Requires additional function: `append_sample_data(count: int) -> None`

## Testing Use Cases

Sample data generation is useful for:
- **Development**: Testing visualizations with varied data
- **Demonstration**: Showing dashboard capabilities to stakeholders
- **Testing**: Integration tests, UI tests
- **Onboarding**: Helping users understand expected data format

## Future Enhancements

- **Customizable Templates**: Allow users to define their own problem statement templates
- **Realistic Relationships**: Generate experiments that reference each other
- **Time Series Patterns**: Generate experiments with realistic temporal patterns
- **Export Templates**: Save/load sample data templates

