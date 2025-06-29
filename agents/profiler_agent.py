import pandas as pd

class ProfilerAgent:
    def __init__(self, filepath: str):
        self.df = pd.read_csv(filepath)

    def get_dataframe(self):
        print("ProfilerAgent: Data loaded.")
        return self.df
