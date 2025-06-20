"""
Organizational Data Models
Pydantic models for organizational input validation and structure
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum

class IndustryType(str, Enum):
    FINANCIAL_SERVICES = "financial_services"
    HEALTHCARE = "healthcare"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    TECHNOLOGY = "technology"
    GOVERNMENT = "government"
    EDUCATION = "education"
    TELECOMMUNICATIONS = "telecommunications"
    ENERGY = "energy"
    TRANSPORTATION = "transportation"
    OTHER = "other"

class CompanySize(str, Enum):
    STARTUP = "startup"  # < 50 employees
    SMALL = "small"      # 50-250 employees
    MEDIUM = "medium"    # 250-1000 employees
    LARGE = "large"      # 1000-5000 employees
    ENTERPRISE = "enterprise"  # > 5000 employees

class BusinessModel(str, Enum):
    B2B = "b2b"
    B2C = "b2c"
    B2G = "b2g"
    B2B2C = "b2b2c"
    MARKETPLACE = "marketplace"
    SAAS = "saas"
    OTHER = "other"

class DataMaturityLevel(str, Enum):
    INITIAL = "initial"        # Ad-hoc, reactive
    MANAGED = "managed"        # Some processes defined
    DEFINED = "defined"        # Standardized processes
    QUANTITATIVELY_MANAGED = "quantitatively_managed"  # Measured and controlled
    OPTIMIZING = "optimizing"  # Continuous improvement

class TechnologyEnvironment(str, Enum):
    ON_PREMISE = "on_premise"
    CLOUD = "cloud"
    HYBRID = "hybrid"
    MULTI_CLOUD = "multi_cloud"

class OrganizationalProfile(BaseModel):
    """Basic organizational information"""
    company_name: str = Field(..., description="Company name")
    industry: IndustryType = Field(..., description="Primary industry sector")
    company_size: CompanySize = Field(..., description="Company size category")
    business_model: BusinessModel = Field(..., description="Primary business model")
    geographic_presence: List[str] = Field(default=[], description="Countries/regions of operation")
    annual_revenue_range: Optional[str] = Field(None, description="Annual revenue range")
    regulatory_requirements: List[str] = Field(default=[], description="Key regulatory requirements (GDPR, HIPAA, SOX, etc.)")

class CurrentDataLandscape(BaseModel):
    """Current data management state"""
    primary_data_sources: List[str] = Field(default=[], description="Main data sources (CRM, ERP, databases, etc.)")
    data_volume_estimate: str = Field(..., description="Estimated data volume (GB, TB, PB)")
    data_types: List[str] = Field(default=[], description="Types of data (customer, financial, operational, etc.)")
    current_data_tools: List[str] = Field(default=[], description="Current data management tools")
    data_governance_maturity: DataMaturityLevel = Field(..., description="Current data governance maturity")
    data_quality_issues: List[str] = Field(default=[], description="Known data quality issues")
    compliance_challenges: List[str] = Field(default=[], description="Current compliance challenges")

class BusinessObjectives(BaseModel):
    """Business goals and objectives"""
    strategic_goals: List[str] = Field(..., description="Top 3-5 strategic business goals")
    key_performance_indicators: List[str] = Field(default=[], description="Key business KPIs")
    digital_transformation_initiatives: List[str] = Field(default=[], description="Current or planned digital initiatives")
    data_driven_decisions: List[str] = Field(default=[], description="Areas where better data could improve decisions")
    competitive_advantages: List[str] = Field(default=[], description="Desired competitive advantages from data")
    budget_constraints: Optional[str] = Field(None, description="Budget range for data initiatives")

class TechnicalEnvironment(BaseModel):
    """Technical infrastructure and requirements"""
    technology_environment: TechnologyEnvironment = Field(..., description="Primary technology environment")
    cloud_providers: List[str] = Field(default=[], description="Cloud providers in use")
    database_technologies: List[str] = Field(default=[], description="Database technologies in use")
    integration_requirements: List[str] = Field(default=[], description="Key integration requirements")
    security_requirements: List[str] = Field(default=[], description="Security and compliance requirements")
    scalability_needs: str = Field(..., description="Expected growth and scalability needs")
    technical_team_size: Optional[int] = Field(None, description="Size of technical team")

class DataChallenges(BaseModel):
    """Current data challenges and pain points"""
    data_silos: bool = Field(default=False, description="Data silos exist across departments")
    data_quality_issues: bool = Field(default=False, description="Significant data quality problems")
    manual_processes: bool = Field(default=False, description="Heavy reliance on manual data processes")
    reporting_delays: bool = Field(default=False, description="Delays in reporting and analytics")
    compliance_risks: bool = Field(default=False, description="Compliance and regulatory risks")
    scalability_issues: bool = Field(default=False, description="Current systems don't scale")
    skill_gaps: bool = Field(default=False, description="Lack of data management skills")
    budget_limitations: bool = Field(default=False, description="Limited budget for data initiatives")

class OrganizationalInput(BaseModel):
    """Complete organizational input model"""
    profile: OrganizationalProfile
    data_landscape: CurrentDataLandscape
    business_objectives: BusinessObjectives
    technical_environment: TechnicalEnvironment
    challenges: DataChallenges
    additional_context: Optional[str] = Field(None, description="Any additional context or specific requirements")
    
    class Config:
        use_enum_values = True
        
    def to_context_string(self) -> str:
        """Convert to a comprehensive context string for AI processing"""
        context = f"""
        Organization: {self.profile.company_name}
        Industry: {self.profile.industry}
        Size: {self.profile.company_size}
        Business Model: {self.profile.business_model}
        Geographic Presence: {', '.join(self.profile.geographic_presence)}
        Regulatory Requirements: {', '.join(self.profile.regulatory_requirements)}
        
        Data Landscape:
        - Data Sources: {', '.join(self.data_landscape.primary_data_sources)}
        - Data Volume: {self.data_landscape.data_volume_estimate}
        - Data Types: {', '.join(self.data_landscape.data_types)}
        - Current Tools: {', '.join(self.data_landscape.current_data_tools)}
        - Governance Maturity: {self.data_landscape.data_governance_maturity}
        - Quality Issues: {', '.join(self.data_landscape.data_quality_issues)}
        
        Business Objectives:
        - Strategic Goals: {', '.join(self.business_objectives.strategic_goals)}
        - KPIs: {', '.join(self.business_objectives.key_performance_indicators)}
        - Digital Initiatives: {', '.join(self.business_objectives.digital_transformation_initiatives)}
        
        Technical Environment:
        - Environment: {self.technical_environment.technology_environment}
        - Cloud Providers: {', '.join(self.technical_environment.cloud_providers)}
        - Databases: {', '.join(self.technical_environment.database_technologies)}
        - Scalability Needs: {self.technical_environment.scalability_needs}
        
        Key Challenges:
        - Data Silos: {self.challenges.data_silos}
        - Quality Issues: {self.challenges.data_quality_issues}
        - Manual Processes: {self.challenges.manual_processes}
        - Reporting Delays: {self.challenges.reporting_delays}
        - Compliance Risks: {self.challenges.compliance_risks}
        - Scalability Issues: {self.challenges.scalability_issues}
        - Skill Gaps: {self.challenges.skill_gaps}
        
        Additional Context: {self.additional_context or 'None provided'}
        """
        return context.strip()
    
    def get_priority_areas(self) -> List[str]:
        """Determine priority DMBOK areas based on input"""
        priorities = []
        
        # High priority areas based on challenges
        if self.challenges.data_quality_issues:
            priorities.append("data_quality")
        if self.challenges.data_silos or self.challenges.manual_processes:
            priorities.append("data_integration_interoperability")
        if self.challenges.compliance_risks:
            priorities.append("data_governance")
            priorities.append("data_security")
        if self.challenges.reporting_delays:
            priorities.append("data_warehousing_bi")
        if self.challenges.scalability_issues:
            priorities.append("data_architecture")
            priorities.append("data_storage_operations")
        
        # Add governance if maturity is low
        if self.data_landscape.data_governance_maturity in ["initial", "managed"]:
            if "data_governance" not in priorities:
                priorities.append("data_governance")
        
        # Add metadata management for discovery issues
        if self.challenges.data_silos:
            priorities.append("metadata_management")
        
        # Add modeling if in growth phase
        if self.profile.company_size in ["startup", "small"] and "growth" in self.technical_environment.scalability_needs.lower():
            priorities.append("data_modeling_design")
        
        return priorities

