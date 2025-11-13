# Visualization Service Contract

**Service**: Dashboard Visualization Generation  
**Type**: Plotly Chart Generation  
**File**: `src/services/visualization.py`

## Overview

The Visualization Service generates interactive charts and visualizations from experiment data using Plotly. It provides functions to create different visualization types as specified in the requirements.

## Interface

### `create_timeline_chart(experiments: List[Experiment], metrics: Optional[List[str]] = None) -> plotly.graph_objects.Figure`

**Description**: Creates a timeline visualization showing experiments over time.

**Parameters**:
- `experiments` (List[Experiment]): List of experiments to visualize
- `metrics` (Optional[List[str]]): Metrics to display (e.g., ["group_size", "experiment_count"]). Default: experiment count over time.

**Returns**:
- `plotly.graph_objects.Figure`: Plotly figure object

**Chart Type**: Line chart or scatter plot

**X-Axis**: Date (start_date of experiments, or date range if end_date available)

**Y-Axis**: Metric value (experiment count, group size, or other specified metrics)

**Features**:
- Hover tooltips showing experiment details
- Color coding by circle (if multiple circles)
- Interactive zoom and pan
- Click to filter/select experiments

**Example**:
```python
experiments = load_experiments()
fig = create_timeline_chart(experiments, metrics=["group_size"])
st.plotly_chart(fig, use_container_width=True)
```

---

### `create_comparison_chart(experiments: List[Experiment], metric: str, group_by: Optional[str] = None) -> plotly.graph_objects.Figure`

**Description**: Creates a comparison chart showing metrics across selected experiments.

**Parameters**:
- `experiments` (List[Experiment]): List of experiments to compare
- `metric` (str): Metric to compare (e.g., "group_size", "experiment_count")
- `group_by` (Optional[str]): Group by field (e.g., "circle", "lead_name"). Default: None (no grouping).

**Returns**:
- `plotly.graph_objects.Figure`: Plotly figure object

**Chart Type**: Bar chart (grouped bars if group_by specified)

**X-Axis**: Experiment identifier (display_name or lead_name + date)

**Y-Axis**: Metric value

**Features**:
- Grouped bars if group_by specified
- Color coding by group
- Hover tooltips
- Interactive selection

**Example**:
```python
selected_experiments = [exp1, exp2, exp3]
fig = create_comparison_chart(selected_experiments, metric="group_size", group_by="circle")
st.plotly_chart(fig, use_container_width=True)
```

---

### `create_distribution_chart(experiments: List[Experiment], field: str) -> plotly.graph_objects.Figure`

**Description**: Creates a distribution chart showing distribution of a field across experiments.

**Parameters**:
- `experiments` (List[Experiment]): List of experiments
- `field` (str): Field to show distribution for (e.g., "group_size", "circle")

**Returns**:
- `plotly.graph_objects.Figure`: Plotly figure object

**Chart Type**: Histogram (for numeric fields) or bar chart (for categorical fields)

**X-Axis**: Field values (bins for numeric, categories for categorical)

**Y-Axis**: Frequency/count

**Features**:
- Automatic binning for numeric fields
- Category grouping for string fields
- Hover tooltips showing counts
- Interactive filtering

**Example**:
```python
experiments = load_experiments()
fig = create_distribution_chart(experiments, field="group_size")
st.plotly_chart(fig, use_container_width=True)
```

---

### `create_circle_distribution_chart(experiments: List[Experiment]) -> plotly.graph_objects.Figure`

**Description**: Creates a chart showing experiment distribution by circle.

**Parameters**:
- `experiments` (List[Experiment]): List of experiments

**Returns**:
- `plotly.graph_objects.Figure`: Plotly figure object

**Chart Type**: Pie chart or bar chart

**Features**:
- Shows count of experiments per circle
- Percentage labels
- Color coding per circle
- Interactive selection

**Example**:
```python
experiments = load_experiments()
fig = create_circle_distribution_chart(experiments)
st.plotly_chart(fig, use_container_width=True)
```

---

### `filter_experiments(experiments: List[Experiment], filters: FilterCriteria) -> List[Experiment]`

**Description**: Filters experiments based on criteria.

**Parameters**:
- `experiments` (List[Experiment]): List of experiments to filter
- `filters` (FilterCriteria): Filter criteria (circles, date range, lead names)

**Returns**:
- `List[Experiment]`: Filtered list of experiments

**Filter Logic**:
- Circle filter: Include experiments where circle in filter.circles
- Date range: Include experiments where start_date in range
- Lead name: Include experiments where lead_name in filter.lead_names
- All filters are AND conditions (must match all specified filters)

**Example**:
```python
filters = FilterCriteria(
    circles=["Data Science", "Engineering"],
    date_range_start=date(2025, 1, 1),
    date_range_end=date(2025, 12, 31)
)
filtered = filter_experiments(experiments, filters)
```

---

### `get_experiment_summary_stats(experiments: List[Experiment]) -> dict`

**Description**: Calculates summary statistics for a list of experiments.

**Parameters**:
- `experiments` (List[Experiment]): List of experiments

**Returns**:
- `dict`: Dictionary of summary statistics

**Statistics Included**:
- Total experiment count
- Average group size
- Date range (earliest start, latest end)
- Circle distribution (count per circle)
- Experiments by time period (monthly/quarterly counts)

**Example**:
```python
experiments = load_experiments()
stats = get_experiment_summary_stats(experiments)
# Returns: {
#     "total_count": 10,
#     "avg_group_size": 12.5,
#     "date_range": {"start": "2025-01-01", "end": "2025-12-31"},
#     "circles": {"Data Science": 5, "Engineering": 5},
#     "monthly_counts": {...}
# }
```

## Visualization Requirements

**Minimum Visualization Types** (from SC-005):
1. ✅ Timeline chart
2. ✅ Comparison chart
3. ✅ Distribution chart

**Performance Requirements**:
- Render time: < 2 seconds (SC-002)
- Update time: < 1 second on interaction (SC-007)
- Support 50+ experiments without degradation (SC-003)

## Chart Configuration

**Default Settings**:
- Theme: Streamlit default (light mode)
- Colors: Distinct colors per circle/category
- Tooltips: Show key experiment details on hover
- Interactivity: Zoom, pan, select, filter

**Customization** (future enhancement):
- Color schemes
- Chart sizes
- Axis labels
- Legend positioning

## Error Handling

- **Empty Data**: Show empty state message instead of chart
- **Invalid Metrics**: Return error message, don't crash
- **Missing Fields**: Handle gracefully (skip or use defaults)
- **Large Datasets**: Optimize rendering (sampling, aggregation if needed)

## Integration with Streamlit

All visualization functions return Plotly figures that can be displayed using:
```python
st.plotly_chart(fig, use_container_width=True)
```

Streamlit's caching can be used to cache expensive visualization computations:
```python
@st.cache_data
def get_cached_visualization(experiments):
    return create_timeline_chart(experiments)
```

