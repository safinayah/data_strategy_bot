"""
Input Collector
Interactive system for collecting organizational information
"""

import json
import os
from typing import Dict, Any, List
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from models.organization import (
    OrganizationalInput, OrganizationalProfile, CurrentDataLandscape,
    BusinessObjectives, TechnicalEnvironment, DataChallenges,
    IndustryType, CompanySize, BusinessModel, DataMaturityLevel, TechnologyEnvironment
)

class InputCollector:
    def __init__(self):
        self.console = Console()
        
    def display_welcome(self):
        """Display welcome message"""
        welcome_text = """
        🎯 Data Strategy Recommendation Bot
        
        This tool will collect information about your organization and generate
        data strategy recommendations based on the DMBOK/CDMP framework.
        
        The questionnaire covers:
        • Organizational Profile
        • Current Data Landscape  
        • Business Objectives
        • Technical Environment
        • Current Challenges
        """
        
        self.console.print(Panel(welcome_text, title="Welcome", border_style="blue"))
        
    def collect_organizational_profile(self) -> OrganizationalProfile:
        """Collect basic organizational information"""
        self.console.print("\n[bold blue]📋 Organizational Profile[/bold blue]")
        
        company_name = Prompt.ask("Company name")
        
        # Industry selection
        self.console.print("\nSelect your industry:")
        industries = list(IndustryType)
        for i, industry in enumerate(industries, 1):
            self.console.print(f"  {i}. {industry.value.replace('_', ' ').title()}")
        
        industry_choice = int(Prompt.ask("Industry", choices=[str(i) for i in range(1, len(industries) + 1)]))
        industry = industries[industry_choice - 1]
        
        # Company size
        self.console.print("\nSelect company size:")
        sizes = list(CompanySize)
        for i, size in enumerate(sizes, 1):
            description = {
                "startup": "< 50 employees",
                "small": "50-250 employees", 
                "medium": "250-1000 employees",
                "large": "1000-5000 employees",
                "enterprise": "> 5000 employees"
            }
            self.console.print(f"  {i}. {size.value.title()} ({description[size.value]})")
        
        size_choice = int(Prompt.ask("Company size", choices=[str(i) for i in range(1, len(sizes) + 1)]))
        company_size = sizes[size_choice - 1]
        
        # Business model
        self.console.print("\nSelect primary business model:")
        models = list(BusinessModel)
        for i, model in enumerate(models, 1):
            self.console.print(f"  {i}. {model.value.upper()}")
        
        model_choice = int(Prompt.ask("Business model", choices=[str(i) for i in range(1, len(models) + 1)]))
        business_model = models[model_choice - 1]
        
        # Geographic presence
        geographic_presence = []
        self.console.print("\nGeographic presence (enter countries/regions, press Enter when done):")
        while True:
            region = Prompt.ask("Region (or press Enter to finish)", default="")
            if not region:
                break
            geographic_presence.append(region)
        
        # Revenue range
        revenue_range = Prompt.ask("Annual revenue range (optional)", default="")
        
        # Regulatory requirements
        regulatory_requirements = []
        self.console.print("\nRegulatory requirements (GDPR, HIPAA, SOX, etc. - press Enter when done):")
        while True:
            regulation = Prompt.ask("Regulation (or press Enter to finish)", default="")
            if not regulation:
                break
            regulatory_requirements.append(regulation)
        
        return OrganizationalProfile(
            company_name=company_name,
            industry=industry,
            company_size=company_size,
            business_model=business_model,
            geographic_presence=geographic_presence,
            annual_revenue_range=revenue_range if revenue_range else None,
            regulatory_requirements=regulatory_requirements
        )
    
    def collect_data_landscape(self) -> CurrentDataLandscape:
        """Collect current data landscape information"""
        self.console.print("\n[bold blue]💾 Current Data Landscape[/bold blue]")
        
        # Data sources
        data_sources = []
        self.console.print("\nPrimary data sources (CRM, ERP, databases, etc. - press Enter when done):")
        while True:
            source = Prompt.ask("Data source (or press Enter to finish)", default="")
            if not source:
                break
            data_sources.append(source)
        
        # Data volume
        data_volume = Prompt.ask("Estimated total data volume", default="Unknown")
        
        # Data types
        data_types = []
        self.console.print("\nTypes of data (customer, financial, operational, etc. - press Enter when done):")
        while True:
            data_type = Prompt.ask("Data type (or press Enter to finish)", default="")
            if not data_type:
                break
            data_types.append(data_type)
        
        # Current tools
        current_tools = []
        self.console.print("\nCurrent data management tools (press Enter when done):")
        while True:
            tool = Prompt.ask("Tool (or press Enter to finish)", default="")
            if not tool:
                break
            current_tools.append(tool)
        
        # Governance maturity
        self.console.print("\nData governance maturity level:")
        maturity_levels = list(DataMaturityLevel)
        for i, level in enumerate(maturity_levels, 1):
            descriptions = {
                "initial": "Ad-hoc, reactive approach",
                "managed": "Some processes defined",
                "defined": "Standardized processes",
                "quantitatively_managed": "Measured and controlled",
                "optimizing": "Continuous improvement"
            }
            self.console.print(f"  {i}. {level.value.title()} - {descriptions[level.value]}")
        
        maturity_choice = int(Prompt.ask("Maturity level", choices=[str(i) for i in range(1, len(maturity_levels) + 1)]))
        governance_maturity = maturity_levels[maturity_choice - 1]
        
        # Quality issues
        quality_issues = []
        self.console.print("\nKnown data quality issues (press Enter when done):")
        while True:
            issue = Prompt.ask("Quality issue (or press Enter to finish)", default="")
            if not issue:
                break
            quality_issues.append(issue)
        
        # Compliance challenges
        compliance_challenges = []
        self.console.print("\nCurrent compliance challenges (press Enter when done):")
        while True:
            challenge = Prompt.ask("Compliance challenge (or press Enter to finish)", default="")
            if not challenge:
                break
            compliance_challenges.append(challenge)
        
        return CurrentDataLandscape(
            primary_data_sources=data_sources,
            data_volume_estimate=data_volume,
            data_types=data_types,
            current_data_tools=current_tools,
            data_governance_maturity=governance_maturity,
            data_quality_issues=quality_issues,
            compliance_challenges=compliance_challenges
        )
    
    def collect_business_objectives(self) -> BusinessObjectives:
        """Collect business objectives"""
        self.console.print("\n[bold blue]🎯 Business Objectives[/bold blue]")
        
        # Strategic goals
        strategic_goals = []
        self.console.print("\nTop 3-5 strategic business goals:")
        for i in range(5):
            goal = Prompt.ask(f"Strategic goal {i+1} (or press Enter to finish)", default="")
            if not goal:
                break
            strategic_goals.append(goal)
        
        # KPIs
        kpis = []
        self.console.print("\nKey performance indicators (press Enter when done):")
        while True:
            kpi = Prompt.ask("KPI (or press Enter to finish)", default="")
            if not kpi:
                break
            kpis.append(kpi)
        
        # Digital transformation initiatives
        digital_initiatives = []
        self.console.print("\nCurrent or planned digital transformation initiatives (press Enter when done):")
        while True:
            initiative = Prompt.ask("Initiative (or press Enter to finish)", default="")
            if not initiative:
                break
            digital_initiatives.append(initiative)
        
        # Data-driven decisions
        data_decisions = []
        self.console.print("\nAreas where better data could improve decisions (press Enter when done):")
        while True:
            area = Prompt.ask("Decision area (or press Enter to finish)", default="")
            if not area:
                break
            data_decisions.append(area)
        
        # Competitive advantages
        competitive_advantages = []
        self.console.print("\nDesired competitive advantages from data (press Enter when done):")
        while True:
            advantage = Prompt.ask("Competitive advantage (or press Enter to finish)", default="")
            if not advantage:
                break
            competitive_advantages.append(advantage)
        
        # Budget
        budget = Prompt.ask("Budget range for data initiatives (optional)", default="")
        
        return BusinessObjectives(
            strategic_goals=strategic_goals,
            key_performance_indicators=kpis,
            digital_transformation_initiatives=digital_initiatives,
            data_driven_decisions=data_decisions,
            competitive_advantages=competitive_advantages,
            budget_constraints=budget if budget else None
        )
    
    def collect_technical_environment(self) -> TechnicalEnvironment:
        """Collect technical environment information"""
        self.console.print("\n[bold blue]⚙️ Technical Environment[/bold blue]")
        
        # Technology environment
        self.console.print("\nPrimary technology environment:")
        tech_envs = list(TechnologyEnvironment)
        for i, env in enumerate(tech_envs, 1):
            self.console.print(f"  {i}. {env.value.replace('_', ' ').title()}")
        
        env_choice = int(Prompt.ask("Technology environment", choices=[str(i) for i in range(1, len(tech_envs) + 1)]))
        tech_environment = tech_envs[env_choice - 1]
        
        # Cloud providers
        cloud_providers = []
        if tech_environment in [TechnologyEnvironment.CLOUD, TechnologyEnvironment.HYBRID, TechnologyEnvironment.MULTI_CLOUD]:
            self.console.print("\nCloud providers in use (press Enter when done):")
            while True:
                provider = Prompt.ask("Cloud provider (or press Enter to finish)", default="")
                if not provider:
                    break
                cloud_providers.append(provider)
        
        # Database technologies
        databases = []
        self.console.print("\nDatabase technologies in use (press Enter when done):")
        while True:
            db = Prompt.ask("Database technology (or press Enter to finish)", default="")
            if not db:
                break
            databases.append(db)
        
        # Integration requirements
        integrations = []
        self.console.print("\nKey integration requirements (press Enter when done):")
        while True:
            integration = Prompt.ask("Integration requirement (or press Enter to finish)", default="")
            if not integration:
                break
            integrations.append(integration)
        
        # Security requirements
        security_reqs = []
        self.console.print("\nSecurity and compliance requirements (press Enter when done):")
        while True:
            security = Prompt.ask("Security requirement (or press Enter to finish)", default="")
            if not security:
                break
            security_reqs.append(security)
        
        # Scalability needs
        scalability = Prompt.ask("Expected growth and scalability needs")
        
        # Team size
        team_size_str = Prompt.ask("Size of technical team (optional)", default="")
        team_size = int(team_size_str) if team_size_str.isdigit() else None
        
        return TechnicalEnvironment(
            technology_environment=tech_environment,
            cloud_providers=cloud_providers,
            database_technologies=databases,
            integration_requirements=integrations,
            security_requirements=security_reqs,
            scalability_needs=scalability,
            technical_team_size=team_size
        )
    
    def collect_challenges(self) -> DataChallenges:
        """Collect current challenges"""
        self.console.print("\n[bold blue]⚠️ Current Data Challenges[/bold blue]")
        
        challenges = {
            "data_silos": "Data silos exist across departments",
            "data_quality_issues": "Significant data quality problems", 
            "manual_processes": "Heavy reliance on manual data processes",
            "reporting_delays": "Delays in reporting and analytics",
            "compliance_risks": "Compliance and regulatory risks",
            "scalability_issues": "Current systems don't scale",
            "skill_gaps": "Lack of data management skills",
            "budget_limitations": "Limited budget for data initiatives"
        }
        
        challenge_responses = {}
        for key, description in challenges.items():
            challenge_responses[key] = Confirm.ask(f"Do you have: {description}")
        
        return DataChallenges(**challenge_responses)
    
    def collect_all_inputs(self) -> OrganizationalInput:
        """Collect all organizational inputs"""
        self.display_welcome()
        
        if not Confirm.ask("\nReady to start the questionnaire?"):
            self.console.print("Questionnaire cancelled.")
            return None
        
        # Collect all sections
        profile = self.collect_organizational_profile()
        data_landscape = self.collect_data_landscape()
        business_objectives = self.collect_business_objectives()
        technical_environment = self.collect_technical_environment()
        challenges = self.collect_challenges()
        
        # Additional context
        self.console.print("\n[bold blue]📝 Additional Context[/bold blue]")
        additional_context = Prompt.ask("Any additional context or specific requirements (optional)", default="")
        
        # Create complete input
        org_input = OrganizationalInput(
            profile=profile,
            data_landscape=data_landscape,
            business_objectives=business_objectives,
            technical_environment=technical_environment,
            challenges=challenges,
            additional_context=additional_context if additional_context else None
        )
        
        # Display summary
        self.display_input_summary(org_input)
        
        return org_input
    
    def display_input_summary(self, org_input: OrganizationalInput):
        """Display summary of collected inputs"""
        self.console.print("\n[bold green]📊 Input Summary[/bold green]")
        
        table = Table(title="Organizational Information Summary")
        table.add_column("Category", style="cyan")
        table.add_column("Details", style="white")
        
        table.add_row("Company", f"{org_input.profile.company_name} ({org_input.profile.industry.value})")
        table.add_row("Size", f"{org_input.profile.company_size.value} - {org_input.profile.business_model.value}")
        table.add_row("Data Volume", org_input.data_landscape.data_volume_estimate)
        table.add_row("Governance Maturity", org_input.data_landscape.data_governance_maturity.value)
        table.add_row("Tech Environment", org_input.technical_environment.technology_environment.value)
        table.add_row("Priority Areas", ", ".join(org_input.get_priority_areas()))
        
        self.console.print(table)
    
    def save_inputs(self, org_input: OrganizationalInput, filename: str = None):
        """Save inputs to JSON file"""
        if not filename:
            filename = f"org_input_{org_input.profile.company_name.lower().replace(' ', '_')}.json"
        
        with open(filename, 'w') as f:
            json.dump(org_input.dict(), f, indent=2)
        
        self.console.print(f"\n✅ Inputs saved to {filename}")
        return filename
    
    def load_inputs(self, filename: str) -> OrganizationalInput:
        """Load inputs from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        return OrganizationalInput(**data)

