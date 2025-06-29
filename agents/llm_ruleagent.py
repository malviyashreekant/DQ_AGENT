import pandas as pd
import ollama

class LLMRuleAgentOllama:
    def __init__(self, df: pd.DataFrame, model: str = "llama3.2"):
        self.df = df
        self.model = model

    def generate_rules(self, table_name="claims"):
        prompt = f"""You are a data quality analyst. Based on this table `{table_name}`, suggest useful data quality validation rules in YAML format. Here are the first few rows:\n\n{self.df.head(3).to_markdown()}"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert in data quality, insurance data validation, and YAML rule writing."},
                {"role": "user", "content": prompt}
            ]
        )

        return response['message']['content']
