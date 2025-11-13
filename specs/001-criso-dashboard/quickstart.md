# Quickstart Guide: CRISP Analysis Dashboard

**Date**: 2025-01-27  
**Phase**: Phase 1 - Design & Contracts  
**Purpose**: Setup and usage instructions for developers and users

## Prerequisites

- **Python**: 3.11 or higher
- **pip**: Python package manager
- **Web Browser**: Modern browser (Chrome, Firefox, Safari, Edge)
- **Operating System**: macOS, Linux, or Windows

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd CRISP-DM-Sim
git checkout 001-crisp-dashboard
```

### 2. Create Virtual Environment

```bash
# Using venv (recommended)
python3.11 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Dependencies** (from research.md):
- `streamlit>=1.28.0`
- `pandas>=2.0.0`
- `plotly>=5.17.0`
- `pydantic>=2.0.0`
- `python-dateutil>=2.8.0`
- `pytest>=7.4.0` (for testing)
- `pytest-cov>=4.1.0` (for coverage)
- `pytest-mock>=3.12.0` (for mocking)

### 4. Create Data Directory

```bash
mkdir -p data
echo "[]" > data/experiments.json
```

This creates the data directory and initializes an empty experiments file.

## Running the Application

### Start Streamlit Server

```bash
streamlit run src/app.py
```

The application will start and automatically open in your default web browser at `http://localhost:8501`.

If the browser doesn't open automatically, navigate to `http://localhost:8501` manually.

### Application Structure

The application has two main pages:

1. **Form Page** (`/form`): Submit new CRISP experiments
2. **Dashboard Page** (`/dashboard`): View visualizations and analysis

Navigation between pages is handled via Streamlit's page navigation.

## Usage

### Submitting an Experiment

1. Navigate to the Form page
2. Fill in all required fields:
   - **Experiment Details**: Lead name, circle, start date (end date optional)
   - **Question/Problem Statement**: Describe the problem
   - **Baseline Statement**: Current state/baseline
   - **Purpose/Objectives**: Goals of the experiment
   - **Design and Execution**: Who was involved, group size, method
   - **Evaluation and Outcome**: Success criteria, analysis approach, evaluation plan
3. Click "Submit Experiment"
4. If validation passes, you'll see a success message
5. Navigate to Dashboard to view your experiment

### Viewing the Dashboard

1. Navigate to the Dashboard page
2. View visualizations:
   - **Timeline**: Experiments over time
   - **Comparison**: Compare metrics across experiments
   - **Distribution**: Distribution of metrics (group size, circles, etc.)
3. Use filters to focus on specific experiments:
   - Filter by circle
   - Filter by date range
   - Filter by lead name
4. Select specific experiments to compare

### Generating Sample Data

1. On the Dashboard page, click "Generate Sample Data"
2. Confirm the action (warning: this replaces existing data)
3. The dashboard will refresh with 5 sample experiments
4. Explore the visualizations with the sample data

## Development

### Project Structure

```
CRISP-DM-Sim/
├── src/
│   ├── models/
│   │   └── experiment.py          # Experiment data model
│   ├── services/
│   │   ├── storage.py              # JSON file persistence
│   │   ├── visualization.py       # Chart generation
│   │   └── sample_data.py          # Sample data generation
│   ├── pages/
│   │   ├── form_page.py           # Form interface
│   │   └── dashboard_page.py      # Dashboard interface
│   └── app.py                      # Main application entry
├── data/
│   └── experiments.json            # Experiment data storage
├── tests/
│   ├── unit/                       # Unit tests
│   └── integration/                # Integration tests
└── requirements.txt                # Python dependencies
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py
```

### Code Quality

```bash
# Format code (if using black)
black src/ tests/

# Lint code (if using flake8 or pylint)
flake8 src/ tests/
```

## Configuration

### File Storage Location

By default, experiments are stored in `data/experiments.json` (relative to project root).

To change the storage location, modify `src/services/storage.py`:

```python
EXPERIMENTS_FILE = "path/to/your/experiments.json"
```

### Streamlit Configuration

Streamlit configuration can be customized via `.streamlit/config.toml`:

```toml
[server]
port = 8501
headless = false

[theme]
primaryColor = "#1f77b4"
```

## Troubleshooting

### Port Already in Use

If port 8501 is already in use:

```bash
streamlit run src/app.py --server.port 8502
```

### File Permission Errors

If you encounter file permission errors when saving experiments:

1. Check that `data/` directory exists and is writable
2. Check file permissions: `chmod 644 data/experiments.json`
3. Ensure you have write permissions in the project directory

### Import Errors

If you encounter import errors:

1. Ensure virtual environment is activated
2. Verify all dependencies are installed: `pip list`
3. Check Python path: `python -c "import sys; print(sys.path)"`

### JSON File Corruption

If the JSON file becomes corrupted:

1. Backup the file: `cp data/experiments.json data/experiments.json.backup`
2. Try to fix manually or restore from backup
3. If unrecoverable, initialize empty file: `echo "[]" > data/experiments.json`

## Next Steps

- Review the [data model documentation](./data-model.md) for entity details
- Review the [service contracts](./contracts/) for API details
- Review the [implementation plan](./plan.md) for design decisions
- Review the [research findings](./research.md) for technical decisions

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the specification documents in `specs/001-criso-dashboard/`
3. Check the project README for additional information

