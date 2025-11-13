# CRISP-DM-Sim

CRISP Analysis Dashboard - A Streamlit web application for visualizing CRISP experiment data.

## About CRISP-DM

**CRISP-DM** (Cross-Industry Standard Process for Data Mining) is a proven methodology for data science and analytics projects. It provides a structured approach with six phases:

1. **Business Understanding** - Define project objectives and requirements from a business perspective
2. **Data Understanding** - Collect and explore data, assess data quality
3. **Data Preparation** - Clean, transform, and prepare data for modeling
4. **Modeling** - Select and apply modeling techniques, calibrate parameters
5. **Evaluation** - Assess models against business objectives, review process
6. **Deployment** - Plan deployment, monitoring, and maintenance

This application helps document and track data science experiments following CRISP-DM principles. Each experiment captures:
- **Problem Statement** (Business Understanding)
- **Baseline Statement** (Data Understanding)
- **Purpose/Objectives** (Business Understanding)
- **Method Description** (Data Preparation & Modeling)
- **Success Criteria & Evaluation Plan** (Evaluation & Deployment)

The sample data demonstrates how different teams and projects apply CRISP-DM methodology across various problem domains.

## Quick Start

```bash
# 1. Clone and navigate to project
git clone <repository-url>
cd CRISP-DM-Sim
git checkout 001-crisp-dashboard

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create data directory
mkdir -p data
echo "[]" > data/experiments.json

# 5. Run the application (from project root)
cd /path/to/CRISP-DM-Sim  # Make sure you're in the project root
streamlit run app.py
```

The application will open at `http://localhost:8501`

**Important**: Always run `streamlit run app.py` from the project root directory (where `src/`, `pages/`, and `data/` folders are located).

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

### 2. Check Python Version

First, verify you have Python 3.11 or higher installed:

```bash
# Check Python version
python3 --version
# or
python --version

# Should show: Python 3.11.x or higher
```

If Python 3.11+ is not installed, install it from [python.org](https://www.python.org/downloads/) or use a package manager:

```bash
# macOS (using Homebrew)
brew install python@3.11

# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3.11-pip

# Windows: Download from python.org
```

### 3. Create Virtual Environment

Create and activate a Python virtual environment:

```bash
# Using venv (recommended)
python3.11 -m venv venv
# or if python3.11 is not in PATH, use:
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

**Verify activation**: Your terminal prompt should show `(venv)` at the beginning:

```bash
(venv) user@hostname:~/CRISP-DM-Sim$
```

**Alternative: Using conda** (if you prefer conda):

```bash
# Create conda environment
conda create -n crisp-dashboard python=3.11
conda activate crisp-dashboard
```

### 4. Install Dependencies

With the virtual environment activated, install all required packages:

```bash
# Upgrade pip first (recommended)
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

**Expected packages**:
- streamlit>=1.28.0
- pandas>=2.0.0
- plotly>=5.17.0
- pydantic>=2.0.0
- python-dateutil>=2.8.0
- pytest>=7.4.0
- pytest-cov>=4.1.0
- pytest-mock>=3.12.0

### 5. Create Data Directory

Create the data directory and initialize the experiments file:

```bash
# Create data directory
mkdir -p data

# Initialize empty experiments file
echo "[]" > data/experiments.json

# Verify file was created
ls -la data/experiments.json
```

This creates the data directory and initializes an empty experiments file.

## Running the Application

### Activate Virtual Environment (if not already active)

```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

### Start Streamlit Server

```bash
# Make sure virtual environment is activated
# Then run from project root:
streamlit run app.py

# Or if you're in a different directory, use:
cd /path/to/CRISP-DM-Sim
streamlit run app.py
```

**Note**: Always run the command from the project root directory (`CRISP-DM-Sim/`) to ensure proper path resolution.

The application will start and automatically open in your default web browser at `http://localhost:8501`.

If the browser doesn't open automatically, navigate to `http://localhost:8501` manually.

**Note**: Keep the terminal window open while the application is running. Press `Ctrl+C` to stop the server.

**Navigation**: Streamlit automatically creates navigation links in the top-left sidebar. You should see:
- **Home** (app.py)
- **1_Form** (Form page)
- **2_Dashboard** (Dashboard page)

If navigation links don't appear, try:
1. Stop the Streamlit server (Ctrl+C) and restart it
2. Clear your browser cache or use a hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
3. Make sure you're running `streamlit run app.py` from the project root

### Application Structure

The application uses Streamlit's native multi-page navigation with the following pages:

1. **Home** (`app.py`): Welcome page with navigation instructions
2. **Form** (`pages/1_Form.py`): Submit new CRISP experiments
3. **Dashboard** (`pages/2_Dashboard.py`): View visualizations and analysis

Navigation between pages is handled automatically by Streamlit. Use the navigation links in the top-left sidebar to switch between pages.

## Usage

### Submitting an Experiment

The form follows CRISP-DM methodology to ensure comprehensive documentation:

1. Navigate to the Form page
2. Fill in all required fields, which map to CRISP-DM phases:
   - **Experiment Details**: Project metadata (lead, team, dates)
   - **Question/Problem Statement** (Business Understanding): What business problem are you solving?
   - **Baseline Statement** (Data Understanding): What is the current state or baseline performance?
   - **Purpose/Objectives** (Business Understanding): What are your specific goals and success metrics?
   - **Design and Execution** (Data Preparation & Modeling): Describe your methodology, who's involved, and approach
   - **Evaluation and Outcome** (Evaluation & Deployment): Define success criteria, analysis approach, and evaluation plan
3. Click "Submit Experiment"
4. If validation passes, you'll see a success message
5. Navigate to Dashboard to view your experiment alongside others

### Viewing the Dashboard

The dashboard provides insights into your CRISP-DM experiment portfolio:

1. Navigate to the Dashboard page
2. Explore the data:
   - **Summary Statistics**: Overview of your experiment portfolio
   - **Data Table**: Quick reference table of all experiments with key fields
   - **Experiment Details**: Browse full documentation of each experiment's CRISP-DM phases
   - **Visualizations**: 
     - **Timeline**: See experiments over time to track project evolution
     - **Comparison**: Compare metrics across experiments to identify patterns
     - **Distribution**: Analyze distribution of metrics (group size, circles, etc.)
3. Use filters to focus on specific experiments:
   - Filter by circle/team to see how different groups apply CRISP-DM
   - Filter by date range to analyze temporal trends
   - Filter by lead name to track individual contributions
4. Select specific experiments to compare methodologies and outcomes

### Sample Data

The dashboard automatically initializes with 10 sample experiments when you first open it (if no experiments exist). These sample experiments demonstrate:

- **Various CRISP-DM Applications**: Different problem types (accuracy, engagement, performance, retention, etc.)
- **Multiple Teams**: Examples from Data Science, Engineering, Product, Analytics, and Operations circles
- **Different Methodologies**: A/B testing, controlled experiments, observational studies, time series analysis, etc.
- **Temporal Distribution**: Experiments spanning different time periods to show project evolution
- **Complete Documentation**: All fields populated following CRISP-DM best practices

This allows you to immediately explore the visualizations and features, understand how CRISP-DM is applied across different scenarios, and see examples of well-documented experiments.

**Note**: Sample data is only generated automatically if the experiments file is empty. Once you have real data, the sample data will not be automatically generated again.

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

**Important**: Make sure your virtual environment is activated before running tests.

```bash
# Activate virtual environment first (if not already active)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py

# Run tests with verbose output
pytest -v

# Run tests and show coverage in terminal
pytest --cov=src --cov-report=term-missing
```

After running coverage, view the HTML report:

```bash
# Coverage report will be in htmlcov/index.html
# Open in browser:
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
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

## Deactivating Virtual Environment

When you're done working on the project:

```bash
# Deactivate virtual environment
deactivate

# Your prompt should return to normal (no (venv) prefix)
```

## Troubleshooting

### Virtual Environment Issues

**Problem**: `python3.11: command not found`

**Solution**: 
- Use `python3` instead of `python3.11`
- Or install Python 3.11+ and ensure it's in your PATH
- Check available Python versions: `python3 --version`

**Problem**: Virtual environment not activating

**Solution**:
```bash
# Verify venv directory exists
ls -la venv/

# Try recreating the virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### Port Already in Use

If port 8501 is already in use:

```bash
streamlit run app.py --server.port 8502
```

### File Permission Errors

If you encounter file permission errors when saving experiments:

1. Check that `data/` directory exists and is writable
2. Check file permissions: `chmod 644 data/experiments.json`
3. Ensure you have write permissions in the project directory

### Import Errors

If you encounter import errors like `ModuleNotFoundError: No module named 'src'`:

1. **Ensure virtual environment is activated**:
   ```bash
   # Check if venv is active (should see (venv) in prompt)
   which python  # Should point to venv/bin/python
   
   # If not active, activate it:
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate  # Windows
   ```

2. **Verify you're running from the project root**:
   ```bash
   # Make sure you're in the CRISP-DM-Sim directory
   pwd  # Should show path ending in CRISP-DM-Sim
   ls -la  # Should show app.py, pages/, src/, data/ directories
   
   # Then run:
   streamlit run app.py
   ```

3. **Verify all dependencies are installed**:
   ```bash
   pip list
   # Should show all required packages
   ```

4. **Reinstall dependencies if needed**:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

5. **Check Python path**:
   ```bash
   python -c "import sys; print(sys.path)"
   # Should include venv paths
   ```

6. **Verify Python version**:
   ```bash
   python --version
   # Should be 3.11 or higher
   ```

### JSON File Corruption

If the JSON file becomes corrupted:

1. Backup the file: `cp data/experiments.json data/experiments.json.backup`
2. Try to fix manually or restore from backup
3. If unrecoverable, initialize empty file: `echo "[]" > data/experiments.json`

## Documentation

For detailed documentation, see:
- [Data Model](./specs/001-criso-dashboard/data-model.md)
- [Service Contracts](./specs/001-criso-dashboard/contracts/)
- [Implementation Plan](./specs/001-criso-dashboard/plan.md)
- [Research Findings](./specs/001-criso-dashboard/research.md)
