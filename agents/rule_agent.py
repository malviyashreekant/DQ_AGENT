import yaml
import pandas as pd
from datetime import datetime

class RuleAgent:
    def __init__(self, df, rules):
        self.df = df
        self.rules = rules
        # Create a mapping from lowercase column names to actual column names
        self.col_map = {col.lower(): col for col in df.columns}

    def validate(self):
        issues = []
        for rule in self.rules:
            col = rule['column']
            check = rule['check']
            # Use the mapping to get the actual column name
            actual_col = self.col_map.get(col.lower())
            if not actual_col:
                issues.append(f"Column '{col}' not found in data.")
                continue

            if check == "not_null":
                invalid_rows = self.df[self.df[actual_col].isnull()]

            elif check == "positive":
                invalid_rows = self.df[self.df[actual_col] <= 0]

            elif check == "past_date":
                invalid_rows = self.df[pd.to_datetime(self.df[actual_col], errors='coerce') > datetime.today()]

            elif check.startswith("length("):
                expected_len = int(check.split("(")[1].strip(")"))
                invalid_rows = self.df[self.df[actual_col].astype(str).str.len() != expected_len]

            elif check.startswith("date_format"):
                fmt = check.split(":", 1)[1].strip().strip('"').strip()
                def is_valid_date(val):
                    try:
                        datetime.strptime(str(val), fmt)
                        return True
                    except Exception:
                        return False
                invalid_rows = self.df[~self.df[actual_col].apply(is_valid_date)]

            elif check == "positive_integer":
                invalid_rows = self.df[~self.df[actual_col].apply(lambda x: isinstance(x, int) and x > 0)]

            else:
                print(f"Unknown check type: {check}")
                continue

            for idx in invalid_rows.index:
                issues.append((idx, actual_col, check))

        return issues

