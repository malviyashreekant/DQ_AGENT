# Data Quality Agent (DQ-Agent)

DQ-Agent is a Python automation tool for profiling datasets, generating data quality rules using Llama 3.2, validating data against rules, and summarizing issues with AI-driven recommendations.

## Features
- **Data Profiling:** Loads and profiles CSV datasets.
- **Rule Generation:** Uses Llama 3 to generate YAML-based data quality rules from the dataset.
- **Rule Validation:** Validates data using static or generated YAML rules.
- **AI Summarization:** Summarizes detected data quality issues and provides recommendations using Llama 3.

## Project Structure
```
dqga.py                  # Main script
agents/
  profiler_agent.py      # Data profiling logic
  llm_ruleagent.py       # LLM-based rule generation
  rule_agent.py          # Rule validation logic
  summarizeagent.py      # AI summarization logic
data/
  claims.csv             # Example dataset
rules/
  claims_rules.yaml              # Static hand-written rules
  generated_claims_rules.yaml    # LLM-generated rules
```

## Usage
1. **Prepare your dataset:** Place your CSV file in the `data/` directory (e.g., `claims.csv`).
2. **Run the main script:**
   ```powershell
   python dqga.py
   ```
3. **Workflow:**
   - Profiles the dataset.
   - Generates YAML rules using Llama 3.
   - Saves and reloads the rules.
   - Validates data using rules.
   - Summarizes issues and recommendations with Llama 3.

## Requirements
- Python 3.8+
- Required packages: `pandas`, `pyyaml`, and any dependencies for Llama 3 integration.

Install dependencies:
```powershell
pip install pandas pyyaml
```

## Customization
- **Rules:** Edit or add rules in `rules/claims_rules.yaml` or use generated rules in `rules/generated_claims_rules.yaml`.
- **Agents:** Extend or modify agents in the `agents/` directory for custom logic.

## License
MIT License
