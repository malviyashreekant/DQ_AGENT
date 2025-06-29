import ollama

class SummaryAgent:
    def __init__(self, model="llama3"):
        self.model = model

    def summarize_issues(self, issues: list):
        if not issues:
            return "No data quality issues were found."

        prompt = "Summarize and recommend improvements based on these data quality issues:\n"
        for i, (idx, col, rule) in enumerate(issues):
            prompt += f"{i+1}. Row {idx}, Column '{col}': failed '{rule}' rule.\n"

        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a data quality analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        return response['message']['content']
