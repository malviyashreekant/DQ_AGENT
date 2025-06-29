# Data Quality Agent (DQ-Agent)

DQ-Agent is a Python automation tool for profiling datasets, generating data quality rules using Llama 3.2, validating data against rules, and summarizing issues with AI-driven recommendations.

## Features
- **Data Profiling:** Loads and profiles CSV datasets.
- **Rule Generation:** Uses Llama 3 to generate YAML-based data quality rules from the dataset.
- **Rule Validation:** Validates data using dynamically generated YAML rules.
- **AI Summarization:** Summarizes detected data quality issues and provides recommendations using Llama 3.

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
```

## Usage
1. **Prepare your dataset:** Place your CSV file in the `data/` directory (e.g., `claims.csv`).
2. **Run the pipeline:**
   ```powershell
   python agents/runpipeline.py
   ```
3. **Workflow:**
   - Profiles the dataset.
   - Generates YAML rules using Llama 3.
   - Saves and reloads the rules.
   - Validates data using generated rules.
   - Summarizes issues and recommendations with Llama 3.
   - Outputs results to a timestamped folder in `dq_outputs/`.

## Requirements
- Python 3.8+
- Required packages: `pandas`, `pyyaml`, and any dependencies for Llama 3 integration.

Install dependencies:
```powershell
pip install pandas pyyaml
```

## Customization
- **Agents:** Extend or modify agents in the `agents/` directory for custom logic.
- **Pipeline:** Adjust the pipeline logic in `agents/dqcontroleragent.py` or the entry script `agents/runpipeline.py`.

## License
