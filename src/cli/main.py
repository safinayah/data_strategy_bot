"""
CLI Main Interface
Command-line interface for the Data Strategy Recommendation Bot
"""

import click
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.input_collector import InputCollector
from core.recommendation_engine import RecommendationEngine
from core.knowledge_base import KnowledgeBaseManager
from utils.report_generator import ReportGenerator

load_dotenv()

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    🎯 Data Strategy Recommendation Bot

    Generate data strategy recommendations based on DMBOK/CDMP framework
    """
    pass

@cli.command()
def setup():
    """Initialize the knowledge base and verify configuration"""
    console.print(Panel("🔧 Setting up Data Strategy Bot", style="blue"))

    # Check environment variables
    required_vars = ["OPENAI_API_KEY", "QDRANT_API_KEY", "QDRANT_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        console.print(f"❌ Missing environment variables: {', '.join(missing_vars)}", style="red")
        console.print("Please configure your .env file with the required API keys.")
        return

    console.print("✅ Environment variables configured")

    # Initialize knowledge base
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Initializing DMBOK knowledge base...", total=None)

        kb_manager = KnowledgeBaseManager()
        success = kb_manager.initialize_knowledge_base()

        if success:
            console.print("✅ Knowledge base initialized successfully")
        else:
            console.print("❌ Failed to initialize knowledge base", style="red")
            return

    console.print(Panel("🎉 Setup complete! You can now run 'data-strategy-bot recommend' to start.", style="green"))

@cli.command()
@click.option('--input-file', '-i', help='Load organizational input from JSON file')
@click.option('--output-file', '-o', help='Save recommendation to specific file')
@click.option('--format', '-f', type=click.Choice(['json', 'markdown', 'pdf']), default='markdown', help='Output format')
def recommend(input_file, output_file, format):
    """Generate data strategy recommendations"""
    console.print(Panel("🎯 Data Strategy Recommendation Generator", style="blue"))

    # Check if setup was completed
    if not os.getenv("OPENAI_API_KEY"):
        console.print("❌ Please run 'data-strategy-bot setup' first", style="red")
        return

    try:
        # Collect organizational input
        input_collector = InputCollector()

        if input_file and os.path.exists(input_file):
            console.print(f"📂 Loading input from {input_file}")
            org_input = input_collector.load_inputs(input_file)
        else:
            org_input = input_collector.collect_all_inputs()
            if not org_input:
                console.print("❌ Input collection cancelled", style="red")
                return

            # Save input for future use
            input_filename = input_collector.save_inputs(org_input)

        # Generate recommendations
        console.print("\n🤖 Generating recommendations...")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing organizational context and generating recommendations...", total=None)

            engine = RecommendationEngine()
            recommendation = engine.generate_comprehensive_recommendation(org_input)

        if not recommendation:
            console.print("❌ Failed to generate recommendations", style="red")
            return

        # Generate report
        console.print("📄 Generating report...")
        report_generator = ReportGenerator()

        if format == 'json':
            output_file = output_file or f"recommendation_{org_input.profile.company_name.lower().replace(' ', '_')}.json"
            engine.save_recommendation(recommendation, output_file)
        elif format == 'markdown':
            output_file = output_file or f"recommendation_{org_input.profile.company_name.lower().replace(' ', '_')}.md"
            report_generator.generate_markdown_report(recommendation, output_file)
        elif format == 'pdf':
            output_file = output_file or f"recommendation_{org_input.profile.company_name.lower().replace(' ', '_')}.pdf"
            md_file = output_file.replace('.pdf', '.md')
            report_generator.generate_markdown_report(recommendation, md_file)
            report_generator.convert_to_pdf(md_file, output_file)

        # Display summary
        display_recommendation_summary(recommendation)

        console.print(f"\n✅ Recommendation generated and saved to {output_file}", style="green")

    except Exception as e:
        console.print(f"❌ Error: {str(e)}", style="red")
        import traceback
        console.print(traceback.format_exc(), style="dim")

@cli.command()
def test():
    """Test the knowledge base and API connections"""
    console.print(Panel("🧪 Testing Data Strategy Bot", style="blue"))

    # Test environment variables
    console.print("🔍 Checking environment configuration...")
    required_vars = ["OPENAI_API_KEY", "QDRANT_API_KEY", "QDRANT_URL"]

    for var in required_vars:
        if os.getenv(var):
            console.print(f"  ✅ {var}: Configured")
        else:
            console.print(f"  ❌ {var}: Missing", style="red")

    # Test knowledge base
    console.print("\n🧠 Testing knowledge base...")
    try:
        kb_manager = KnowledgeBaseManager()
        kb_manager.test_knowledge_retrieval()
        console.print("✅ Knowledge base test completed")
    except Exception as e:
        console.print(f"❌ Knowledge base test failed: {e}", style="red")

    # Test OpenAI connection
    console.print("\n🤖 Testing OpenAI connection...")
    try:
        from utils.openai_client import OpenAIClient
        openai_client = OpenAIClient()

        # Simple test
        test_response = openai_client.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            max_tokens=10
        )

        if test_response.choices[0].message.content:
            console.print("✅ OpenAI connection successful")
        else:
            console.print("❌ OpenAI connection failed", style="red")

    except Exception as e:
        console.print(f"❌ OpenAI test failed: {e}", style="red")

    console.print("\n🎉 Testing complete!")

@cli.command()
@click.argument('input_file')
def analyze(input_file):
    """Analyze a saved organizational input file"""
    if not os.path.exists(input_file):
        console.print(f"❌ File not found: {input_file}", style="red")
        return

    try:
        input_collector = InputCollector()
        org_input = input_collector.load_inputs(input_file)

        console.print(Panel(f"📊 Analysis of {org_input.profile.company_name}", style="blue"))

        # Display analysis
        table = Table(title="Organizational Analysis")
        table.add_column("Aspect", style="cyan")
        table.add_column("Details", style="white")

        table.add_row("Company", f"{org_input.profile.company_name}")
        table.add_row("Industry", org_input.profile.industry.value)
        table.add_row("Size", org_input.profile.company_size.value)
        table.add_row("Business Model", org_input.profile.business_model.value)
        table.add_row("Data Maturity", org_input.data_landscape.data_governance_maturity.value)
        table.add_row("Tech Environment", org_input.technical_environment.technology_environment.value)

        console.print(table)

        # Priority areas
        priority_areas = org_input.get_priority_areas()
        console.print(f"\n🎯 Priority Areas: {', '.join(priority_areas)}")

        # Challenges summary
        challenges = []
        if org_input.challenges.data_quality_issues:
            challenges.append("Data Quality")
        if org_input.challenges.data_silos:
            challenges.append("Data Silos")
        if org_input.challenges.manual_processes:
            challenges.append("Manual Processes")
        if org_input.challenges.reporting_delays:
            challenges.append("Reporting Delays")
        if org_input.challenges.compliance_risks:
            challenges.append("Compliance Risks")

        console.print(f"⚠️ Key Challenges: {', '.join(challenges)}")

    except Exception as e:
        console.print(f"❌ Error analyzing file: {e}", style="red")

def display_recommendation_summary(recommendation):
    """Display a summary of the recommendation"""
    console.print(Panel(f"📋 Recommendation Summary for {recommendation.organization_name}", style="green"))

    # Priority recommendations
    priority_recs = recommendation.get_priority_recommendations()
    if priority_recs:
        table = Table(title="Priority Recommendations")
        table.add_column("Area", style="cyan")
        table.add_column("Priority", style="yellow")
        table.add_column("Timeline", style="white")

        for rec in priority_recs[:5]:  # Top 5
            table.add_row(rec.title, rec.priority.value, rec.estimated_timeline)

        console.print(table)

    # Quick wins
    if recommendation.quick_wins:
        console.print(f"\n🚀 Quick Wins:")
        for i, win in enumerate(recommendation.quick_wins[:3], 1):
            console.print(f"  {i}. {win}")

    # Implementation phases
    console.print(f"\n📅 Implementation Phases: {len(recommendation.implementation_roadmap)} phases planned")
    for phase in recommendation.implementation_roadmap:
        console.print(f"  • {phase.phase.value.title()} Phase ({phase.duration})")

if __name__ == "__main__":
    cli()

