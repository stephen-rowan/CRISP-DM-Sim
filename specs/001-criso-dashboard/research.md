# Research: CRISP Analysis Dashboard

**Date**: 2025-01-27  
**Phase**: Phase 0 - Outline & Research  
**Purpose**: Resolve all NEEDS CLARIFICATION items from Technical Context and Constitution Check

## Research Tasks

### 1. Python Version and Dependency Management

**Task**: Determine Python version requirements and specific library versions for Streamlit dashboard

**Findings**:
- **Decision**: Python 3.11+ (minimum 3.11 for modern features and performance)
- **Rationale**: 
  - Streamlit requires Python 3.8+, but 3.11+ provides better performance and type hinting support
  - Python 3.11+ is widely available and stable
  - Better support for modern Python features (dataclasses, type hints, pattern matching)
- **Alternatives considered**: 
  - Python 3.8-3.10: Older versions work but lack performance improvements
  - Python 3.12+: Too new, may have compatibility issues with some libraries

**Dependencies**:
- **Decision**: 
  - `streamlit>=1.28.0` (latest stable, good performance)
  - `pandas>=2.0.0` (required for data manipulation)
  - `plotly>=5.17.0` (interactive visualizations, primary visualization library)
  - `pydantic>=2.0.0` (data validation and models)
  - `python-dateutil>=2.8.0` (date parsing and validation)
- **Rationale**: 
  - Streamlit 1.28+ has improved performance and caching
  - Plotly is preferred over matplotlib for interactive Streamlit dashboards (better integration, interactivity)
  - Pydantic provides robust data validation for form inputs
  - Pandas 2.0+ has better performance and type support
- **Alternatives considered**:
  - matplotlib: Less interactive, requires more code for Streamlit integration
  - altair: Good but plotly has better feature set for this use case

### 2. JSON File Storage Structure and Naming

**Task**: Define JSON file path, naming convention, and data structure

**Findings**:
- **Decision**: 
  - File path: `data/experiments.json` (relative to project root)
  - Format: Single JSON array containing all experiments
  - Naming: Fixed filename `experiments.json` (no versioning or user-specific files for MVP)
- **Rationale**: 
  - `data/` directory keeps data separate from source code
  - Single array format simplifies reading/writing (no need to merge multiple files)
  - Fixed filename aligns with single-user, local deployment assumption
  - JSON array format matches spec requirement (FR-008)
- **Alternatives considered**:
  - One file per experiment: More complex file management, harder to read all experiments
  - Database (SQLite): Overkill for MVP, adds complexity
  - User-specific files: Not needed for MVP (no authentication)

**Data Structure**:
```json
[
  {
    "id": "uuid-string",
    "created_at": "ISO-8601-timestamp",
    "display_name": "optional-friendly-name",
    "lead_name": "string",
    "circle": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD or null",
    "problem_statement": "string",
    "baseline_statement": "string",
    "purpose_objectives": "string",
    "who_was_involved": "string",
    "group_size": integer,
    "method_description": "string",
    "success_criteria": "string",
    "analysis_approach": "string",
    "evaluation_plan": "string"
  }
]
```

### 3. Testing Framework and Structure

**Task**: Define testing approach, framework setup, and coverage requirements

**Findings**:
- **Decision**: 
  - Framework: `pytest>=7.4.0` with `pytest-cov>=4.1.0` for coverage
  - Test structure: Unit tests for models/services, integration tests for form flow
  - Coverage target: 80% minimum for core business logic (models, services)
  - Mocking: `pytest-mock>=3.12.0` for mocking file I/O and Streamlit components
- **Rationale**: 
  - pytest is the de facto standard for Python testing
  - pytest-cov provides coverage reporting
  - 80% coverage is reasonable for MVP (focus on critical paths)
  - Mocking file I/O allows testing without actual file system operations
- **Alternatives considered**:
  - unittest: More verbose, less Pythonic
  - Higher coverage (90%+): Too strict for MVP, slows development
  - No coverage requirement: Insufficient quality assurance

**Test Organization**:
- `tests/unit/`: Test individual functions and classes in isolation
- `tests/integration/`: Test complete workflows (form submission → storage → visualization)

### 4. Data Quality Assessment Procedures

**Task**: Define data quality standards and assessment procedures for user-submitted form data

**Findings**:
- **Decision**: 
  - **Completeness**: All required fields must be present (validated at form submission)
  - **Correctness**: 
    - Date validation (end_date >= start_date)
    - Group size must be positive integer
    - Text fields must be non-empty strings (after trimming)
  - **Consistency**: 
    - UUID format validation
    - ISO-8601 timestamp format for created_at
    - Date format consistency (YYYY-MM-DD)
  - **Quality Metrics**: 
    - Required field completion rate: 100% (enforced)
    - Date logic errors: 0% (prevented by validation)
    - Text field length: Documented max (5000 chars per field)
- **Rationale**: 
  - Form validation ensures data quality at entry point
  - Client-side and server-side validation prevent invalid data
  - Quality metrics align with CRISP-DM Data Understanding phase requirements
- **Alternatives considered**:
  - Post-submission validation only: Allows bad data entry, harder to fix
  - Loose validation: Leads to data quality issues downstream

**Data Quality Procedures**:
1. **At Entry (Form Validation)**: 
   - Required field checks
   - Type validation (dates, integers, strings)
   - Business rule validation (date logic, positive numbers)
2. **At Storage**: 
   - Schema validation using Pydantic models
   - JSON serialization validation
3. **At Load**: 
   - JSON parsing validation
   - Schema validation on read
   - Handle corrupted data gracefully (skip invalid entries, log errors)

### 5. Data Preparation Procedures

**Task**: Document JSON file structure, data validation, and transformation procedures

**Findings**:
- **Decision**: 
  - **Storage Format**: JSON array as specified in FR-008
  - **Validation**: Pydantic models enforce schema at write time
  - **Transformation**: 
    - Form inputs → Pydantic model → JSON serialization
    - JSON deserialization → Pydantic model → Dashboard data structures
  - **Data Cleaning**: 
    - Trim whitespace from text fields
    - Normalize date formats to YYYY-MM-DD
    - Ensure UUID format consistency
- **Rationale**: 
  - Pydantic provides automatic validation and serialization
  - Consistent data format ensures reliable visualizations
  - Minimal transformation needed (form data is already structured)
- **Alternatives considered**:
  - Manual validation: Error-prone, more code
  - No transformation: Risk of inconsistent data formats

**Data Preparation Workflow**:
1. User submits form → Form data dictionary
2. Validate against Pydantic Experiment model
3. Add metadata (UUID, created_at timestamp)
4. Append to existing experiments array
5. Serialize entire array to JSON
6. Write to `data/experiments.json`

### 6. CRISP-DM Modeling Phase Interpretation

**Task**: Clarify how Modeling phase applies to visualization dashboard (not predictive model)

**Findings**:
- **Decision**: 
  - **Modeling Phase Interpretation**: In CRISP-DM context, "Modeling" refers to creating analytical models or visualizations that represent patterns in data
  - For this dashboard project, "Modeling" = **Visualization Design and Implementation**
  - The "model" is the dashboard visualization structure that represents experiment data patterns
- **Rationale**: 
  - CRISP-DM framework is flexible and applies to analytics/visualization projects, not just predictive modeling
  - Visualization design is analogous to model selection in traditional data mining
  - Dashboard visualizations are the "models" that help users understand experiment patterns
- **Alternatives considered**:
  - Skip Modeling phase: Violates CRISP-DM framework requirements
  - Traditional ML model: Not applicable to this use case

**Modeling Phase Deliverables**:
- Visualization type selection (timeline, bar charts, comparison views)
- Visualization design rationale (why these visualizations answer business questions)
- Visualization implementation (code for generating charts)
- Visualization performance assessment (render time, interactivity)

### 7. Deployment Plan and Configuration

**Task**: Define local deployment approach, Streamlit server configuration, and file storage location

**Findings**:
- **Decision**: 
  - **Deployment Type**: Local development and single-machine deployment
  - **Streamlit Configuration**: 
    - Default port: 8501 (Streamlit default)
    - Server configuration: `streamlit run src/app.py`
    - No authentication (as per spec assumptions)
  - **File Storage**: 
    - Location: `data/experiments.json` (relative to project root)
    - Permissions: Read/write for application user
    - Backup: Manual (user responsibility for MVP)
  - **Environment Setup**: 
    - Virtual environment (venv or conda)
    - `requirements.txt` for dependency management
    - `.env` file for configuration (if needed in future)
- **Rationale**: 
  - Local deployment aligns with MVP scope (no distributed requirements)
  - Streamlit's default configuration is sufficient for single-user access
  - Simple file-based storage meets requirements without infrastructure complexity
- **Alternatives considered**:
  - Cloud deployment: Out of scope for MVP
  - Database deployment: Unnecessary complexity for local, single-user use case
  - Docker containerization: Could be added later, not needed for MVP

**Deployment Steps**:
1. Install Python 3.11+
2. Create virtual environment
3. Install dependencies from `requirements.txt`
4. Create `data/` directory
5. Initialize `data/experiments.json` as empty array `[]`
6. Run `streamlit run src/app.py`
7. Access dashboard at `http://localhost:8501`

### 8. Visualization Validation Methodology

**Task**: Define validation approach for dashboard visualizations (accuracy, performance, usability)

**Findings**:
- **Decision**: 
  - **Accuracy Validation**: 
    - Visual inspection: Charts display correct data from experiments
    - Data integrity checks: Visualization data matches source JSON data
    - Calculation verification: Aggregations and metrics computed correctly
  - **Performance Validation**: 
    - Render time: < 2 seconds (SC-002)
    - Update time: < 1 second on interaction (SC-007)
    - Load time: < 3 seconds for 50 experiments (SC-003)
  - **Usability Validation**: 
    - User testing: 90% success rate for form completion and first visualization (SC-004)
    - Visual clarity: At least 3 distinct visualization types (SC-005)
  - **Validation Methods**: 
    - Automated performance tests (timing measurements)
    - Manual visual inspection (QA process)
    - User acceptance testing (UAT) with sample data
- **Rationale**: 
  - Multi-faceted validation ensures both technical correctness and user value
  - Performance metrics align with success criteria
  - Usability validation ensures dashboard meets business objectives
- **Alternatives considered**:
  - Automated only: Misses usability and visual quality issues
  - Manual only: Inconsistent, not scalable

**Validation Checklist**:
- [ ] Visualizations render correct data (compare chart data to JSON source)
- [ ] All visualization types display without errors
- [ ] Performance meets success criteria (timing tests)
- [ ] Interactive features work (filtering, selection)
- [ ] Empty state displays correctly (no experiments)
- [ ] Sample data generation works (US3)
- [ ] Comparative visualizations work (multiple experiments selected)

## Summary of Resolved Clarifications

All NEEDS CLARIFICATION items from Technical Context and Constitution Check have been resolved:

1. ✅ Python version: 3.11+
2. ✅ Dependencies: Streamlit, pandas, plotly, pydantic (specific versions)
3. ✅ Storage: `data/experiments.json`, JSON array format
4. ✅ Testing: pytest with 80% coverage target
5. ✅ Data quality: Validation procedures defined
6. ✅ Data preparation: Transformation workflow documented
7. ✅ Modeling phase: Interpreted as visualization design
8. ✅ Deployment: Local Streamlit deployment plan
9. ✅ Visualization validation: Methodology defined

## Next Steps

Proceed to Phase 1: Design & Contracts
- Generate data-model.md from feature spec entities
- Generate API contracts (form submission, data retrieval)
- Generate quickstart.md for setup instructions
- Update agent context with new technologies

