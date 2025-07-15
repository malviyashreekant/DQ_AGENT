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

            try:
                if check in ("not_null", "not_empty"):
                    invalid_rows = self.df[self.df[actual_col].isnull() | (self.df[actual_col] == "")]

                elif check == "positive":
                    # Fixed: Handle non-numeric values properly
                    invalid_rows = self.df[~self.df[actual_col].apply(self._is_positive_number)]

                elif check == "positive_integer":
                    # Fixed: Complete rewrite of positive_integer check
                    invalid_rows = self.df[~self.df[actual_col].apply(self._is_positive_integer)]

                elif check == "past_date":
                    # Fixed: Better date handling
                    invalid_rows = self.df[~self.df[actual_col].apply(self._is_past_date)]

                elif check.startswith("length("):
                    expected_len = int(check.split("(")[1].strip(")"))
                    invalid_rows = self.df[~self.df[actual_col].apply(
                        lambda x: self._check_length(x, expected_len))]

                elif check.startswith("date_format"):
                    fmt = check.split(":", 1)[1].strip().strip('"').strip()
                    invalid_rows = self.df[~self.df[actual_col].apply(
                        lambda x: self._is_valid_date_format(x, fmt))]

                else:
                    print(f"Unknown check type: {check}")
                    continue

                for idx in invalid_rows.index:
                    issues.append((idx, actual_col, check))

            except Exception as e:
                issues.append(f"Error validating column '{actual_col}' with check '{check}': {str(e)}")

        return issues

    def _is_positive_number(self, val):
    #Check if value is a positive number
        try:
            if pd.isnull(val) or val == "":
                return False
            num_val = float(val)
            return num_val > 0
        except (ValueError, TypeError):
            return False

    def _is_positive_integer(self, val):
        """Check if value is a positive integer"""
        try:
            if pd.isnull(val) or val == "":
                return False
            num_val = float(val)
            return num_val > 0 and num_val == int(num_val)
        except (ValueError, TypeError):
            return False

    def _is_past_date(self, val):
        """Check if date is in the past"""
        try:
            if pd.isnull(val) or val == "":
                return False
            date_val = pd.to_datetime(val, errors='coerce')
            return pd.notnull(date_val) and date_val < pd.Timestamp.now()
        except:
            return False

    def _check_length(self, val, expected_len):
        """Check if value has expected length"""
        try:
            if pd.isnull(val):
                return False
            return len(str(val)) == expected_len
        except:
            return False

    def _is_valid_date_format(self, val, fmt):
        """Check if value matches expected date format"""
        try:
            if pd.isnull(val) or val == "":
                return False
            datetime.strptime(str(val), fmt)
            return True
        except:
            return False



