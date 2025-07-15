import yaml
import os
from typing import Dict, Any, Optional

class DQConfig:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            self._create_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {str(e)}")

    def _create_default_config(self):
        """Create default configuration file"""
        default_config = {
            'models': {
                'default': 'llama3.2',
                'fallback': 'llama3.1'
            },
            'rule_templates': {
                'insurance_fields': {
                    'age': 'positive_integer',
                    'months_as_customer': 'positive_integer',
                    'total_claim_amount': 'positive_integer',
                    'bodily_injuries': 'positive_integer',
                    'incident_date': 'date_format: %Y-%m-%d',
                    'policy_bind_date': 'date_format: %Y-%m-%d',
                    'insured_zip': 'length(5)',
                    'fraud_reported': 'not_null',
                    'authorities_contacted': 'not_null',
                    'policy_number': 'not_null',
                    'customer_id': 'not_null'
                }
            },
            'output': {
                'base_dir': 'dq_outputs',
                'keep_history': 30  # days
            },
            'memory': {
                'max_entries': 1000,
                'cleanup_interval': 100
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value

    def get_rule_templates(self) -> Dict[str, str]:
        """Get rule templates for common fields"""
        return self.get('rule_templates.insurance_fields', {})