# Data Quality Agent (DQ-Agent)

DQ-Agent is a Python automation tool for profiling datasets, generating data quality rules using Llama 3.2, validating data against rules, and summarizing issues with AI-driven recommendations.

# Dataset Information
Sample of 20 records used from Kaggle Dataset ( https://www.kaggle.com/datasets/buntyshah/auto-insurance-claims-data ) that contains real-world auto insurance claim records intended for analysis or fraud detection

## Features

- **Automated Rule Generation:** Uses LLM (Llama 3) to generate semantic data quality rules from your dataset.
- **Comprehensive Data Validation:** Validates your data against dynamically generated YAML rules.
- **Detailed Reporting and Summaries:** Produces detailed reports and AI-generated summaries of data quality issues.
- **Memory Management:** Maintains pipeline history for traceability and auditing.
- **Configurable Validation Rules:** Easily customize rule templates and validation logic via configuration.

## Quick Start

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
2. **Prepare your data:**
   - Place your CSV file in the `data/` directory.

3. **Configure the pipeline:**
   - Update the `filepath` variable in [`agents/runpipeline.py`](agents/runpipeline.py) to point to your CSV file.

4. **Run the pipeline:**
   ```
   python agents/runpipeline.py
   ```

## Testing

- **Unit tests:**
  ```
  python -m unittest test_rule_agent -v
  ```
- **Integration tests:**
  ```
  python -m unittest test_integration -v
  ```

## Configuration

Edit [`config.yaml`](config.yaml) to customize:
- Model selection (e.g., Llama 3 version)
- Rule templates for common fields
- Output directories and retention
- Memory and logging settings

## Project Structure

```
agents/
  profiler_agent.py        # Data profiling logic
  llm_ruleagent.py         # LLM-based rule generation
  rule_agent.py            # Rule validation logic
  summarizeagent.py        # AI summarization logic
  dqcontroleragent.py      # Orchestrates the pipeline
  runpipeline.py           # Main entry point to run the pipeline
  memory_man.py            # In-memory logging for pipeline stages
data/
  claims.csv               # Example dataset
dq_outputs/                # Output folders with results
test/
  test_rule_agent.py       # Unit tests for rule validation
  test_integration.py      # Integration tests for the pipeline
requirements.txt           # Python dependencies
README.md                  # Project documentation
```




