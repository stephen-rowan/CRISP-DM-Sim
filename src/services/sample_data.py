"""Sample data service for generating realistic experiment data."""

from datetime import date, timedelta
from typing import List
import random

from src.models.experiment import Experiment
from src.services.storage import save_experiments


# Sample data templates
CIRCLES = ["Data Science", "Engineering", "Product", "Analytics", "Operations"]
LEAD_NAMES = ["Jane Smith", "John Doe", "Alice Johnson", "Bob Williams", "Carol Davis", 
              "David Brown", "Eva Martinez", "Frank Wilson", "Grace Lee", "Henry Taylor"]

# Display name templates for generating varied, plausible experiment names
DISPLAY_NAME_TEMPLATES = [
    "{circle} Q{quarter} {year} Initiative",
    "{circle} {month} {year} Study",
    "{circle} {problem_type} Analysis",
    "{circle} {year} Experiment",
    "{circle} {month} Research Project",
    "{circle} Performance Study {year}",
    "{circle} {problem_type} Evaluation",
    "{circle} {month} {year} Trial",
]

PROBLEM_TYPES = [
    "Accuracy",
    "Engagement",
    "Performance",
    "Retention",
    "Optimization",
    "Quality",
    "Efficiency",
    "Conversion",
]

PROBLEM_STATEMENTS = [
    "How can we improve model accuracy by 10%?",
    "What is the impact of feature X on user engagement?",
    "Can we reduce processing time while maintaining quality?",
    "How does algorithm Y compare to algorithm Z?",
    "What factors influence customer retention?",
    "Can we optimize resource allocation?",
    "How effective is the new recommendation system?",
    "What is the relationship between metrics A and B?",
    "How can we improve user satisfaction scores?",
    "What is the optimal pricing strategy for our product?",
    "Can we reduce customer churn through targeted interventions?",
    "How does user onboarding flow affect conversion rates?",
    "What is the impact of UI changes on user behavior?",
    "Can we improve data quality through automated validation?",
    "How effective are our current marketing campaigns?",
]

BASELINE_STATEMENTS = [
    "Current accuracy is 85%",
    "Baseline performance shows 70% engagement",
    "Initial measurements indicate 2.5s processing time",
    "Current system achieves 60% success rate",
    "Baseline retention rate is 75%",
    "Current resource utilization is 80%",
    "Existing system has 3.2 rating",
    "Baseline correlation is 0.45",
    "Current satisfaction score is 3.5/5.0",
    "Baseline conversion rate is 12%",
    "Current churn rate is 8% monthly",
    "Baseline onboarding completion is 65%",
    "Current click-through rate is 2.3%",
    "Baseline data quality score is 78%",
    "Current campaign ROI is 2.1x",
]

PURPOSE_OBJECTIVES = [
    "Increase accuracy to 90%",
    "Improve engagement by 15%",
    "Reduce processing time to under 2s",
    "Achieve 70% success rate",
    "Improve retention to 80%",
    "Optimize utilization to 90%",
    "Achieve 4.0 rating",
    "Increase correlation to 0.60",
    "Improve satisfaction to 4.2/5.0",
    "Increase conversion rate to 15%",
    "Reduce churn to 5% monthly",
    "Improve onboarding completion to 80%",
    "Increase click-through rate to 3.5%",
    "Improve data quality to 90%",
    "Achieve campaign ROI of 3.0x",
]

WHO_INVOLVED = [
    "Data team, Engineering team",
    "Product team, Analytics team",
    "Engineering team, Operations team",
    "Data Science team, Product team",
    "Analytics team, Engineering team",
    "Cross-functional team",
    "Data team, Product team, Engineering team",
    "Full stack team",
    "Product team, Design team, Engineering team",
    "Marketing team, Analytics team",
    "Customer Success team, Product team",
    "UX team, Engineering team, Product team",
    "Data Engineering team, Analytics team",
    "Quality Assurance team, Engineering team",
    "Business Intelligence team, Product team",
]

METHOD_DESCRIPTIONS = [
    "A/B testing with new features",
    "Controlled experiment with treatment and control groups",
    "Observational study of user behavior",
    "Randomized controlled trial",
    "Quasi-experimental design",
    "Longitudinal study over 3 months",
    "Cross-sectional analysis",
    "Time series analysis",
    "Multi-variate testing with 3 variants",
    "Cohort analysis with segmentation",
    "Pre-post analysis with intervention",
    "User journey mapping and analysis",
    "Funnel analysis with conversion tracking",
    "Data quality audit with automated checks",
    "Campaign performance analysis with attribution modeling",
]

SUCCESS_CRITERIA = [
    "Accuracy >= 90%",
    "Engagement increase >= 15%",
    "Processing time <= 2s",
    "Success rate >= 70%",
    "Retention >= 80%",
    "Utilization >= 90%",
    "Rating >= 4.0",
    "Correlation >= 0.60",
    "Satisfaction score >= 4.2/5.0",
    "Conversion rate >= 15%",
    "Churn rate <= 5%",
    "Onboarding completion >= 80%",
    "Click-through rate >= 3.5%",
    "Data quality score >= 90%",
    "Campaign ROI >= 3.0x",
]

ANALYSIS_APPROACHES = [
    "Statistical significance testing",
    "Regression analysis",
    "Hypothesis testing with p-values",
    "Bayesian analysis",
    "Machine learning evaluation",
    "Time series analysis",
    "Comparative analysis",
    "Correlation analysis",
    "Sentiment analysis with NLP",
    "Cohort analysis with retention metrics",
    "Survival analysis for churn prediction",
    "Funnel analysis with drop-off points",
    "Clickstream analysis with heatmaps",
    "Data profiling and quality metrics",
    "Attribution modeling with multi-touch analysis",
]

EVALUATION_PLANS = [
    "Weekly reviews, monthly reports",
    "Daily monitoring, weekly analysis",
    "Bi-weekly checkpoints, final report",
    "Continuous monitoring, quarterly review",
    "Monthly assessments, annual summary",
    "Weekly metrics, monthly deep dive",
    "Daily tracking, weekly summaries",
    "Bi-weekly reviews, monthly analysis",
    "Weekly sentiment analysis, monthly trend reports",
    "Daily conversion tracking, weekly optimization",
    "Monthly churn analysis, quarterly retention review",
    "Weekly onboarding metrics, monthly cohort analysis",
    "Daily engagement tracking, weekly behavior reports",
    "Weekly data quality audits, monthly improvement reviews",
    "Daily campaign performance, weekly ROI analysis",
]


def generate_realistic_experiment(circle: str, start_date: date, lead_name: str) -> Experiment:
    """
    Generate a single realistic experiment with specified parameters.

    Args:
        circle: Circle name for the experiment
        start_date: Start date for the experiment
        lead_name: Lead name for the experiment

    Returns:
        Experiment: Single Experiment model with realistic sample data
    """
    # Calculate end_date (typically 1-3 months after start_date)
    days_duration = random.randint(30, 90)
    end_date = start_date + timedelta(days=days_duration)
    
    # Generate realistic group size (5-30 range)
    group_size = random.randint(5, 30)
    
    # Select random templates
    idx = random.randint(0, len(PROBLEM_STATEMENTS) - 1)
    
    # Always generate a display name with varied, plausible format
    month = start_date.strftime("%B")
    year = start_date.year
    quarter = (start_date.month - 1) // 3 + 1
    problem_type = PROBLEM_TYPES[idx % len(PROBLEM_TYPES)]
    
    # Select a random display name template
    template = random.choice(DISPLAY_NAME_TEMPLATES)
    display_name = template.format(
        circle=circle,
        month=month,
        year=year,
        quarter=quarter,
        problem_type=problem_type
    )
    
    return Experiment(
        display_name=display_name,
        lead_name=lead_name,
        circle=circle,
        start_date=start_date,
        end_date=end_date,
        problem_statement=PROBLEM_STATEMENTS[idx],
        baseline_statement=BASELINE_STATEMENTS[idx],
        purpose_objectives=PURPOSE_OBJECTIVES[idx],
        who_was_involved=WHO_INVOLVED[idx],
        group_size=group_size,
        method_description=METHOD_DESCRIPTIONS[idx],
        success_criteria=SUCCESS_CRITERIA[idx],
        analysis_approach=ANALYSIS_APPROACHES[idx],
        evaluation_plan=EVALUATION_PLANS[idx],
    )


def generate_realistic_experiment_with_template(
    circle: str, start_date: date, lead_name: str, template_idx: int
) -> Experiment:
    """
    Generate a single realistic experiment with specified parameters and template index.

    Args:
        circle: Circle name for the experiment
        start_date: Start date for the experiment
        lead_name: Lead name for the experiment
        template_idx: Index into the template arrays for consistent data

    Returns:
        Experiment: Single Experiment model with realistic sample data
    """
    # Calculate end_date (typically 1-3 months after start_date)
    days_duration = random.randint(30, 90)
    end_date = start_date + timedelta(days=days_duration)
    
    # Generate realistic group size (5-30 range)
    group_size = random.randint(5, 30)
    
    # Use specified template index
    idx = template_idx % len(PROBLEM_STATEMENTS)
    
    # Always generate a display name with varied, plausible format
    month = start_date.strftime("%B")
    year = start_date.year
    quarter = (start_date.month - 1) // 3 + 1
    problem_type = PROBLEM_TYPES[idx % len(PROBLEM_TYPES)]
    
    # Select a random display name template
    template = random.choice(DISPLAY_NAME_TEMPLATES)
    display_name = template.format(
        circle=circle,
        month=month,
        year=year,
        quarter=quarter,
        problem_type=problem_type
    )
    
    return Experiment(
        display_name=display_name,
        lead_name=lead_name,
        circle=circle,
        start_date=start_date,
        end_date=end_date,
        problem_statement=PROBLEM_STATEMENTS[idx],
        baseline_statement=BASELINE_STATEMENTS[idx],
        purpose_objectives=PURPOSE_OBJECTIVES[idx],
        who_was_involved=WHO_INVOLVED[idx],
        group_size=group_size,
        method_description=METHOD_DESCRIPTIONS[idx],
        success_criteria=SUCCESS_CRITERIA[idx],
        analysis_approach=ANALYSIS_APPROACHES[idx],
        evaluation_plan=EVALUATION_PLANS[idx],
    )


def generate_sample_experiments(count: int = 10) -> List[Experiment]:
    """
    Generate a list of sample experiments with realistic data.

    Args:
        count: Number of sample experiments to generate. Default: 10.

    Returns:
        List[Experiment]: List of Experiment models with sample data
    """
    experiments = []
    
    # Generate experiments spanning last 6-12 months
    base_date = date.today()
    
    # Use a set to track used combinations to ensure distinct records
    used_combinations = set()
    
    for i in range(count):
        # Vary start dates over the past 6-12 months
        days_ago = random.randint(30, 365)
        start_date = base_date - timedelta(days=days_ago)
        
        # Rotate through circles and lead names, ensuring variety
        circle = CIRCLES[i % len(CIRCLES)]
        lead_name = LEAD_NAMES[i % len(LEAD_NAMES)]
        
        # Ensure each combination is unique by varying the template index
        template_idx = i % len(PROBLEM_STATEMENTS)
        
        # Create a unique key for this combination
        combo_key = (circle, lead_name, template_idx, start_date)
        attempts = 0
        while combo_key in used_combinations and attempts < 10:
            # Vary the date slightly if combination already used
            days_ago = random.randint(30, 365)
            start_date = base_date - timedelta(days=days_ago)
            template_idx = (i + attempts) % len(PROBLEM_STATEMENTS)
            combo_key = (circle, lead_name, template_idx, start_date)
            attempts += 1
        
        used_combinations.add(combo_key)
        
        # Generate experiment with specific template
        experiment = generate_realistic_experiment_with_template(
            circle, start_date, lead_name, template_idx
        )
        experiments.append(experiment)
    
    return experiments


def load_sample_data() -> None:
    """
    Generate sample experiments and save them to the JSON file (replaces existing data).

    Raises:
        IOError: If file write fails
    """
    # Generate 10 sample experiments
    sample_experiments = generate_sample_experiments(count=10)
    
    # Save them (replaces existing data)
    save_experiments(sample_experiments)

