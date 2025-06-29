import pandas as pd
import ollama
import yaml

class LLMRuleAgentOllama:
    def __init__(self, df: pd.DataFrame, model: str = "llama3.2"):
        self.df = df
        self.model = model

    def generate_rules(self, table_name="claims"):
        # Use few-shot format guidance in the prompt
        prompt = f"""You are a data quality analyst. Your task is to generate data quality validation rules in **pure YAML format** based on the sample table `{table_name}`.

Only output valid YAML with this exact structure:

rules:
  - column: age
    check: not_null
  - column: name
    check: length(5)
  - column: join_date
    check: "date_format: YYYY-MM-DD"

Allowed check types:
- not_null
- not_empty
- length(n)
- positive_integer
- "date_format: YYYY-MM-DD"

 DO NOT include:
- Markdown formatting (like ```yaml or *)
- YAML document separators (---)
- Explanations, comments, or aliases (! or &)
- Column inference — always include a column name

Only return clean YAML — no prose or markdown.

Here are the first few rows of the table:

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
