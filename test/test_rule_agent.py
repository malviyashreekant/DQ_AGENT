import unittest
import pandas as pd
import sys
import os

# Add the agents directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))

from rule_agent import RuleAgent

class TestRuleAgent(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.df = pd.DataFrame({
            'age': [25, 30, -5, 0, None, 'invalid'],
            'amount': [100.5, 200, -10, 0, None, 'text'],
            'date': ['2023-01-01', '2023-02-01', '2023-13-01', None, '', 'invalid'],
            'zip_code': ['12345', '67890', '123', '1234567', None, '']
        })
        
    def test_positive_integer_validation(self):
        """Test positive integer validation"""
        rules = [{'column': 'age', 'check': 'positive_integer'}]
        validator = RuleAgent(self.df, rules)
        issues = validator.validate()
        
        # Should find issues in rows 2, 3, 4, 5 (negative, zero, null, invalid)
        issue_rows = [issue[0] for issue in issues if isinstance(issue, tuple)]
        expected_issue_rows = [2, 3, 4, 5]
        
        self.assertEqual(set(issue_rows), set(expected_issue_rows))
    
    def test_not_null_validation(self):
        """Test not null validation"""
        rules = [{'column': 'age', 'check': 'not_null'}]
        validator = RuleAgent(self.df, rules)
        issues = validator.validate()
        
        # Should find issue in row 4 (None)
        issue_rows = [issue[0] for issue in issues if isinstance(issue, tuple)]
        self.assertIn(4, issue_rows)
    
    def test_length_validation(self):
        """Test length validation"""
        rules = [{'column': 'zip_code', 'check': 'length(5)'}]
        validator = RuleAgent(self.df, rules)
        issues = validator.validate()
        
        # Should find issues in rows 2, 3, 4, 5 (wrong length, null, empty)
        issue_rows = [issue[0] for issue in issues if isinstance(issue, tuple)]
        expected_issue_rows = [2, 3, 4, 5]
        
        self.assertEqual(set(issue_rows), set(expected_issue_rows))

if __name__ == '__main__':
    unittest.main()