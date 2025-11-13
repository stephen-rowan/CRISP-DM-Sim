# Tasks: CRISP Analysis Dashboard

**Input**: Design documents from `/specs/001-criso-dashboard/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included based on 80% coverage target specified in plan.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths follow plan.md structure: `src/models/`, `src/services/`, `src/pages/`, `data/`, `tests/unit/`, `tests/integration/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in repository root
- [X] T002 Create requirements.txt with dependencies: streamlit>=1.28.0, pandas>=2.0.0, plotly>=5.17.0, pydantic>=2.0.0, python-dateutil>=2.8.0, pytest>=7.4.0, pytest-cov>=4.1.0, pytest-mock>=3.12.0
- [X] T003 [P] Create src/ directory structure: src/models/, src/services/, src/pages/
- [X] T004 [P] Create tests/ directory structure: tests/unit/, tests/integration/
- [X] T005 [P] Create data/ directory and initialize data/experiments.json as empty array []
- [X] T006 [P] Create README.md with setup instructions from quickstart.md
- [X] T007 [P] Create .gitignore file for Python project (venv/, __pycache__/, *.pyc, data/*.json backup files)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 Create Experiment Pydantic model in src/models/experiment.py with all fields from data-model.md (id, created_at, display_name, lead_name, circle, start_date, end_date, problem_statement, baseline_statement, purpose_objectives, who_was_involved, group_size, method_description, success_criteria, analysis_approach, evaluation_plan)
- [X] T009 [P] Create FilterCriteria Pydantic model in src/models/experiment.py for dashboard filtering (circles, date_range_start, date_range_end, lead_names)
- [X] T010 Implement Storage Service load_experiments() in src/services/storage.py to load all experiments from data/experiments.json
- [X] T011 Implement Storage Service save_experiment() in src/services/storage.py to append single experiment to data/experiments.json with atomic write
- [X] T012 Implement Storage Service save_experiments() in src/services/storage.py to replace all experiments in data/experiments.json
- [X] T013 [P] Implement Storage Service experiment_exists() in src/services/storage.py to check if experiment ID exists
- [X] T014 [P] Implement Storage Service get_experiment_by_id() in src/services/storage.py to retrieve experiment by UUID
- [X] T015 Create main Streamlit app entry point in src/app.py with page routing structure
- [X] T016 [P] Configure pytest.ini or pyproject.toml for test configuration and coverage settings

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Complete Experiment Form and View Initial Dashboard (Priority: P1) 🎯 MVP

**Goal**: User completes CRISP experiment form and immediately sees dashboard with at least one visualization showing experiment information.

**Independent Test**: Submit a form with sample data and verify dashboard appears with at least one visualization displaying experiment information. This delivers immediate value by converting form data into visual insights.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T017 [P] [US1] Unit test for Experiment model validation in tests/unit/test_models.py (required fields, date logic, character limits)
- [X] T018 [P] [US1] Unit test for Storage Service load_experiments() in tests/unit/test_storage.py (empty file, valid data, corrupted JSON handling)
- [X] T019 [P] [US1] Unit test for Storage Service save_experiment() in tests/unit/test_storage.py (append operation, atomic write, error handling)
- [X] T020 [P] [US1] Unit test for form validation in tests/unit/test_form_validation.py (required fields, date logic, character limits)
- [X] T021 [US1] Integration test for form submission flow in tests/integration/test_form_flow.py (form → validation → save → dashboard display)

### Implementation for User Story 1

- [X] T022 [US1] Implement form UI render_form() in src/pages/form_page.py with all CRISP template sections (Experiment Details, Question/Problem Statement, Baseline Statement, Purpose/Objectives, Design and Execution, Evaluation and Outcome)
- [X] T023 [US1] Implement form validation validate_form_data() in src/pages/form_page.py (required fields, date logic, character limits)
- [X] T024 [US1] Implement create_experiment_from_form() in src/pages/form_page.py to convert form data to Experiment model with UUID and timestamp
- [X] T025 [US1] Integrate form submission with Storage Service save_experiment() in src/pages/form_page.py
- [X] T026 [US1] Implement create_timeline_chart() in src/services/visualization.py to show experiments over time using Plotly
- [X] T027 [US1] Implement dashboard page render_dashboard() in src/pages/dashboard_page.py to display timeline visualization
- [X] T028 [US1] Connect form page to dashboard page navigation in src/pages/form_page.py (redirect after successful submission)
- [X] T029 [US1] Implement empty state handling in src/pages/dashboard_page.py when no experiments exist (show message with link to form)
- [X] T030 [US1] Add error handling for form submission failures in src/pages/form_page.py (show error message, retain form data)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. User can complete form and view dashboard with timeline visualization.

---

## Phase 4: User Story 2 - View Historical Experiments and Comparative Analysis (Priority: P2)

**Goal**: User can view list of all experiments, select specific experiments, and see comparative visualizations showing trends, success criteria comparisons, group size patterns, and common themes.

**Independent Test**: Submit 3-5 different experiment forms and verify dashboard displays comparative visualizations (timeline, comparison charts, aggregated statistics). This delivers value by enabling pattern recognition across experiments.

### Tests for User Story 2

- [X] T031 [P] [US2] Unit test for create_comparison_chart() in tests/unit/test_visualization.py (bar chart with multiple experiments, grouping by circle)
- [X] T032 [P] [US2] Unit test for create_distribution_chart() in tests/unit/test_visualization.py (histogram for numeric fields, bar chart for categorical)
- [X] T033 [P] [US2] Unit test for filter_experiments() in tests/unit/test_visualization.py (circle filter, date range filter, lead name filter)
- [X] T034 [P] [US2] Unit test for get_experiment_summary_stats() in tests/unit/test_visualization.py (total count, average group size, date range, circle distribution)
- [X] T035 [US2] Integration test for comparative analysis flow in tests/integration/test_comparative_analysis.py (load multiple experiments → filter → display comparisons)

### Implementation for User Story 2

- [X] T036 [US2] Implement create_comparison_chart() in src/services/visualization.py to compare metrics across selected experiments using Plotly bar charts
- [X] T037 [US2] Implement create_distribution_chart() in src/services/visualization.py to show distribution of fields (group_size, circle) using Plotly
- [X] T038 [US2] Implement create_circle_distribution_chart() in src/services/visualization.py to show experiment count per circle using Plotly pie/bar chart
- [X] T039 [US2] Implement filter_experiments() in src/services/visualization.py to filter experiments by FilterCriteria (circles, date range, lead names)
- [X] T040 [US2] Implement get_experiment_summary_stats() in src/services/visualization.py to calculate summary statistics (total count, avg group size, date range, circle distribution, monthly counts)
- [X] T041 [US2] Add experiment list/timeline display in src/pages/dashboard_page.py showing all experiments with key identifiers (display_name, lead_name, dates, circle)
- [X] T042 [US2] Add experiment selection UI in src/pages/dashboard_page.py (multi-select or checkboxes) to allow selecting specific experiments for comparison
- [X] T043 [US2] Add filter controls in src/pages/dashboard_page.py (circle filter, date range picker, lead name filter)
- [X] T044 [US2] Update dashboard to display comparison chart when multiple experiments selected in src/pages/dashboard_page.py
- [X] T045 [US2] Update dashboard to display distribution charts in src/pages/dashboard_page.py (group size distribution, circle distribution)
- [X] T046 [US2] Add summary statistics display in src/pages/dashboard_page.py showing key metrics (total experiments, average group size, date range)
- [X] T047 [US2] Implement responsive visualization updates in src/pages/dashboard_page.py (update within 1 second of filter/selection change per SC-007)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. User can view historical experiments, filter, select, and see comparative visualizations.

---

## Phase 5: User Story 3 - Generate Sample Data and Explore Pre-populated Visualizations (Priority: P3)

**Goal**: User can generate realistic sample experiment data to explore dashboard capabilities without manually filling forms. System creates 5+ sample experiments and populates dashboard for demonstration.

**Independent Test**: Click "Generate Sample Data" button and verify dashboard populates with multiple sample experiments displaying various visualizations. This delivers value by enabling quick exploration and demonstration of capabilities.

### Tests for User Story 3

- [X] T048 [P] [US3] Unit test for generate_sample_experiments() in tests/unit/test_sample_data.py (generates correct count, all experiments valid, varied data)
- [X] T049 [P] [US3] Unit test for generate_realistic_experiment() in tests/unit/test_sample_data.py (realistic data, valid dates, coherent text fields)
- [X] T050 [P] [US3] Unit test for load_sample_data() in tests/unit/test_sample_data.py (replaces existing data, saves correctly)
- [X] T051 [US3] Integration test for sample data generation flow in tests/integration/test_sample_data_flow.py (generate → save → load → display in dashboard)

### Implementation for User Story 3

- [X] T052 [US3] Implement generate_realistic_experiment() in src/services/sample_data.py to create single realistic experiment with specified circle, start_date, lead_name
- [X] T053 [US3] Implement generate_sample_experiments() in src/services/sample_data.py to generate list of sample experiments (default 5, varied circles, time periods, group sizes, problem statements)
- [X] T054 [US3] Implement load_sample_data() in src/services/sample_data.py to generate and save sample experiments using save_experiments() (replaces existing data)
- [X] T055 [US3] Add "Generate Sample Data" button in src/pages/dashboard_page.py with confirmation dialog (warning: replaces existing data)
- [X] T056 [US3] Integrate sample data generation with dashboard refresh in src/pages/dashboard_page.py (after generation, reload and display visualizations)
- [X] T057 [US3] Add success message after sample data generation in src/pages/dashboard_page.py

**Checkpoint**: All user stories should now be independently functional. User can generate sample data and explore all dashboard visualizations.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T058 [P] Add Streamlit caching for load_experiments() in src/services/storage.py using @st.cache_data decorator
- [ ] T059 [P] Add Streamlit caching for visualization generation in src/services/visualization.py using @st.cache_data decorator
- [ ] T060 [P] Performance optimization: Ensure dashboard renders within 2 seconds per SC-002 in src/pages/dashboard_page.py
- [ ] T061 [P] Performance optimization: Ensure visualization updates within 1 second per SC-007 in src/pages/dashboard_page.py
- [X] T062 [P] Add comprehensive error handling for file I/O errors in src/services/storage.py (disk full, permission errors, file locked)
- [ ] T063 [P] Add logging for experiment operations in src/services/storage.py and src/pages/form_page.py
- [ ] T064 [P] Add character count indicators for text areas in src/pages/form_page.py (optional enhancement per form-service.md)
- [X] T065 [P] Improve empty state messaging in src/pages/dashboard_page.py with clear instructions
- [ ] T066 [P] Add validation for 50+ experiments performance per SC-003 (load and render test)
- [X] T067 [P] Update README.md with complete usage instructions from quickstart.md
- [ ] T068 [P] Run quickstart.md validation: Verify all setup steps work correctly
- [X] T069 [P] Code cleanup and refactoring: Review all code for consistency and best practices
- [X] T070 [P] Ensure 80% test coverage target per plan.md (run pytest --cov and verify coverage)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for basic dashboard structure but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1/US2 for dashboard display but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints/UI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T007)
- All Foundational tasks marked [P] can run in parallel within Phase 2 (T009, T013-T014, T016)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for Experiment model validation in tests/unit/test_models.py"
Task: "Unit test for Storage Service load_experiments() in tests/unit/test_storage.py"
Task: "Unit test for Storage Service save_experiment() in tests/unit/test_storage.py"
Task: "Unit test for form validation in tests/unit/test_form_validation.py"

# After tests are written and failing, launch implementation:
Task: "Implement form UI render_form() in src/pages/form_page.py"
Task: "Implement create_timeline_chart() in src/services/visualization.py"
```

---

## Parallel Example: User Story 2

```bash
# Launch all visualization tests together:
Task: "Unit test for create_comparison_chart() in tests/unit/test_visualization.py"
Task: "Unit test for create_distribution_chart() in tests/unit/test_visualization.py"
Task: "Unit test for filter_experiments() in tests/unit/test_visualization.py"
Task: "Unit test for get_experiment_summary_stats() in tests/unit/test_visualization.py"

# Launch visualization implementations together (after tests):
Task: "Implement create_comparison_chart() in src/services/visualization.py"
Task: "Implement create_distribution_chart() in src/services/visualization.py"
Task: "Implement create_circle_distribution_chart() in src/services/visualization.py"
Task: "Implement filter_experiments() in src/services/visualization.py"
Task: "Implement get_experiment_summary_stats() in src/services/visualization.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Submit form with sample data
   - Verify dashboard appears with timeline visualization
   - Verify data persists in data/experiments.json
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
   - Form submission and basic dashboard
3. Add User Story 2 → Test independently → Deploy/Demo
   - Comparative analysis and filtering
4. Add User Story 3 → Test independently → Deploy/Demo
   - Sample data generation
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (form + basic dashboard)
   - Developer B: User Story 2 (comparative visualizations) - can start after US1 basic structure
   - Developer C: User Story 3 (sample data) - can start after US1/US2 dashboard
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All file paths are relative to repository root
- Follow Pydantic validation patterns from data-model.md
- Follow contract specifications from contracts/ directory
- Performance targets: SC-002 (2s render), SC-007 (1s update), SC-003 (50+ experiments)

