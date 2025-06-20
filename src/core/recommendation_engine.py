"""
Recommendation Engine
Core engine for generating data strategy recommendations
"""

import json
from typing import Dict, Any, List, Optional
from models.organization import OrganizationalInput
from models.recommendations import (
    DataStrategyRecommendation, RecommendationArea, ImplementationRoadmap,
    ResourceRequirement, RiskAssessment, PriorityLevel, ImplementationPhase
)
from core.knowledge_base import KnowledgeBaseManager
from utils.openai_client import OpenAIClient

class RecommendationEngine:
    def __init__(self):
        self.knowledge_manager = KnowledgeBaseManager()
        self.openai_client = OpenAIClient()
        
        # DMBOK area mapping
        self.dmbok_areas = {
            "data_governance": "governance_recommendations",
            "data_architecture": "architecture_recommendations", 
            "data_modeling_design": "modeling_recommendations",
            "data_storage_operations": "storage_recommendations",
            "data_security": "security_recommendations",
            "data_integration_interoperability": "integration_recommendations",
            "document_content_management": "content_recommendations",
            "data_warehousing_bi": "warehousing_recommendations",
            "metadata_management": "metadata_recommendations",
            "data_quality": "quality_recommendations"
        }
    
    def generate_comprehensive_recommendation(self, org_input: OrganizationalInput) -> DataStrategyRecommendation:
        """Generate comprehensive data strategy recommendation"""
        
        print("🔍 Analyzing organizational context...")
        
        # Get organizational context
        context = org_input.to_context_string()
        priority_areas = org_input.get_priority_areas()
        
        print(f"📊 Identified {len(priority_areas)} priority areas: {', '.join(priority_areas)}")
        
        # Retrieve relevant DMBOK knowledge
        print("🧠 Retrieving relevant DMBOK knowledge...")
        relevant_knowledge = self.knowledge_manager.search_relevant_knowledge(context, limit=10)
        
        # Generate overall recommendation
        print("🤖 Generating AI-powered recommendations...")
        overall_recommendation = self.openai_client.generate_recommendation(
            context, relevant_knowledge, priority_areas
        )
        
        # Generate area-specific recommendations
        area_recommendations = {}
        for area_id in priority_areas:
            if area_id in self.dmbok_areas:
                print(f"   📋 Generating {area_id} recommendations...")
                area_knowledge = self._get_area_knowledge(area_id, relevant_knowledge)
                if area_knowledge:
                    priority = self._determine_priority(area_id, org_input)
                    area_rec = self.openai_client.generate_area_specific_recommendation(
                        context, area_knowledge, priority
                    )
                    if area_rec:
                        area_recommendations[self.dmbok_areas[area_id]] = self._create_recommendation_area(
                            area_knowledge, area_rec, priority
                        )
        
        # Generate implementation roadmap
        print("🗺️ Creating implementation roadmap...")
        recommendation_list = list(area_recommendations.values())
        roadmap_data = self.openai_client.generate_implementation_roadmap(
            context, recommendation_list

        )
        roadmap = [self._create_roadmap_phase(phase) for phase in roadmap_data]
        
        # Generate resource requirements and risks
        print("📋 Analyzing resource requirements and risks...")
        resources = self._generate_resource_requirements(org_input, area_recommendations)
        risks = self._generate_risk_assessment(org_input, area_recommendations)
        
        # Create comprehensive recommendation
        recommendation = DataStrategyRecommendation(
            organization_name=org_input.profile.company_name,
            executive_summary=self._generate_executive_summary(org_input, area_recommendations),
            current_state_overview=self._generate_current_state_overview(org_input),
            implementation_roadmap=roadmap,
            resource_requirements=resources,
            risk_assessment=risks,
            success_metrics=self._generate_success_metrics(org_input),
            roi_expectations=self._generate_roi_expectations(org_input),
            quick_wins=self._generate_quick_wins(org_input, area_recommendations),
            long_term_vision=self._generate_long_term_vision(org_input),
            next_steps=self._generate_next_steps(org_input, area_recommendations),
            **area_recommendations
        )
        
        print("✅ Recommendation generation complete!")
        return recommendation
    
    def _get_area_knowledge(self, area_id: str, knowledge_list: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Get knowledge for specific area"""
        for knowledge in knowledge_list:
            if area_id.replace('_', ' ').lower() in knowledge['title'].lower():
                return knowledge
        return None
    
    def _determine_priority(self, area_id: str, org_input: OrganizationalInput) -> str:
        """Determine priority level for an area"""
        # High priority areas based on challenges
        high_priority_areas = {
            "data_governance": org_input.data_landscape.data_governance_maturity in ["initial", "managed"],
            "data_quality": org_input.challenges.data_quality_issues,
            "data_security": org_input.challenges.compliance_risks,
            "data_integration_interoperability": org_input.challenges.data_silos,
            "data_warehousing_bi": org_input.challenges.reporting_delays
        }
        
        if high_priority_areas.get(area_id, False):
            return "critical"
        elif area_id in org_input.get_priority_areas()[:3]:
            return "high"
        elif area_id in org_input.get_priority_areas():
            return "medium"
        else:
            return "low"
    
    def _create_recommendation_area(self, knowledge: Dict[str, Any], recommendation: Dict[str, Any], priority: str) -> RecommendationArea:
        """Create RecommendationArea from knowledge and AI recommendation"""
        return RecommendationArea(
            title=knowledge['title'],
            priority=PriorityLevel(priority),
            weight=knowledge['weight'],
            current_state_assessment=recommendation.get('current_state_assessment', ''),
            recommended_actions=recommendation.get('recommended_actions', []),
            implementation_steps=recommendation.get('implementation_steps', []),
            success_metrics=recommendation.get('success_metrics', []),
            estimated_timeline=recommendation.get('estimated_timeline', ''),
            resource_requirements=recommendation.get('resource_requirements', []),
            potential_challenges=recommendation.get('potential_challenges', []),
            quick_wins=recommendation.get('quick_wins', [])
        )
    
    def _create_roadmap_phase(self, phase_data: Dict[str, Any]) -> ImplementationRoadmap:
        """Create ImplementationRoadmap from phase data"""
        return ImplementationRoadmap(
            phase=ImplementationPhase(phase_data['phase']),
            duration=phase_data['duration'],
            objectives=phase_data['objectives'],
            key_activities=phase_data['key_activities'],
            deliverables=phase_data['deliverables'],
            success_criteria=phase_data['success_criteria'],
            dependencies=phase_data.get('dependencies', [])
        )
    
    def _generate_resource_requirements(self, org_input: OrganizationalInput, recommendations: Dict[str, Any]) -> List[ResourceRequirement]:
        """Generate resource requirements"""
        resources = []
        
        # People resources
        if org_input.technical_environment.technical_team_size and org_input.technical_environment.technical_team_size < 5:
            resources.append(ResourceRequirement(
                category="People",
                description="Data governance lead and data stewards",
                priority=PriorityLevel.HIGH,
                estimated_cost="$150K-250K annually",
                timeline="Foundation phase"
            ))
        
        # Technology resources
        if org_input.challenges.scalability_issues:
            resources.append(ResourceRequirement(
                category="Technology",
                description="Cloud data platform and integration tools",
                priority=PriorityLevel.HIGH,
                estimated_cost="$50K-200K annually",
                timeline="Core implementation phase"
            ))
        
        # Budget resources
        resources.append(ResourceRequirement(
            category="Budget",
            description="Data management initiative budget",
            priority=PriorityLevel.CRITICAL,
            estimated_cost=org_input.business_objectives.budget_constraints or "To be determined",
            timeline="Ongoing"
        ))
        
        return resources
    
    def _generate_risk_assessment(self, org_input: OrganizationalInput, recommendations: Dict[str, Any]) -> List[RiskAssessment]:
        """Generate risk assessment"""
        risks = []
        
        # Change management risk
        risks.append(RiskAssessment(
            risk_description="Resistance to new data governance processes",
            probability="Medium",
            impact="High",
            mitigation_strategies=[
                "Executive sponsorship and communication",
                "Gradual rollout with quick wins",
                "Training and support programs"
            ]
        ))
        
        # Resource risk
        if org_input.challenges.skill_gaps:
            risks.append(RiskAssessment(
                risk_description="Lack of skilled data management professionals",
                probability="High",
                impact="High",
                mitigation_strategies=[
                    "Hire experienced data professionals",
                    "Invest in training existing staff",
                    "Consider external consulting support"
                ]
            ))
        
        # Technology risk
        if org_input.challenges.scalability_issues:
            risks.append(RiskAssessment(
                risk_description="Technology platform limitations",
                probability="Medium",
                impact="Medium",
                mitigation_strategies=[
                    "Thorough technology assessment",
                    "Phased migration approach",
                    "Proof of concept validation"
                ]
            ))
        
        return risks
    
    def _generate_executive_summary(self, org_input: OrganizationalInput, recommendations: Dict[str, Any]) -> str:
        """Generate executive summary"""
        priority_count = len([r for r in recommendations.values() if r.priority in ["critical", "high"]])
        
        return f"""
        {org_input.profile.company_name} has significant opportunities to improve data management capabilities and drive business value through strategic data initiatives. 
        Our assessment identifies {priority_count} high-priority areas requiring immediate attention, with a focus on establishing strong data governance foundations and addressing critical quality issues.
        
        The recommended three-phase approach will enable {org_input.profile.company_name} to build robust data management capabilities while delivering quick wins and measurable business value. 
        Expected benefits include improved decision-making speed, enhanced operational efficiency, better regulatory compliance, and increased competitive advantage through data-driven insights.
        """
    
    def _generate_current_state_overview(self, org_input: OrganizationalInput) -> str:
        """Generate current state overview"""
        return f"""
        Current data governance maturity: {org_input.data_landscape.data_governance_maturity.value}
        Primary data sources: {', '.join(org_input.data_landscape.primary_data_sources[:3])}
        Data volume: {org_input.data_landscape.data_volume_estimate}
        Technology environment: {org_input.technical_environment.technology_environment.value}
        Key challenges: Data quality issues, manual processes, and reporting delays
        """
    
    def _generate_success_metrics(self, org_input: OrganizationalInput) -> List[str]:
        """Generate success metrics"""
        return [
            "Data quality scores improvement (target: >95%)",
            "Time to generate reports (target: 50% reduction)",
            "Data governance maturity advancement (target: next level)",
            "User satisfaction with data access (target: >80%)",
            "Compliance audit findings (target: zero critical findings)"
        ]
    
    def _generate_roi_expectations(self, org_input: OrganizationalInput) -> str:
        """Generate ROI expectations"""
        return f"""
        Expected ROI of 200-400% over 3 years through improved decision-making speed, 
        reduced manual effort, better compliance, and enhanced operational efficiency. 
        Payback period estimated at 12-18 months for {org_input.profile.company_size.value} organizations.
        """
    
    def _generate_quick_wins(self, org_input: OrganizationalInput, recommendations: Dict[str, Any]) -> List[str]:
        """Generate quick wins"""
        quick_wins = [
            "Establish data governance council with executive sponsorship",
            "Implement basic data quality monitoring for critical datasets",
            "Create data dictionary for key business terms"
        ]
        
        # Add area-specific quick wins
        for rec in recommendations.values():
            quick_wins.extend(rec.quick_wins[:2])  # Add top 2 quick wins from each area
        
        return list(set(quick_wins))  # Remove duplicates
    
    def _generate_long_term_vision(self, org_input: OrganizationalInput) -> str:
        """Generate long-term vision"""
        return f"""
        Transform {org_input.profile.company_name} into a data-driven organization where high-quality, 
        accessible data enables rapid decision-making, drives innovation, and provides sustainable competitive advantage. 
        Achieve industry-leading data management maturity with automated processes, self-service analytics, 
        and proactive data governance that supports business growth and regulatory compliance.
        """
    
    def _generate_next_steps(self, org_input: OrganizationalInput, recommendations: Dict[str, Any]) -> List[str]:
        """Generate immediate next steps"""
        return [
            "Secure executive sponsorship and budget approval",
            "Form data governance steering committee",
            "Conduct detailed current state assessment",
            "Prioritize quick wins for immediate implementation",
            "Develop detailed project plans for foundation phase",
            "Begin recruitment for key data management roles"
        ]
    
    def save_recommendation(self, recommendation: DataStrategyRecommendation, filename: str = None) -> str:
        """Save recommendation to JSON file"""
        if not filename:
            org_name = recommendation.organization_name.lower().replace(' ', '_')
            filename = f"data_strategy_recommendation_{org_name}.json"
        
        with open(filename, 'w') as f:
            json.dump(recommendation.dict(), f, indent=2)
        
        print(f"💾 Recommendation saved to {filename}")
        return filename

