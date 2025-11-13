"""Visualization service for generating dashboard charts using Plotly."""

from typing import List, Optional, Dict, Any
from datetime import date
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from src.models.experiment import Experiment, FilterCriteria


def create_timeline_chart(experiments: List[Experiment], metrics: Optional[List[str]] = None) -> go.Figure:
    """
    Create a timeline visualization showing experiments over time.

    Args:
        experiments: List of experiments to visualize
        metrics: Metrics to display (default: experiment count over time)

    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if not experiments:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No experiments to display",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig

    # Prepare data
    dates = []
    experiment_names = []
    circles = []
    group_sizes = []

    for exp in experiments:
        dates.append(exp.start_date)
        name = exp.display_name or f"{exp.lead_name} - {exp.start_date}"
        experiment_names.append(name)
        circles.append(exp.circle)
        group_sizes.append(exp.group_size)

    # Create DataFrame for easier manipulation
    df = pd.DataFrame({
        'date': dates,
        'experiment': experiment_names,
        'circle': circles,
        'group_size': group_sizes
    })

    # Group by date and circle for count
    df_grouped = df.groupby(['date', 'circle']).size().reset_index(name='count')
    df_grouped = df_grouped.sort_values('date')

    # Create timeline chart
    fig = go.Figure()

    # Add scatter plot with different colors per circle
    for circle in df_grouped['circle'].unique():
        circle_data = df_grouped[df_grouped['circle'] == circle]
        fig.add_trace(go.Scatter(
            x=circle_data['date'],
            y=circle_data['count'],
            mode='lines+markers',
            name=circle,
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Date: %{x}<br>' +
                         'Count: %{y}<extra></extra>'
        ))

    fig.update_layout(
        title="Experiments Timeline",
        xaxis_title="Date",
        yaxis_title="Experiment Count",
        hovermode='closest',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


def create_comparison_chart(experiments: List[Experiment], metric: str, group_by: Optional[str] = None) -> go.Figure:
    """
    Create a comparison chart showing metrics across selected experiments.

    Args:
        experiments: List of experiments to compare
        metric: Metric to compare (e.g., "group_size")
        group_by: Group by field (e.g., "circle", "lead_name")

    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if not experiments:
        fig = go.Figure()
        fig.add_annotation(
            text="No experiments to compare",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig

    # Prepare data
    experiment_labels = []
    metric_values = []
    group_values = []

    for exp in experiments:
        label = exp.display_name or f"{exp.lead_name} - {exp.start_date}"
        experiment_labels.append(label)
        
        # Get metric value
        if metric == "group_size":
            metric_values.append(exp.group_size)
        else:
            metric_values.append(0)  # Default for unknown metrics

        # Get group_by value
        if group_by == "circle":
            group_values.append(exp.circle)
        elif group_by == "lead_name":
            group_values.append(exp.lead_name)
        else:
            group_values.append("All")

    # Create bar chart
    if group_by:
        df = pd.DataFrame({
            'experiment': experiment_labels,
            'metric': metric_values,
            'group': group_values
        })
        fig = px.bar(df, x='experiment', y='metric', color='group',
                     title=f"Comparison: {metric} by {group_by}",
                     labels={'metric': metric.replace('_', ' ').title(), 'experiment': 'Experiment'})
    else:
        fig = go.Figure(data=[
            go.Bar(x=experiment_labels, y=metric_values)
        ])
        fig.update_layout(
            title=f"Comparison: {metric}",
            xaxis_title="Experiment",
            yaxis_title=metric.replace('_', ' ').title()
        )

    return fig


def create_distribution_chart(experiments: List[Experiment], field: str) -> go.Figure:
    """
    Create a distribution chart showing distribution of a field across experiments.

    Args:
        experiments: List of experiments
        field: Field to show distribution for (e.g., "group_size", "circle")

    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if not experiments:
        fig = go.Figure()
        fig.add_annotation(
            text="No experiments to display",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig

    # Extract field values
    values = []
    for exp in experiments:
        if field == "group_size":
            values.append(exp.group_size)
        elif field == "circle":
            values.append(exp.circle)
        else:
            values.append(None)

    # Filter out None values
    values = [v for v in values if v is not None]

    if not values:
        fig = go.Figure()
        fig.add_annotation(
            text=f"No data for field: {field}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig

    # Determine if numeric or categorical
    if field == "group_size":
        # Histogram for numeric
        fig = go.Figure(data=[go.Histogram(x=values, nbinsx=10)])
        fig.update_layout(
            title=f"Distribution of {field.replace('_', ' ').title()}",
            xaxis_title=field.replace('_', ' ').title(),
            yaxis_title="Frequency"
        )
    else:
        # Bar chart for categorical
        from collections import Counter
        counts = Counter(values)
        fig = go.Figure(data=[
            go.Bar(x=list(counts.keys()), y=list(counts.values()))
        ])
        fig.update_layout(
            title=f"Distribution of {field.replace('_', ' ').title()}",
            xaxis_title=field.replace('_', ' ').title(),
            yaxis_title="Count"
        )

    return fig


def create_circle_distribution_chart(experiments: List[Experiment]) -> go.Figure:
    """
    Create a chart showing experiment distribution by circle.

    Args:
        experiments: List of experiments

    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    if not experiments:
        fig = go.Figure()
        fig.add_annotation(
            text="No experiments to display",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig

    # Count experiments per circle
    from collections import Counter
    circle_counts = Counter(exp.circle for exp in experiments)

    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=list(circle_counts.keys()),
        values=list(circle_counts.values()),
        hole=0.3
    )])
    fig.update_layout(title="Experiment Distribution by Circle")

    return fig


def filter_experiments(experiments: List[Experiment], filters: FilterCriteria) -> List[Experiment]:
    """
    Filter experiments based on criteria.

    Args:
        experiments: List of experiments to filter
        filters: Filter criteria (circles, date range, lead names)

    Returns:
        List[Experiment]: Filtered list of experiments
    """
    filtered = experiments

    # Filter by circles
    if filters.circles:
        filtered = [exp for exp in filtered if exp.circle in filters.circles]

    # Filter by date range
    if filters.date_range_start:
        filtered = [exp for exp in filtered if exp.start_date >= filters.date_range_start]
    if filters.date_range_end:
        filtered = [exp for exp in filtered if exp.start_date <= filters.date_range_end]

    # Filter by lead names
    if filters.lead_names:
        filtered = [exp for exp in filtered if exp.lead_name in filters.lead_names]

    return filtered


def get_experiment_summary_stats(experiments: List[Experiment]) -> Dict[str, Any]:
    """
    Calculate summary statistics for a list of experiments.

    Args:
        experiments: List of experiments

    Returns:
        dict: Dictionary of summary statistics
    """
    if not experiments:
        return {
            "total_count": 0,
            "avg_group_size": 0,
            "date_range": {"start": None, "end": None},
            "circles": {},
            "monthly_counts": {}
        }

    # Total count
    total_count = len(experiments)

    # Average group size
    group_sizes = [exp.group_size for exp in experiments]
    avg_group_size = sum(group_sizes) / len(group_sizes) if group_sizes else 0

    # Date range
    start_dates = [exp.start_date for exp in experiments]
    end_dates = [exp.end_date for exp in experiments if exp.end_date]
    date_range = {
        "start": min(start_dates).isoformat() if start_dates else None,
        "end": max(end_dates).isoformat() if end_dates else None
    }

    # Circle distribution
    from collections import Counter
    circle_counts = Counter(exp.circle for exp in experiments)
    circles = dict(circle_counts)

    # Monthly counts
    monthly_counts = {}
    for exp in experiments:
        month_key = exp.start_date.strftime("%Y-%m")
        monthly_counts[month_key] = monthly_counts.get(month_key, 0) + 1

    return {
        "total_count": total_count,
        "avg_group_size": round(avg_group_size, 2),
        "date_range": date_range,
        "circles": circles,
        "monthly_counts": monthly_counts
    }

