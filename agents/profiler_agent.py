import pandas as pd

class ProfilerAgent:
    def __init__(self, filepath: str):
        self.df = pd.read_csv(filepath, header=0)  # Explicitly set first row as header

    def get_dataframe(self):
        print("ProfilerAgent: Data loaded.")
        return self.df  # <-- Make sure to return the DataFrame
