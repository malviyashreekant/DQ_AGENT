import yaml
import pandas as pd
from datetime import datetime

class RuleAgent:
    def __init__(self, df: pd.DataFrame, rule_path: str):
        self.df = df
        with open(rule_path) as f:
            self.rules = yaml.safe_load(f)['rules']

    def validate(self):
        issues = []
        for rule in self.rules:
            col = rule['column']
            check = rule['check']

            if check == "not_null":
                invalid_rows = self.df[self.df[col].isnull()]
            elif check == "positive":
                invalid_rows = self.df[self.df[col] <= 0]
            elif check == "past_date":
                invalid_rows = self.df[pd.to_datetime(self.df[col]) > datetime.today()]
            else:
                continue

            for idx in invalid_rows.index:
                issues.append((idx, col, check))
        return issues
