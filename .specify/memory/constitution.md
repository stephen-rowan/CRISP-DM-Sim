<!--
Sync Impact Report:
Version change: [NONE] → 1.0.0
Modified principles: N/A (initial creation)
Added sections: CRISP-DM Framework Requirements
Removed sections: N/A
Templates requiring updates:
  ✅ plan-template.md - Constitution Check section already references constitution
  ✅ spec-template.md - No direct constitution references, structure compatible
  ✅ tasks-template.md - No direct constitution references, structure compatible
Follow-up TODOs: None
-->

# CRISP-DM-Sim Constitution

## Core Principles

### I. CRISP-DM Framework Adherence (NON-NEGOTIABLE)

All data mining and analytics projects MUST follow the six-phase CRISP-DM framework structure. Each phase must be explicitly documented, with clear deliverables and phase transitions. Projects cannot skip phases or combine phases without explicit justification. The framework ensures systematic, transparent, and reproducible data science workflows.

**Rationale**: CRISP-DM provides a proven, industry-standard methodology that ensures comprehensive coverage of all aspects of data mining projects, from business understanding through deployment. Adherence prevents critical gaps in analysis, ensures stakeholder alignment, and facilitates knowledge transfer.

### II. Phase Documentation Requirements

Each CRISP-DM phase MUST produce documented deliverables before proceeding to the next phase. Documentation must include: phase objectives, activities performed, data sources used, decisions made, issues encountered, and outcomes. Phase transitions require explicit approval or checkpoint validation.

**Rationale**: Comprehensive documentation ensures project continuity, enables reproducibility, supports knowledge transfer, and provides audit trails for decision-making processes.

### III. Iterative Process Acknowledgment

The CRISP-DM framework acknowledges that phases may be revisited iteratively. Projects MUST document when and why phases are revisited, maintaining a clear audit trail of the iterative process. Phase revisits must be justified based on new insights, data quality issues, or business requirement changes.

**Rationale**: Data mining is inherently iterative. Explicit documentation of iterations prevents circular work, ensures learning is captured, and maintains project momentum while allowing necessary refinements.

### IV. Stakeholder Engagement

Stakeholder involvement is REQUIRED during Business Understanding and Evaluation phases. Projects MUST document stakeholder input, decisions, and approval points. Business objectives and success criteria must be explicitly defined with stakeholder agreement before proceeding to Data Understanding.

**Rationale**: Stakeholder alignment ensures projects deliver business value, prevents scope creep, and ensures evaluation criteria match business needs. Early engagement prevents costly rework in later phases.

### V. Data Quality Standards

Data quality assessment MUST be performed during Data Understanding and Data Preparation phases. Projects MUST document data quality issues, data cleaning procedures, and quality metrics. Data quality standards must be established and validated before Modeling phase begins.

**Rationale**: Data quality directly impacts model reliability and business outcomes. Explicit quality standards prevent garbage-in-garbage-out scenarios and ensure downstream phases work with reliable data.

### VI. Model Validation and Evaluation

Model validation MUST be performed during Modeling and Evaluation phases using appropriate techniques for the problem domain. Projects MUST document validation methodology, performance metrics, and model selection rationale. Evaluation MUST assess both technical performance and business objective alignment.

**Rationale**: Rigorous validation ensures models are reliable, generalizable, and meet business objectives. Without proper validation, deployed models may fail in production or provide misleading insights.

## CRISP-DM Framework Requirements

### Phase 1: Business Understanding

**MUST Requirements**:
- Define project objectives from business perspective
- Assess current situation including resources, constraints, and requirements
- Translate business objectives into data mining problem definition
- Establish success criteria aligned with business objectives
- Create preliminary project plan with phase timelines
- Document stakeholder roles and responsibilities
- Obtain stakeholder approval before proceeding to Data Understanding

**Deliverables**:
- Business objectives document
- Data mining problem definition
- Success criteria specification
- Preliminary project plan
- Stakeholder approval record

### Phase 2: Data Understanding

**MUST Requirements**:
- Collect initial data from identified sources
- Describe data structure, format, and volume
- Explore data to identify interesting subsets and patterns
- Assess data quality including completeness, correctness, and consistency
- Document data quality issues and their potential impact
- Verify data relevance to business objectives
- Document data sources, collection methods, and access procedures

**Deliverables**:
- Data collection report
- Data description document
- Data exploration findings
- Data quality assessment report
- Data source inventory

### Phase 3: Data Preparation

**MUST Requirements**:
- Select relevant data subsets for modeling
- Clean data to address quality issues identified in Data Understanding
- Construct derived attributes or features as needed
- Integrate data from multiple sources if applicable
- Format data appropriately for selected modeling tools
- Document all data transformations and their rationale
- Validate prepared dataset quality before Modeling phase

**Deliverables**:
- Data selection criteria and rationale
- Data cleaning procedures and results
- Feature engineering documentation
- Final dataset specification
- Data transformation log

### Phase 4: Modeling

**MUST Requirements**:
- Select appropriate modeling techniques based on problem type and data characteristics
- Build models using selected techniques
- Calibrate model parameters to optimal values
- Assess model performance using appropriate metrics
- Document model selection rationale
- Compare multiple modeling approaches if applicable
- Document model assumptions and limitations

**Deliverables**:
- Model selection rationale
- Model specifications and parameters
- Model performance assessment results
- Model comparison analysis (if multiple models)
- Model assumptions and limitations document

### Phase 5: Evaluation

**MUST Requirements**:
- Evaluate model results against business objectives and success criteria
- Review entire process for lessons learned
- Assess model reliability and generalizability
- Determine if model meets business requirements
- Document evaluation findings and recommendations
- Obtain stakeholder review and approval
- Decide on next steps: deployment, iteration, or project termination

**Deliverables**:
- Model evaluation report
- Business objective alignment assessment
- Process review and lessons learned
- Recommendations document
- Stakeholder approval record
- Next steps decision document

### Phase 6: Deployment

**MUST Requirements**:
- Develop deployment plan including integration approach
- Implement model into operational environment
- Create monitoring procedures for model performance
- Establish maintenance procedures and schedules
- Document deployment process and operational procedures
- Provide user training and documentation if applicable
- Plan for model updates and versioning

**Deliverables**:
- Deployment plan
- Operational model implementation
- Monitoring procedures and dashboards
- Maintenance procedures
- User documentation and training materials
- Model versioning strategy

## Development Workflow

### Phase Gate Reviews

Projects MUST conduct phase gate reviews before transitioning between CRISP-DM phases. Gate reviews validate phase completion, review deliverables, and approve progression to the next phase. Gate reviews must be documented with approval records.

### Documentation Standards

All CRISP-DM phase documentation MUST be maintained in the project repository. Documentation structure should align with CRISP-DM phases. Documentation must be version-controlled and accessible to all project stakeholders.

### Quality Assurance

Data quality checks MUST be performed at multiple stages: initial data collection, after data preparation, and before final model deployment. Quality metrics must be documented and tracked throughout the project lifecycle.

## Governance

This constitution supersedes all other development practices and project guidelines. All projects within CRISP-DM-Sim MUST comply with CRISP-DM framework requirements as specified in this constitution.

**Amendment Procedure**: Constitution amendments require documentation of rationale, impact assessment on existing projects, and approval from project maintainers. Amendments that change CRISP-DM phase requirements are considered MAJOR version changes.

**Versioning Policy**: Constitution versions follow semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Backward incompatible changes to CRISP-DM requirements or core principles
- MINOR: New requirements added, new sections added, or material expansions to existing guidance
- PATCH: Clarifications, wording improvements, typo fixes, non-semantic refinements

**Compliance Review**: All project plans, specifications, and implementations must verify compliance with this constitution. The Constitution Check section in implementation plans serves as a mandatory gate before project execution begins.

**Version**: 1.0.0 | **Ratified**: 2025-11-13 | **Last Amended**: 2025-11-13
