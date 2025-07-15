import pandas as pd
import logging

class ProfilerAgent:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = None
        self.logger = logging.getLogger(__name__)
        self._load_data()

    def _load_data(self):
        """Load data with comprehensive error handling"""
        try:
            self.df = pd.read_csv(self.filepath, header=0)
            if self.df.empty:
                raise ValueError("CSV file is empty")
            self.logger.info(f"Successfully loaded {len(self.df)} rows from {self.filepath}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filepath}")
        except pd.errors.EmptyDataError:
            raise ValueError("CSV file is empty or corrupted")
        except pd.errors.ParserError as e:
            raise ValueError(f"CSV parsing error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error loading CSV: {str(e)}")

    def get_dataframe(self):
        """Get the loaded DataFrame"""
        if self.df is None:
            raise RuntimeError("Data not loaded. Check if file exists and is valid.")
        return self.df

    def get_profile(self):
        """Generate comprehensive data profile"""
        if self.df is None:
            raise RuntimeError("Data not loaded")
        
        profile = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'null_counts': self.df.isnull().sum().to_dict(),
            'null_percentages': (self.df.isnull().sum() / len(self.df) * 100).to_dict(),
            'unique_counts': self.df.nunique().to_dict(),
            'memory_usage': self.df.memory_usage(deep=True).to_dict()
        }
        
        # Add summary stats for numeric columns
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            profile['summary_stats'] = self.df[numeric_cols].describe().to_dict()
        
        return profile