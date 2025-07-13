import pandas as pd
import ollama
import yaml

class LLMRuleAgentOllama:
    def __init__(self, df: pd.DataFrame, model: str = "llama3.2"):
        self.df = df
        self.model = model

    def generate_rules(self, table_name="claims"):
        # Use few-shot format guidance in the prompt
        prompt = f"""You are a data quality analyst specialized in Property & Casualty (P&C) insurance. Your task is to generate semantic data quality validation rules in **pure YAML format** based on the sample table `{table_name}`. This dataset contains P&C insurance fields such as policyholder info, incident details, claim amounts, and regulatory indicators.

Output Requirements:
- Only output **valid YAML** using this structure:
rules:
  - column: age
    check: not_null
  - column: total_claim_amount
    check: positive_integer
  - column: incident_date
    check: "date_format: YYYY-MM-DD"

- Output **only YAML**. Do not include markdown (e.g., ```yaml), document separators (---), comments, or explanations.

- Do **not hallucinate** column names. Only generate rules for the columns provided in the sample table.

Allowed Check Types and Their Meaning:
- `not_null`: Value must not be null or empty (this is equivalent to `not_empty`). If a column has this check and contains a `null`, `NaN`, or blank string, it must be flagged in `issues.json`.
- `positive_integer`: Value must be an integer greater than 0. Any negative or non-integer value must be flagged.
- `length(n)`: Value must be exactly `n` characters long. Any other length should be flagged.
- `"date_format: YYYY-MM-DD"`: Value must match the exact `YYYY-MM-DD` pattern. Any other format, such as `MM/DD/YYYY` or `YYYY/MM/DD`, should be flagged.
- `not_empty`: Same as `not_null`. Value must not be blank, null, or missing.

Insurance-Relevant Field Expectations:
Apply the following rules when these columns appear:
- `age`, `months_as_customer`, `total_claim_amount`, `bodily_injuries`: → `positive_integer`
- `incident_date`, `policy_bind_date`, `auto_model_year`: → `"date_format: YYYY-MM-DD"`
- `insured_zip`: → `length(5)` or `length(6)` depending on observed data
- `fraud_reported`, `authorities_contacted`, `policy_number`, `customer_id`: → `not_null`

Reminder:
- The model must **flag all validation failures**. If a rule like `not_null` is defined and the column contains any nulls or empty values, each violating row must be captured in `issues.json`.
- Only generate YAML. No markdown, prose, or extra output.

Now, using the sample table provided below, return only the validation rules in YAML.


{self.df.head(3).to_markdown()}
"""

        # LLM call
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert in data quality and YAML formatting. Only respond with valid YAML."},
                {"role": "user", "content": prompt}
            ]
        )

        raw_yaml = response['message']['content']
        cleaned_yaml = self._clean_output(raw_yaml)
        wrapped_yaml = self._ensure_rules_wrapped(cleaned_yaml)

        return wrapped_yaml

    def _clean_output(self, raw: str) -> str:
        """Remove markdown, bullets, tags, and format-destroying characters. Fix indentation."""
        lines = raw.strip().splitlines()
        cleaned = []

        for line in lines:
            line = line.strip()

            # Skip markdown-like lines
            if line.startswith(("```", "---", "*", "+", "#", "`")):
                continue

            # Auto-quote multiple-colon values
            if "check:" in line and line.count(":") > 1:
                key, value = line.split(":", 1)
                value = value.strip().strip('"').strip("'")  # Remove any existing quotes
                line = f'{key.strip()}: "{value}"'

            # Fix indentation for list items and their keys
            if line.startswith("- "):
                cleaned.append("  " + line)
            elif line.startswith("check:") or line.startswith("column:"):
                cleaned.append("    " + line)
            elif line.startswith("rules:"):
                cleaned.append(line)
            else:
                cleaned.append(line)

        # Fix any double double-quotes in the whole output
        cleaned_yaml = "\n".join(cleaned)
        cleaned_yaml = cleaned_yaml.replace('""', '"')

        return cleaned_yaml

    from typing import Optional

    def _ensure_rules_wrapped(self, yaml_string: str) -> Optional[str]:
        """Ensure output is a dictionary with a 'rules' list and valid rule structure."""
        try:
            # Debug: print the YAML string before parsing
            print("DEBUG: YAML string to parse:\n", yaml_string)

            # Remove empty lines that may break YAML parsing
            yaml_string = "\n".join([line for line in yaml_string.splitlines() if line.strip()])

            parsed = yaml.safe_load(yaml_string)

            # If it's a list, wrap it
            if isinstance(parsed, list):
                parsed = {"rules": parsed}

            if not isinstance(parsed, dict) or "rules" not in parsed:
                raise ValueError("Missing 'rules' key in YAML")

            # Check each rule for required structure
            for rule in parsed["rules"]:
                if not isinstance(rule, dict) or "column" not in rule or "check" not in rule:
                    raise ValueError(f"Malformed rule: {rule}")

            # Return re-dumped valid YAML
            return yaml.dump(parsed, sort_keys=False)

        except Exception as e:
            print("YAML validation failed:", e)
            print("Tip: Check for missing column/check keys or formatting errors.")
            return None
