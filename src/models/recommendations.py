"""
Recommendation Models
Pydantic models for data strategy recommendations
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class PriorityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ImplementationPhase(str, Enum):
    FOUNDATION = "foundation"      # 0-6 months
    CORE = "core"                 # 6-18 months
    ADVANCED = "advanced"         # 18+ months

class RecommendationArea(BaseModel):
    """Individual recommendation for a DMBOK knowledge area"""
    title: str = Field(..., description="Knowledge area title")
    priority: PriorityLevel = Field(..., description="Priority level")
    weight: int = Field(..., description="CDMP exam weight percentage")
    current_state_assessment: str = Field(..., description="Assessment of current state")
    recommended_actions: List[str] = Field(..., description="Specific recommended actions")
    implementation_steps: List[str] = Field(..., description="Step-by-step implementation guide")
    success_metrics: List[str] = Field(..., description="Metrics to measure success")
    estimated_timeline: str = Field(..., description="Estimated implementation timeline")
    resource_requirements: List[str] = Field(..., description="Required resources")
    potential_challenges: List[str] = Field(..., description="Potential implementation challenges")
    quick_wins: List[str] = Field(default=[], description="Quick wins and early victories")

class ImplementationRoadmap(BaseModel):
    """Implementation roadmap with phases"""
    phase: ImplementationPhase = Field(..., description="Implementation phase")
    duration: str = Field(..., description="Phase duration")
    objectives: List[str] = Field(..., description="Phase objectives")
    key_activities: List[str] = Field(..., description="Key activities in this phase")
    deliverables: List[str] = Field(..., description="Expected deliverables")
    success_criteria: List[str] = Field(..., description="Success criteria for phase completion")
    dependencies: List[str] = Field(default=[], description="Dependencies on other phases or external factors")

class ResourceRequirement(BaseModel):
    """Resource requirements for implementation"""
    category: str = Field(..., description="Resource category (people, technology, budget)")
    description: str = Field(..., description="Detailed description")
    priority: PriorityLevel = Field(..., description="Priority level")
    estimated_cost: Optional[str] = Field(None, description="Estimated cost range")
    timeline: str = Field(..., description="When this resource is needed")

class RiskAssessment(BaseModel):
    """Risk assessment for implementation"""
    risk_description: str = Field(..., description="Description of the risk")
    probability: str = Field(..., description="Probability of occurrence (Low/Medium/High)")
    impact: str = Field(..., description="Impact if risk occurs (Low/Medium/High)")
    mitigation_strategies: List[str] = Field(..., description="Strategies to mitigate the risk")

class DataStrategyRecommendation(BaseModel):
    """Complete data strategy recommendation"""
    organization_name: str = Field(..., description="Organization name")
    executive_summary: str = Field(..., description="High-level summary of recommendations")
    current_state_overview: str = Field(..., description="Overview of current data management state")
    
    # Core recommendations by DMBOK area
    governance_recommendations: Optional[RecommendationArea] = None
    architecture_recommendations: Optional[RecommendationArea] = None
    modeling_recommendations: Optional[RecommendationArea] = None
    storage_recommendations: Optional[RecommendationArea] = None
    security_recommendations: Optional[RecommendationArea] = None
    integration_recommendations: Optional[RecommendationArea] = None
    content_recommendations: Optional[RecommendationArea] = None
    warehousing_recommendations: Optional[RecommendationArea] = None
    metadata_recommendations: Optional[RecommendationArea] = None
    quality_recommendations: Optional[RecommendationArea] = None
    
    # Implementation guidance
    implementation_roadmap: List[ImplementationRoadmap] = Field(..., description="Phased implementation roadmap")
    resource_requirements: List[ResourceRequirement] = Field(..., description="Required resources")
    risk_assessment: List[RiskAssessment] = Field(..., description="Implementation risks and mitigation")
    
    # Success measurement
    success_metrics: List[str] = Field(..., description="Overall success metrics")
    roi_expectations: str = Field(..., description="Expected return on investment")
    
    # Additional guidance
    quick_wins: List[str] = Field(..., description="Quick wins to build momentum")
    long_term_vision: str = Field(..., description="Long-term data strategy vision")
    next_steps: List[str] = Field(..., description="Immediate next steps")
    
    class Config:
        use_enum_values = True

    def get_priority_recommendations(self):
        """Get recommendations sorted by priority with validation"""

        # Collect all recommendation areas safely
        recommendations = []

        # List all possible recommendation attributes
        rec_attributes = [
            'governance_recommendations',
            'architecture_recommendations',
            'modeling_recommendations',
            'storage_recommendations',
            'security_recommendations',
            'integration_recommendations',
            'content_recommendations',
            'warehousing_recommendations',
            'metadata_recommendations',
            'quality_recommendations'
        ]

        # Only add valid RecommendationArea objects
        for attr_name in rec_attributes:
            if hasattr(self, attr_name):
                rec = getattr(self, attr_name)
                if rec is not None and hasattr(rec, 'title') and hasattr(rec, 'priority'):
                    recommendations.append(rec)
                elif rec is not None:
                    print(f"Warning: Invalid recommendation in {attr_name}: {type(rec)}")

        # Sort by priority
        priority_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}

        recommendations.sort(
            key=lambda x: (
                priority_order.get(x.priority.value if hasattr(x.priority, 'value') else str(x.priority).lower(), 0),
                getattr(x, 'weight', 0)
            ),
            reverse=True
        )

        return recommendations

    def get_foundation_phase_items(self) -> List[str]:
        """Get items for foundation phase (0-6 months)"""
        foundation_items = []
        
        # Add quick wins
        foundation_items.extend(self.quick_wins)
        
        # Add critical and high priority items
        for rec in self.get_priority_recommendations():
            if rec.priority in ["critical", "high"]:
                foundation_items.extend(rec.quick_wins)
        
        return foundation_items
    
    def generate_executive_summary(self) -> str:
        """Generate executive summary based on recommendations"""
        priority_areas = [rec.title for rec in self.get_priority_recommendations()[:3]]
        
        summary = f"""
        Based on our assessment of {self.organization_name}'s current data management maturity and business objectives, 
        we recommend focusing on {len(priority_areas)} key areas: {', '.join(priority_areas)}.
        
        The recommended approach follows a three-phase implementation strategy:
        1. Foundation Phase (0-6 months): Establish core governance and address critical quality issues
        2. Core Implementation Phase (6-18 months): Build robust data architecture and integration capabilities  
        3. Advanced Capabilities Phase (18+ months): Implement advanced analytics and optimization
        
        This strategy will enable {self.organization_name} to achieve better data-driven decision making, 
        improved operational efficiency, and enhanced competitive advantage through strategic data management.
        """
        
        return summary.strip()

