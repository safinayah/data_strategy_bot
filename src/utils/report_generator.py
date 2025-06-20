"""
Report Generator
Generates formatted reports from recommendations
"""

import os
from typing import Dict, Any
from rich.console import Console
from rich.markdown import Markdown
from models.recommendations import DataStrategyRecommendation

class ReportGenerator:
    def __init__(self):
        self.console = Console()
    
    def generate_markdown_report(self, recommendation: DataStrategyRecommendation, filename: str):
        """Generate comprehensive markdown report"""
        
        report_content = self._build_markdown_content(recommendation)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 Markdown report generated: {filename}")
        return filename

    def _build_markdown_content(self, recommendation):
        """Build markdown content with proper validation"""

        # Get priority recommendations with validation
        priority_recs = recommendation.get_priority_recommendations()

        # Filter out any non-RecommendationArea objects
        valid_recs = []
        for rec in priority_recs:
            if hasattr(rec, 'title') and hasattr(rec, 'priority'):
                valid_recs.append(rec)
            else:
                print(f"Warning: Skipping invalid recommendation object: {type(rec)}")

        # Build content with valid recommendations only
        content = f"""# Data Strategy Recommendation Report

    ## Executive Summary
    {recommendation.executive_summary}

    ## Current State Overview
    {recommendation.current_state_overview}

    ## Priority Recommendations

    """

        for i, area_rec in enumerate(valid_recs, 1):
            content += f"""### {i}. {area_rec.title}

    **Priority:** {area_rec.priority.value if hasattr(area_rec.priority, 'value') else area_rec.priority}
    **Current State:** {area_rec.current_state_assessment}

    **Recommended Actions:**
    """
            for action in area_rec.recommended_actions:
                content += f"- {action}\n"

            content += f"""
    **Implementation Steps:**
    """
            for step in area_rec.implementation_steps:
                content += f"- {step}\n"

            content += f"""
    **Success Metrics:**
    """
            for metric in area_rec.success_metrics:
                content += f"- {metric}\n"

            content += f"""
    **Timeline:** {area_rec.estimated_timeline}
    **Resources Required:** {', '.join(area_rec.resource_requirements)}

    ---

    """

        return content

    def convert_to_pdf(self, markdown_file: str, pdf_file: str):
        """Convert markdown to PDF using system utility"""
        try:
            # Use the manus-md-to-pdf utility
            os.system(f"manus-md-to-pdf {markdown_file} {pdf_file}")
            print(f"📄 PDF report generated: {pdf_file}")
            return pdf_file
        except Exception as e:
            print(f"❌ Error converting to PDF: {e}")
            return None
    
    def display_report_preview(self, recommendation: DataStrategyRecommendation):
        """Display a preview of the report in the console"""
        content = self._build_markdown_content(recommendation)
        
        # Display first part of the report
        preview_content = content[:2000] + "..." if len(content) > 2000 else content
        
        markdown = Markdown(preview_content)
        self.console.print(markdown)

