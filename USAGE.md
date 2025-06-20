# Data Strategy Bot - Usage Examples

## Quick Start

1. **Setup the system:**
```bash
data-strategy-bot setup
```

2. **Generate recommendations:**
```bash
data-strategy-bot recommend
```

3. **Test the system:**
```bash
data-strategy-bot test
```

## Detailed Usage Examples

### Example 1: Technology Startup

**Scenario:** A 50-person SaaS startup needs data strategy guidance.

**Input Profile:**
- Company: TechStart Inc.
- Industry: Technology
- Size: Small (50-250 employees)
- Business Model: SaaS
- Data Volume: 500GB
- Governance Maturity: Initial
- Key Challenges: Data silos, manual reporting

**Expected Recommendations:**
- Priority on Data Governance (establish foundation)
- Data Quality management (address manual processes)
- Data Integration (solve silos)
- Quick wins: Data governance council, basic quality monitoring

### Example 2: Healthcare Organization

**Scenario:** A regional healthcare provider with compliance requirements.

**Input Profile:**
- Company: Regional Health System
- Industry: Healthcare
- Size: Large (1000-5000 employees)
- Regulatory: HIPAA, state regulations
- Data Volume: 10TB
- Governance Maturity: Managed
- Key Challenges: Compliance risks, data security

**Expected Recommendations:**
- Priority on Data Security and Governance
- Compliance-focused data management
- Enhanced metadata management for audit trails
- Risk mitigation strategies for healthcare data

### Example 3: Financial Services

**Scenario:** A mid-size investment firm with regulatory oversight.

**Input Profile:**
- Company: Investment Partners LLC
- Industry: Financial Services
- Size: Medium (250-1000 employees)
- Regulatory: SOX, SEC requirements
- Data Volume: 2TB
- Governance Maturity: Defined
- Key Challenges: Reporting delays, data quality

**Expected Recommendations:**
- Data Warehousing and BI improvements
- Enhanced data quality processes
- Automated reporting capabilities
- Compliance monitoring and controls

## Command Line Options

### Generate Recommendations with Options

```bash
# Generate with specific output format
data-strategy-bot recommend --format pdf

# Use saved input file
data-strategy-bot recommend --input-file my_company.json

# Specify output file
data-strategy-bot recommend --output-file my_strategy.md
```

### Analyze Saved Inputs

```bash
# Analyze a previously saved organizational profile
data-strategy-bot analyze my_company.json
```

### Test System Components

```bash
# Test all components
data-strategy-bot test

# Setup knowledge base
data-strategy-bot setup
```

## Sample Organizational Input

```json
{
  "profile": {
    "company_name": "Example Corp",
    "industry": "technology",
    "company_size": "medium",
    "business_model": "b2b",
    "geographic_presence": ["US", "Canada"],
    "regulatory_requirements": ["GDPR", "SOX"]
  },
  "data_landscape": {
    "primary_data_sources": ["CRM", "ERP", "Web Analytics"],
    "data_volume_estimate": "5TB",
    "data_types": ["Customer", "Financial", "Operational"],
    "current_data_tools": ["Salesforce", "Tableau", "MySQL"],
    "data_governance_maturity": "managed",
    "data_quality_issues": ["Duplicate records", "Missing values"],
    "compliance_challenges": ["Data retention", "Access controls"]
  },
  "business_objectives": {
    "strategic_goals": [
      "Improve customer experience",
      "Increase operational efficiency",
      "Expand to new markets"
    ],
    "key_performance_indicators": ["Customer satisfaction", "Revenue growth"],
    "digital_transformation_initiatives": ["Cloud migration", "AI implementation"]
  },
  "technical_environment": {
    "technology_environment": "hybrid",
    "cloud_providers": ["AWS"],
    "database_technologies": ["MySQL", "PostgreSQL"],
    "scalability_needs": "Expecting 50% growth in next 2 years"
  },
  "challenges": {
    "data_silos": true,
    "data_quality_issues": true,
    "manual_processes": true,
    "reporting_delays": false,
    "compliance_risks": false,
    "scalability_issues": true,
    "skill_gaps": true,
    "budget_limitations": false
  }
}
```

## Expected Output Structure

The system generates comprehensive reports including:

1. **Executive Summary** - High-level recommendations and business impact
2. **Current State Assessment** - Analysis of data management maturity
3. **Prioritized Recommendations** - DMBOK area-specific guidance
4. **Implementation Roadmap** - Three-phase implementation plan
5. **Resource Requirements** - People, technology, and budget needs
6. **Risk Assessment** - Implementation risks and mitigation strategies
7. **Success Metrics** - KPIs and ROI expectations
8. **Quick Wins** - Immediate actions for momentum
9. **Next Steps** - Specific actions for the next 30 days

## Troubleshooting

### Common Issues

1. **API Key Errors:**
   - Ensure .env file is properly configured
   - Verify API keys are valid and have sufficient credits

2. **Knowledge Base Issues:**
   - Run `data-strategy-bot setup` to initialize
   - Check Qdrant connection and API key

3. **Import Errors:**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Install package in development mode: `pip install -e .`

### Getting Help

- Run `data-strategy-bot --help` for command options
- Use `data-strategy-bot test` to verify system functionality
- Check log files for detailed error messages

