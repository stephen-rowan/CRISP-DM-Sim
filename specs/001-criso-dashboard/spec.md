# Feature Specification: CRISO Analysis Dashboard

**Feature Branch**: `001-criso-dashboard`  
**Created**: 2024-12-19  
**Status**: Draft  
**Input**: User description: "Create a Streamlit app dashboard to visualize CRISO Analysis based on user completing a form template."

## Clarifications

### Session 2025-11-13

- Q: How should experiments be uniquely identified in the system? → A: UUID (universally unique identifier)
- Q: What file format should be used for persisting experiment data to local storage? → A: JSON files (one file per experiment or single JSON array file)
- Q: How should experiments be organized in JSON file storage? → A: Single JSON file containing an array of all experiments
- Q: Should the form include a separate "experiment name" field (distinct from lead name), and if so, what are the requirements? → A: Optional display name field (user can provide a friendly name for identification)
- Q: What should happen if saving experiment data to the JSON file fails (e.g., disk full, permission error, file locked)? → A: Show error message and retain form data (user can retry or copy data)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete Experiment Form and View Initial Dashboard (Priority: P1)

A user opens the Streamlit application and is presented with a form template matching the CRISO experiment documentation structure. The user fills in all required fields including experiment details (lead name, circle, dates), problem statement, baseline, objectives, design information, group details, method, success criteria, analysis approach, and evaluation plan. Upon submission, the system saves the experiment data and immediately displays a dashboard with key metrics and visualizations derived from the submitted information.

**Why this priority**: This is the core user journey - without form completion and basic visualization, the feature provides no value. This story delivers a complete end-to-end experience that can be demonstrated independently.

**Independent Test**: Can be fully tested by having a user complete the form with sample data and verifying that a dashboard appears with at least one visualization showing experiment information. This delivers immediate value by converting form data into visual insights.

**Acceptance Scenarios**:

1. **Given** a user opens the application, **When** they navigate to the form page, **Then** they see all form fields organized according to the CRISO template structure (Experiment Details, Question/Problem Statement, Baseline Statement, Purpose/Objectives, Design and Execution, Evaluation and Outcome)
2. **Given** a user has filled in all required form fields, **When** they submit the form, **Then** the system saves the data and redirects them to a dashboard view
3. **Given** a user has submitted an experiment form, **When** they view the dashboard, **Then** they see at least one visualization displaying key metrics from their experiment data
4. **Given** a user has submitted multiple experiments, **When** they view the dashboard, **Then** they can see visualizations comparing or aggregating data across experiments

---

### User Story 2 - View Historical Experiments and Comparative Analysis (Priority: P2)

A user who has previously submitted multiple experiment forms can view a list of all their experiments and select specific experiments to compare. The dashboard provides visualizations that show trends over time, compare success criteria across experiments, analyze group sizes and participation patterns, and identify common themes in problem statements or methods used.

**Why this priority**: While the first story provides core value, this story enables users to gain insights from multiple experiments, which is essential for understanding patterns and making data-driven governance decisions. This multiplies the value of the feature.

**Independent Test**: Can be fully tested by submitting 3-5 different experiment forms and verifying that the dashboard can display comparative visualizations (e.g., timeline of experiments, comparison charts, aggregated statistics). This delivers value by enabling pattern recognition across experiments.

**Acceptance Scenarios**:

1. **Given** a user has submitted multiple experiments, **When** they view the dashboard, **Then** they see a list or timeline of all their experiments with key identifiers (display name if provided, lead name, dates, circle)
2. **Given** a user views the experiment list, **When** they select one or more experiments, **Then** the dashboard updates to show visualizations specific to the selected experiments
3. **Given** a user has experiments spanning different time periods, **When** they view the dashboard, **Then** they see visualizations that show trends over time (e.g., number of experiments per month, average group sizes over time)
4. **Given** a user has experiments with different success criteria, **When** they view comparative visualizations, **Then** they can see how success criteria vary across experiments

---

### User Story 3 - Generate Sample Data and Explore Pre-populated Visualizations (Priority: P3)

A user can generate sample experiment data to explore the dashboard capabilities without manually filling forms. The system creates realistic sample experiments based on the CRISO template structure, populates the dashboard with this data, and allows users to interact with visualizations to understand what insights can be derived from experiment data.

**Why this priority**: This story enhances user onboarding and allows stakeholders to understand the dashboard's value proposition before committing real data. It also serves as a demonstration tool.

**Independent Test**: Can be fully tested by clicking a "Generate Sample Data" button and verifying that the dashboard populates with multiple sample experiments and displays various visualizations. This delivers value by enabling quick exploration and demonstration of capabilities.

**Acceptance Scenarios**:

1. **Given** a user opens the application, **When** they click a "Generate Sample Data" or "Load Sample Data" option, **Then** the system creates multiple sample experiments with realistic data across different circles, time periods, and experiment types
2. **Given** sample data has been generated, **When** the user views the dashboard, **Then** they see visualizations populated with the sample experiment data
3. **Given** sample data is displayed, **When** the user interacts with visualizations (filters, selections), **Then** the visualizations update responsively to show filtered or selected data

---

### Edge Cases

- What happens when a user submits a form with missing required fields? (System should validate and show clear error messages)
- How does the system handle very long text inputs in problem statements or methods? (Should display appropriately in visualizations, possibly with truncation and expandable views)
- What happens when a user submits an experiment with an end date before the start date? (System should validate date logic and prevent invalid submissions)
- How does the system handle experiments with zero or very large group sizes? (Visualizations should scale appropriately and handle edge values)
- What happens when no experiments have been submitted yet? (Dashboard should show an empty state with instructions to complete a form)
- How does the system handle special characters or formatting in text fields? (Should preserve and display appropriately)
- What happens when a user tries to submit duplicate experiment names? (System allows duplicate experiment names since each experiment is uniquely identified by UUID)
- What happens when saving experiment data to JSON file fails (disk full, permission error, file locked)? (System shows clear error message and retains all form data so user can retry or copy data before attempting again)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a form interface that matches the CRISO experiment template structure with all required sections (Experiment Details, Question/Problem Statement, Baseline Statement, Purpose/Objectives, Design and Execution, Evaluation and Outcome)
- **FR-002**: System MUST collect experiment lead name, circle, start date, and end date (if applicable) in the Experiment Details section. System MAY collect an optional experiment display name field for user-friendly identification.
- **FR-003**: System MUST collect problem/question statement, baseline statement, and purpose/objectives as text inputs
- **FR-004**: System MUST collect design information including who was involved, group size (number of people), and method description
- **FR-005**: System MUST collect evaluation information including success criteria, analysis approach, and evaluation plan
- **FR-006**: System MUST validate that required fields are completed before allowing form submission
- **FR-007**: System MUST validate that end date (if provided) is not before start date
- **FR-008**: System MUST persist submitted experiment data in a single JSON file (array format) to local file storage so it can be retrieved for dashboard display
- **FR-009**: System MUST display a dashboard with visualizations showing key metrics from experiment data
- **FR-010**: System MUST generate at least one visualization that displays experiment information (e.g., timeline, metrics chart, comparison view)
- **FR-011**: System MUST support viewing multiple experiments simultaneously in comparative visualizations
- **FR-012**: System MUST display experiment metadata (name, dates, circle) in dashboard views
- **FR-013**: System MUST provide a way to generate or load sample experiment data for demonstration purposes
- **FR-014**: System MUST display an appropriate empty state when no experiments have been submitted
- **FR-015**: System MUST allow users to filter or select specific experiments for focused visualization views
- **FR-016**: System MUST handle text inputs of reasonable length (at least 5000 characters per text field) without breaking visualizations

### Key Entities *(include if feature involves data)*

- **Experiment**: Represents a single CRISO experiment submission. Key attributes include: experiment display name (optional), experiment lead name, circle, start date, end date (optional), problem statement, baseline statement, purpose/objectives, design information (who was involved), group size (number of people), method description, success criteria, analysis approach, evaluation plan. Each experiment has a UUID (universally unique identifier) as its unique identifier and timestamp of submission.

- **Dashboard View**: Represents the visualization state of the dashboard. Key attributes include: selected experiments (one or more), active visualizations, filter criteria, time range. The view aggregates and presents data from one or more experiments.

- **Visualization**: Represents a specific chart or visual representation of experiment data. Key attributes include: visualization type (timeline, bar chart, comparison, etc.), data source (which experiments), metrics displayed, time range. Visualizations derive their data from experiment entities.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete and submit an experiment form in under 5 minutes when all required information is available
- **SC-002**: Dashboard visualizations render and display within 2 seconds of form submission or data load
- **SC-003**: System can display and visualize data from at least 50 experiments simultaneously without performance degradation
- **SC-004**: 90% of users can successfully complete the form and view their first dashboard visualization without assistance
- **SC-005**: Dashboard displays at least 3 distinct types of visualizations (e.g., timeline, metric comparison, distribution chart)
- **SC-006**: Sample data generation creates at least 5 realistic sample experiments that demonstrate dashboard capabilities
- **SC-007**: Users can filter or select experiments and see updated visualizations within 1 second of interaction

## Assumptions

- Users will access the application through a web browser (Streamlit's default interface)
- Experiment data will be stored locally in a single JSON file (array format) for the initial implementation
- No user authentication is required for the MVP - all users can view and submit all experiments
- Form submissions are sequential - users complete one form at a time
- Text fields can accommodate standard experiment documentation lengths (up to 5000 characters per field)
- Date inputs follow standard calendar date format (YYYY-MM-DD or similar)
- Group size is represented as a numeric value (number of people)
- The application will run on a single machine/server without distributed data requirements
- Sample data generation creates realistic but fictional experiment data for demonstration purposes

## Dependencies

- Streamlit framework must be available and properly configured
- Python environment with necessary data visualization libraries (e.g., plotly, matplotlib, pandas)
- Sufficient local storage space for experiment data files
- Web browser compatibility for Streamlit interface

## Out of Scope

- User authentication and authorization (all users have equal access)
- Data export to external formats (CSV, PDF, etc.) - may be added in future iterations
- Real-time collaboration or multi-user editing
- Integration with external data sources or APIs
- Advanced analytics or machine learning on experiment data
- Data backup and recovery mechanisms beyond local file storage
- Mobile app version or native mobile interface
- Email notifications or alerts
- Experiment editing or deletion after submission
- Version control or change history for experiment submissions
