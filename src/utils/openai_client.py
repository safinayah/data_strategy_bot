"""
OpenAI Client
Handles OpenAI API interactions for generating recommendations
"""

import os
import json
from typing import Dict, Any, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4"
        self.max_tokens = int(os.getenv("MAX_TOKENS", 4000))
        self.temperature = float(os.getenv("TEMPERATURE", 0.7))
    
    def generate_recommendation(self, 
                              organizational_context: str, 
                              dmbok_knowledge: List[Dict[str, Any]], 
                              focus_areas: List[str] = None) -> str:
        """Generate data strategy recommendation using OpenAI"""
        
        # Build knowledge context
        knowledge_context = self._build_knowledge_context(dmbok_knowledge)
        
        # Create comprehensive prompt
        prompt = self._create_recommendation_prompt(
            organizational_context, 
            knowledge_context, 
            focus_areas
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating recommendation: {e}")
            return None
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for data strategy recommendations"""
        return """
        You are a senior data strategy consultant with expertise in the DAMA-DMBOK framework and CDMP certification. 
        Your role is to analyze organizational information and generate comprehensive, actionable data strategy recommendations.
        
        Key principles:
        1. Base recommendations on DMBOK best practices and industry standards
        2. Prioritize recommendations based on organizational maturity and business needs
        3. Provide specific, actionable guidance with clear implementation steps
        4. Consider resource constraints and practical implementation challenges
        5. Focus on business value and ROI
        6. Use professional, clear language suitable for executive audiences
        
        Structure your recommendations to include:
        - Current state assessment
        - Prioritized recommendations by DMBOK knowledge area
        - Implementation roadmap with phases
        - Resource requirements and timeline estimates
        - Risk assessment and mitigation strategies
        - Success metrics and expected outcomes
        """
    
    def _build_knowledge_context(self, dmbok_knowledge: List[Dict[str, Any]]) -> str:
        """Build context from DMBOK knowledge"""
        context_parts = []
        
        for knowledge in dmbok_knowledge:
            context_part = f"""
            {knowledge['title']} (Priority Weight: {knowledge['weight']}%):
            Description: {knowledge['description']}
            
            Key Concepts: {', '.join(knowledge['key_concepts'])}
            
            Best Practices:
            {chr(10).join(f"- {practice}" for practice in knowledge['best_practices'])}
            
            Implementation Steps:
            {chr(10).join(f"{i+1}. {step}" for i, step in enumerate(knowledge['implementation_steps']))}
            
            Common Challenges: {', '.join(knowledge['common_challenges'])}
            Success Metrics: {', '.join(knowledge['success_metrics'])}
            """
            context_parts.append(context_part.strip())
        
        return "\n\n".join(context_parts)
    
    def _create_recommendation_prompt(self, 
                                    organizational_context: str, 
                                    knowledge_context: str, 
                                    focus_areas: List[str] = None) -> str:
        """Create comprehensive recommendation prompt"""
        
        focus_instruction = ""
        if focus_areas:
            focus_instruction = f"\nPay special attention to these priority areas: {', '.join(focus_areas)}"
        
        prompt = f"""
        Please analyze the following organizational information and generate a comprehensive data strategy recommendation 
        based on the DMBOK framework and best practices.
        
        ORGANIZATIONAL CONTEXT:
        {organizational_context}
        
        RELEVANT DMBOK KNOWLEDGE AREAS:
        {knowledge_context}
        {focus_instruction}
        
        Please provide a detailed data strategy recommendation that includes:
        
        1. EXECUTIVE SUMMARY (2-3 paragraphs)
        - High-level assessment and key recommendations
        - Expected business impact and value proposition
        
        2. CURRENT STATE ASSESSMENT
        - Analysis of current data management maturity
        - Key strengths and gaps identified
        - Critical challenges that need immediate attention
        
        3. PRIORITIZED RECOMMENDATIONS BY DMBOK AREA
        For each relevant knowledge area, provide:
        - Current state assessment
        - Specific recommended actions
        - Implementation steps (3-5 key steps)
        - Success metrics
        - Estimated timeline
        - Resource requirements
        - Potential challenges and mitigation strategies
        - Quick wins (if applicable)
        
        4. IMPLEMENTATION ROADMAP
        Structure recommendations into three phases:
        - Foundation Phase (0-6 months): Critical foundations and quick wins
        - Core Implementation Phase (6-18 months): Major capabilities and processes
        - Advanced Capabilities Phase (18+ months): Optimization and advanced features
        
        For each phase, specify:
        - Key objectives
        - Major activities and deliverables
        - Success criteria
        - Dependencies
        
        5. RESOURCE REQUIREMENTS
        - People (roles, skills, team size)
        - Technology (tools, platforms, infrastructure)
        - Budget considerations (high-level estimates)
        
        6. RISK ASSESSMENT
        - Key implementation risks
        - Probability and impact assessment
        - Mitigation strategies
        
        7. SUCCESS METRICS AND ROI
        - Key performance indicators
        - Expected return on investment
        - Timeline for realizing benefits
        
        8. NEXT STEPS
        - Immediate actions (next 30 days)
        - Key decisions needed
        - Stakeholder engagement requirements
        
        Format the response as a professional consulting report with clear sections and actionable recommendations.
        Use bullet points and numbered lists for clarity. Avoid technical jargon and focus on business value.
        """
        
        return prompt.strip()
    
    def generate_area_specific_recommendation(self, 
                                            organizational_context: str,
                                            knowledge_area: Dict[str, Any],
                                            priority_level: str) -> Dict[str, Any]:
        """Generate recommendation for a specific DMBOK area"""
        
        prompt = f"""
        Generate a detailed recommendation for {knowledge_area['title']} based on the following organizational context.
        This area has been identified as {priority_level} priority.
        
        ORGANIZATIONAL CONTEXT:
        {organizational_context}
        
        KNOWLEDGE AREA DETAILS:
        {knowledge_area['description']}
        
        Best Practices: {', '.join(knowledge_area['best_practices'])}
        Implementation Steps: {', '.join(knowledge_area['implementation_steps'])}
        Common Challenges: {', '.join(knowledge_area['common_challenges'])}
        
        Please provide a JSON response with the following structure:
        {{
            "current_state_assessment": "Assessment of current state in this area",
            "recommended_actions": ["Action 1", "Action 2", "Action 3"],
            "implementation_steps": ["Step 1", "Step 2", "Step 3"],
            "success_metrics": ["Metric 1", "Metric 2", "Metric 3"],
            "estimated_timeline": "Timeline estimate",
            "resource_requirements": ["Resource 1", "Resource 2"],
            "potential_challenges": ["Challenge 1", "Challenge 2"],
            "quick_wins": ["Quick win 1", "Quick win 2"]
        }}
        
        Ensure all recommendations are specific, actionable, and tailored to the organization's context.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data strategy expert. Provide specific, actionable recommendations in valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.3  # Lower temperature for more consistent JSON
            )
            
            # Parse JSON response
            content = response.choices[0].message.content
            # Clean up potential markdown formatting
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            return json.loads(content.strip())
            
        except Exception as e:
            print(f"Error generating area-specific recommendation: {e}")
            return None
    
    def generate_implementation_roadmap(self, 
                                      organizational_context: str,
                                      priority_recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate implementation roadmap"""

        recommendations_summary = "\n".join([
            f"- {rec.title} (Priority: {rec.priority if hasattr(rec, 'priority') else 'medium'})"
            for rec in priority_recommendations
        ])
        
        prompt = f"""
        Based on the organizational context and priority recommendations, create a three-phase implementation roadmap.
        
        ORGANIZATIONAL CONTEXT:
        {organizational_context}
        
        PRIORITY RECOMMENDATIONS:
        {recommendations_summary}
        
        Create a JSON response with three phases:
        {{
            "phases": [
                {{
                    "phase": "foundation",
                    "duration": "0-6 months",
                    "objectives": ["Objective 1", "Objective 2"],
                    "key_activities": ["Activity 1", "Activity 2"],
                    "deliverables": ["Deliverable 1", "Deliverable 2"],
                    "success_criteria": ["Criteria 1", "Criteria 2"],
                    "dependencies": ["Dependency 1"]
                }},
                {{
                    "phase": "core",
                    "duration": "6-18 months",
                    "objectives": ["Objective 1", "Objective 2"],
                    "key_activities": ["Activity 1", "Activity 2"],
                    "deliverables": ["Deliverable 1", "Deliverable 2"],
                    "success_criteria": ["Criteria 1", "Criteria 2"],
                    "dependencies": ["Dependency 1"]
                }},
                {{
                    "phase": "advanced",
                    "duration": "18+ months",
                    "objectives": ["Objective 1", "Objective 2"],
                    "key_activities": ["Activity 1", "Activity 2"],
                    "deliverables": ["Deliverable 1", "Deliverable 2"],
                    "success_criteria": ["Criteria 1", "Criteria 2"],
                    "dependencies": ["Dependency 1"]
                }}
            ]
        }}
        
        Ensure logical progression from foundation to advanced capabilities.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data strategy expert. Create a logical implementation roadmap in valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            result = json.loads(content.strip())
            return result.get("phases", [])
            
        except Exception as e:
            print(f"Error generating roadmap: {e}")
            return []

