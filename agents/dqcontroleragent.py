from profiler_agent import ProfilerAgent
from llm_ruleagent import LLMRuleAgentOllama
from rule_agent import RuleAgent
from summarizeagent import SummaryAgent
from memory_man import DQMemory
from datetime import datetime
import os
import json
import yaml

class DQOrchestratorAgent:
    def __init__(self, filepath, model="llama3.2"):
        self.filepath = filepath
        self.model = model
        self.memory = DQMemory()

    def run(self):
        # Step 1: Load data
        profiler = ProfilerAgent(self.filepath)
        df = profiler.get_dataframe()

        # Step 2: Generate rules using LLM
        rulegen = LLMRuleAgentOllama(df, self.model)
        rules_yaml = rulegen.generate_rules()

        if rules_yaml is None:
            return "Pipeline stopped due to YAML error."

        self.memory.log({"stage": "rule_generation", "output": rules_yaml})

        # Step 3: Setup versioned output directory
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = os.path.join("dq_outputs", timestamp)
        os.makedirs(output_dir, exist_ok=True)

        rule_path = os.path.join(output_dir, "generated_rules.yaml")
        issues_path = os.path.join(output_dir, "issues.json")
        summary_path = os.path.join(output_dir, "summary.txt")

        # Save rules
        with open(rule_path, "w") as f:
            f.write(rules_yaml)

        # Step 4: Apply rules
        with open(rule_path, "r") as f:
            rules_yaml_loaded = yaml.safe_load(f)
        rules = rules_yaml_loaded["rules"]

        validator = RuleAgent(df, rules)
        issues = validator.validate()
        self.memory.log({"stage": "validation", "output": issues})

        # Step 5: Summarize
        summarizer = SummaryAgent(self.model)
        summary = summarizer.summarize_issues(issues)
        self.memory.log({"stage": "summary", "output": summary})

        # Save issues and summary
        with open(issues_path, "w") as f:
            json.dump(issues, f, indent=2)

        with open(summary_path, "w") as f:
            f.write(summary)

        return summary
