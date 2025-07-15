import unittest
import tempfile
import os
import pandas as pd
import sys

# Add the agents directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))

from dqcontroleragent import DQOrchestratorAgent

class TestIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        # Create temporary CSV file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        test_data = pd.DataFrame({
            'age': [25, 30, -5],
            'total_claim_amount': [1000, 2000, -500],
            'incident_date': ['2023-01-01', '2023-02-01', 'invalid'],
            'policy_number': ['P001', 'P002', None]
        })
        test_data.to_csv(self.temp_file.name, index=False)
        self.temp_file.close()
        
    def tearDown(self):
        """Clean up temporary file"""
        os.unlink(self.temp_file.name)
        
    def test_full_pipeline(self):
        """Test the complete pipeline"""
        try:
            orchestrator = DQOrchestratorAgent(self.temp_file.name)
            result = orchestrator.run()
            
            # Should complete without throwing exception
            self.assertIsInstance(result, str)
            self.assertNotIn("Pipeline failed", result)
            
        except Exception as e:
            self.fail(f"Pipeline failed with exception: {str(e)}")

if __name__ == '__main__':
    unittest.main()