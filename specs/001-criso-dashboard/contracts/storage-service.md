# Storage Service Contract

**Service**: Experiment Data Persistence  
**Type**: Local JSON File Storage  
**File**: `src/services/storage.py`

## Overview

The Storage Service handles reading and writing experiment data to/from a local JSON file. It provides a simple interface for persisting and retrieving experiment data.

## Interface

### `load_experiments() -> List[Experiment]`

**Description**: Loads all experiments from the JSON file.

**Returns**: 
- `List[Experiment]`: List of Experiment Pydantic models

**Raises**:
- `FileNotFoundError`: If `data/experiments.json` doesn't exist (should create empty file)
- `JSONDecodeError`: If JSON file is corrupted or invalid
- `ValidationError`: If any experiment in JSON doesn't match Experiment schema

**Behavior**:
- If file doesn't exist, creates empty array `[]` and returns empty list
- Validates each experiment against Experiment Pydantic model
- Skips invalid experiments (logs error, continues loading valid ones)
- Returns empty list if file is empty or contains only invalid data

**Example**:
```python
experiments = load_experiments()
# Returns: [Experiment(...), Experiment(...), ...]
```

---

### `save_experiment(experiment: Experiment) -> None`

**Description**: Saves a new experiment to the JSON file.

**Parameters**:
- `experiment` (Experiment): Pydantic Experiment model to save

**Returns**: None

**Raises**:
- `ValidationError`: If experiment doesn't pass Pydantic validation
- `IOError`: If file write fails (disk full, permission error, file locked)
- `OSError`: If directory creation fails

**Behavior**:
- Loads existing experiments
- Appends new experiment to list
- Writes entire array back to file (atomic write via temp file + rename)
- Creates `data/` directory if it doesn't exist
- Creates `data/experiments.json` if it doesn't exist

**Error Handling**:
- On write failure: Raises IOError with descriptive message
- Preserves existing data (doesn't overwrite on failure)
- Uses temporary file + atomic rename for safe writes

**Example**:
```python
new_experiment = Experiment(
    lead_name="Jane Smith",
    circle="Engineering",
    start_date=date(2025, 1, 1),
    # ... other fields
)
save_experiment(new_experiment)
```

---

### `save_experiments(experiments: List[Experiment]) -> None`

**Description**: Saves multiple experiments to the JSON file (replaces all existing data).

**Parameters**:
- `experiments` (List[Experiment]): List of Experiment models to save

**Returns**: None

**Raises**:
- `ValidationError`: If any experiment doesn't pass validation
- `IOError`: If file write fails
- `OSError`: If directory creation fails

**Behavior**:
- Validates all experiments before writing
- Replaces entire file contents (used for sample data generation)
- Uses atomic write (temp file + rename)

**Example**:
```python
sample_experiments = generate_sample_experiments()  # Returns List[Experiment]
save_experiments(sample_experiments)
```

---

### `experiment_exists(experiment_id: UUID) -> bool`

**Description**: Checks if an experiment with the given ID exists.

**Parameters**:
- `experiment_id` (UUID): Experiment ID to check

**Returns**:
- `bool`: True if experiment exists, False otherwise

**Raises**:
- `FileNotFoundError`: If file doesn't exist (returns False)
- `JSONDecodeError`: If JSON is corrupted (returns False)

**Example**:
```python
exists = experiment_exists(UUID("550e8400-e29b-41d4-a716-446655440000"))
```

---

### `get_experiment_by_id(experiment_id: UUID) -> Optional[Experiment]`

**Description**: Retrieves a single experiment by ID.

**Parameters**:
- `experiment_id` (UUID): Experiment ID to retrieve

**Returns**:
- `Optional[Experiment]`: Experiment if found, None otherwise

**Raises**:
- `FileNotFoundError`: If file doesn't exist (returns None)
- `JSONDecodeError`: If JSON is corrupted (returns None)

**Example**:
```python
experiment = get_experiment_by_id(UUID("550e8400-e29b-41d4-a716-446655440000"))
if experiment:
    print(experiment.lead_name)
```

## File Structure

**File Path**: `data/experiments.json` (relative to project root)

**Format**: JSON array of experiment objects

**Initialization**: Empty array `[]` if file doesn't exist

## Error Handling Strategy

1. **File Not Found**: Create empty file, return empty list/None
2. **Invalid JSON**: Log error, return empty list/None (don't crash)
3. **Invalid Experiment Data**: Skip invalid entries, log warning, continue with valid data
4. **Write Failures**: Raise IOError with clear message, preserve existing data
5. **Permission Errors**: Raise IOError with descriptive message

## Thread Safety

**Note**: Streamlit runs in a single-threaded environment by default. No explicit locking needed for MVP. If multi-user access is added later, file locking should be implemented.

## Performance Considerations

- **Read Operations**: Load entire file into memory (acceptable for < 50 experiments)
- **Write Operations**: Atomic write via temp file + rename (prevents corruption)
- **Caching**: Consider Streamlit caching for `load_experiments()` to avoid repeated file reads

