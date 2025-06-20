<<<<<<< HEAD
# data_strategy_bot
=======
# Data Strategy Recommendation Bot

A CLI-based bot that receives organizational inputs and generates data strategy recommendations based on DMBOK/CDMP framework using OpenAI and Qdrant vector database.

## Features

- Interactive CLI questionnaire for organizational data collection
- DMBOK/CDMP framework-based recommendations
- Vector database for efficient knowledge retrieval
- OpenAI-powered intelligent analysis
- Structured data strategy reports

## Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure your API keys:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` with your actual API keys:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `QDRANT_URL`: Your Qdrant instance URL

## Usage

Run the CLI application:
```bash
python -m src.cli.main
```

Follow the interactive prompts to provide organizational information and receive data strategy recommendations.

## Project Structure

```
data_strategy_bot/
├── src/
│   ├── cli/           # Command-line interface
│   ├── core/          # Core business logic
│   ├── models/        # Data models
│   ├── utils/         # Utility functions
│   └── data/          # Knowledge base and templates
├── tests/             # Test files
├── requirements.txt   # Python dependencies
└── setup.py          # Package setup
```

## DMBOK Knowledge Areas Covered

1. Data Governance
2. Data Architecture
3. Data Modeling and Design
4. Data Storage and Operations
5. Data Security
6. Data Integration and Interoperability
7. Document and Content Management
8. Data Warehousing and Business Intelligence
9. Metadata Management
10. Data Quality Management

## License

This project is for educational and professional development purposes.

>>>>>>> 7f2fcd9 (Initial commit)
