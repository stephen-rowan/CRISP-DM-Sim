# Form Service Contract

**Service**: Experiment Form Submission  
**Type**: Streamlit Form Interface  
**File**: `src/pages/form_page.py`

## Overview

The Form Service handles the CRISP experiment form interface, validation, and submission. It provides the user interface for entering experiment data and coordinates with the Storage Service to persist submissions.

## Interface

### `render_form() -> Optional[Experiment]`

**Description**: Renders the Streamlit form interface and handles form submission.

**Returns**: 
- `Optional[Experiment]`: Experiment model if form was submitted and validated, None otherwise

**Behavior**:
- Displays form with all CRISP template sections
- Validates required fields before submission
- Shows validation errors inline
- On successful submission: saves experiment and returns Experiment model
- On validation failure: displays errors and returns None

**Form Sections** (matching CRISP template):

1. **Experiment Details**:
   - Display name (optional text input)
   - Lead name (required text input)
   - Circle (required text input)
   - Start date (required date input)
   - End date (optional date input)

2. **Question/Problem Statement**:
   - Problem statement (required text area, max 5000 chars)

3. **Baseline Statement**:
   - Baseline statement (required text area, max 5000 chars)

4. **Purpose/Objectives**:
   - Purpose/objectives (required text area, max 5000 chars)

5. **Design and Execution**:
   - Who was involved (required text input, max 1000 chars)
   - Group size (required number input, min 1)
   - Method description (required text area, max 5000 chars)

6. **Evaluation and Outcome**:
   - Success criteria (required text area, max 5000 chars)
   - Analysis approach (required text area, max 5000 chars)
   - Evaluation plan (required text area, max 5000 chars)

**Validation Rules**:
- All required fields must be filled
- Text fields trimmed of whitespace
- Date validation: end_date >= start_date (if end_date provided)
- Group size must be >= 1
- Character limits enforced per field

**Error Display**:
- Inline error messages below invalid fields
- Summary of validation errors at top of form (if any)
- Clear indication of required vs optional fields

**Success Behavior**:
- Shows success message
- Optionally redirects to dashboard (or shows "View Dashboard" button)
- Clears form (or keeps data for review)

**Example Flow**:
```python
# In Streamlit page
experiment = render_form()
if experiment:
    st.success("Experiment saved successfully!")
    if st.button("View Dashboard"):
        st.switch_page("pages/dashboard_page.py")
```

---

### `validate_form_data(form_data: dict) -> Tuple[bool, List[str]]`

**Description**: Validates form data dictionary against Experiment schema.

**Parameters**:
- `form_data` (dict): Dictionary of form field values

**Returns**:
- `Tuple[bool, List[str]]`: (is_valid, list_of_error_messages)

**Behavior**:
- Validates all required fields present
- Validates field types and formats
- Validates business rules (date logic, positive numbers)
- Returns list of human-readable error messages

**Example**:
```python
form_data = {
    "lead_name": "John Doe",
    "circle": "Data Science",
    "start_date": "2025-01-01",
    "end_date": "2024-12-31",  # Invalid: before start_date
    # ... other fields
}
is_valid, errors = validate_form_data(form_data)
# Returns: (False, ["end_date must be >= start_date"])
```

---

### `create_experiment_from_form(form_data: dict) -> Experiment`

**Description**: Creates Experiment Pydantic model from validated form data.

**Parameters**:
- `form_data` (dict): Validated form data dictionary

**Returns**:
- `Experiment`: Pydantic Experiment model

**Raises**:
- `ValidationError`: If form_data doesn't pass Pydantic validation

**Behavior**:
- Adds metadata (UUID for id, current timestamp for created_at)
- Converts form data types (strings to dates, etc.)
- Creates and validates Experiment model

**Example**:
```python
form_data = {
    "display_name": "Q1 Experiment",
    "lead_name": "Jane Smith",
    "circle": "Engineering",
    "start_date": date(2025, 1, 1),
    # ... other fields
}
experiment = create_experiment_from_form(form_data)
# Returns: Experiment(id=UUID(...), created_at=datetime(...), ...)
```

## Form UI Components

**Streamlit Components Used**:
- `st.form()`: Form container
- `st.text_input()`: Text fields
- `st.text_area()`: Multi-line text fields
- `st.date_input()`: Date pickers
- `st.number_input()`: Number input (group size)
- `st.form_submit_button()`: Submit button
- `st.error()`: Error message display
- `st.success()`: Success message display

## User Experience Flow

1. User navigates to form page
2. Form displays with all sections
3. User fills in fields
4. User clicks "Submit Experiment"
5. Validation runs:
   - If invalid: Show errors, keep form data, allow correction
   - If valid: Save experiment, show success, offer dashboard navigation
6. User can submit another experiment or navigate to dashboard

## Error Handling

- **Validation Errors**: Display inline, don't clear form data
- **Save Errors**: Show error message, retain form data (user can retry or copy data)
- **Network/File Errors**: Show descriptive error, suggest retry

## Accessibility Considerations

- Clear field labels
- Required field indicators
- Error messages associated with fields
- Logical tab order
- Character count indicators for text areas (optional enhancement)

