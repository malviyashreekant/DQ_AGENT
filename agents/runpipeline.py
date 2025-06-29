from dqcontroleragent import DQOrchestratorAgent

if __name__ == "__main__":
    filepath = "data/claims.csv" # Change this to your actual file
    orchestrator = DQOrchestratorAgent(filepath)
    result = orchestrator.run()
    print("\n Final Summary:\n", result)
