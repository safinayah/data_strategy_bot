# Data Strategy Recommendation Bot - Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying and using the Data Strategy Recommendation Bot in your local environment.

## System Requirements

- **Python:** 3.11 or higher
- **Operating System:** Linux, macOS, or Windows
- **Memory:** Minimum 4GB RAM (8GB recommended)
- **Storage:** 2GB free space
- **Internet:** Required for API calls to OpenAI and Qdrant

## Prerequisites

### Required API Keys

1. **OpenAI API Key**
   - Sign up at https://platform.openai.com/
   - Create an API key with sufficient credits
   - Ensure access to GPT-4 model (recommended) or GPT-3.5-turbo

2. **Qdrant Vector Database**
   - Option 1: Qdrant Cloud (https://cloud.qdrant.io/)
   - Option 2: Self-hosted Qdrant instance
   - Note the API key and URL endpoint

## Installation Methods

### Method 1: Automated Installation (Recommended)

1. **Download and extract the project:**
```bash
# Extract the data_strategy_bot folder to your desired location
cd data_strategy_bot
```

2. **Run the installation script:**
```bash
./install.sh
```

3. **Configure environment variables:**
```bash
# Edit the .env file with your API keys
nano .env
```

Add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_URL=your_qdrant_url_here
```

### Method 2: Manual Installation

1. **Install Python dependencies:**
```bash
pip3 install -r requirements.txt
```

2. **Install the package:**
```bash
pip3 install -e .
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Initial Setup

### 1. Initialize Knowledge Base

```bash
data-strategy-bot setup
```

This command will:
- Verify your API keys
- Create the Qdrant collection
- Load DMBOK knowledge into the vector database
- Confirm system readiness

### 2. Test the System

```bash
data-strategy-bot test
```

This will verify:
- Environment configuration
- API connectivity
- Knowledge base functionality

## Usage

### Basic Usage

Generate recommendations with interactive questionnaire:
```bash
data-strategy-bot recommend
```

### Advanced Usage

```bash
# Generate PDF report
data-strategy-bot recommend --format pdf

# Use saved organizational input
data-strategy-bot recommend --input-file company_profile.json

# Specify output file
data-strategy-bot recommend --output-file my_strategy_report.md
```

### Analyze Existing Data

```bash
# Analyze a saved organizational profile
data-strategy-bot analyze company_profile.json
```

## Project Structure

```
data_strategy_bot/
├── src/
│   ├── cli/                    # Command-line interface
│   │   ├── main.py            # Main CLI commands
│   │   └── questionnaire.py   # Interactive components
│   ├── core/                   # Core business logic
│   │   ├── input_collector.py # Input collection system
│   │   ├── knowledge_base.py  # Knowledge base manager
│   │   └── recommendation_engine.py # AI recommendation engine
│   ├── models/                 # Data models
│   │   ├── organization.py    # Organizational data structures
│   │   └── recommendations.py # Recommendation data structures
│   ├── utils/                  # Utility modules
│   │   ├── openai_client.py   # OpenAI API client
│   │   ├── qdrant_client.py   # Qdrant vector database client
│   │   └── report_generator.py # Report generation
│   └── data/                   # Knowledge base and templates
│       └── dmbok_knowledge/    # DMBOK framework content
├── tests/                      # Test suite
├── requirements.txt            # Python dependencies
├── setup.py                   # Package configuration
├── .env.example               # Environment template
├── README.md                  # Project overview
├── USAGE.md                   # Usage examples
└── install.sh                 # Installation script
```

## Configuration Options

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_key_here
QDRANT_API_KEY=your_key_here
QDRANT_URL=your_url_here

# Optional
LOG_LEVEL=INFO              # Logging level
MAX_TOKENS=4000            # OpenAI max tokens
TEMPERATURE=0.7            # OpenAI temperature
```

### Customization

The system is designed to be configurable:

1. **DMBOK Knowledge:** Modify `src/data/dmbok_knowledge/knowledge_base.py`
2. **Prompts:** Customize prompts in `src/utils/openai_client.py`
3. **Report Templates:** Modify `src/utils/report_generator.py`
4. **Input Models:** Extend `src/models/organization.py`

## Troubleshooting

### Common Issues

1. **"Module not found" errors:**
```bash
# Reinstall the package
pip3 install -e .
```

2. **API key errors:**
```bash
# Verify .env file configuration
cat .env
# Ensure no extra spaces or quotes around keys
```

3. **Qdrant connection issues:**
```bash
# Test Qdrant connectivity
data-strategy-bot test
```

4. **Permission errors on install.sh:**
```bash
chmod +x install.sh
```

### Performance Optimization

1. **For large organizations:** Increase MAX_TOKENS in .env
2. **For faster responses:** Use GPT-3.5-turbo instead of GPT-4
3. **For cost optimization:** Reduce TEMPERATURE for more deterministic outputs

### Logging and Debugging

Enable detailed logging:
```bash
export LOG_LEVEL=DEBUG
data-strategy-bot recommend
```

## Security Considerations

1. **API Keys:** Never commit .env file to version control
2. **Data Privacy:** Organizational data is processed by OpenAI
3. **Local Storage:** Input files are saved locally in JSON format
4. **Network:** Ensure secure connections to API endpoints

## Backup and Recovery

### Backup Important Data

```bash
# Backup organizational inputs
cp *.json backup/

# Backup generated reports
cp *.md *.pdf reports/
```

### Recovery

If the knowledge base needs to be rebuilt:
```bash
data-strategy-bot setup
```

## Support and Maintenance

### Regular Maintenance

1. **Update dependencies:**
```bash
pip3 install -r requirements.txt --upgrade
```

2. **Refresh knowledge base:**
```bash
data-strategy-bot setup
```

3. **Test system health:**
```bash
data-strategy-bot test
```

### Getting Help

1. **Command help:**
```bash
data-strategy-bot --help
data-strategy-bot recommend --help
```

2. **System diagnostics:**
```bash
data-strategy-bot test
```

3. **Check logs:** Review console output for error messages

## Production Deployment Considerations

For production or team deployment:

1. **Shared Qdrant Instance:** Use a dedicated Qdrant cluster
2. **API Rate Limits:** Monitor OpenAI usage and implement rate limiting
3. **Data Governance:** Establish policies for organizational data handling
4. **Access Control:** Implement user authentication if needed
5. **Monitoring:** Set up logging and monitoring for system health

## License and Compliance

This system is designed for educational and professional development purposes. When using in production:

1. Review OpenAI's usage policies
2. Ensure compliance with data privacy regulations
3. Consider data residency requirements
4. Implement appropriate security measures

---

**Note:** This system generates AI-powered recommendations based on the DMBOK framework. While comprehensive, recommendations should be reviewed by qualified data management professionals before implementation.

