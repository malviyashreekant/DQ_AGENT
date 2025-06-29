import ollama

class SummaryAgent:
    def __init__(self, model="llama3.2"):
        self.model = model

    def summarize_issues(self, issues: list):
        if not issues:
            return "No data quality issues were found."

        prompt = "Summarize and recommend improvements based on these data quality issues:\n"
        for i, issue in enumerate(issues):
            # Safely extract the first three elements
            idx = issue[0] if len(issue) > 0 else "N/A"
            col = issue[1] if len(issue) > 1 else "N/A"
            rule = issue[2] if len(issue) > 2 else "N/A"
            prompt += f"{i+1}. Row {idx}, Column '{col}': failed '{rule}' rule.\n"

        response = ollama.chat(
        model=self.model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a data quality analyst. Your job is to summarize validation errors. "
                    "Always assume that the rules are correct and the data is faulty. "
                    "For example, if a value fails a 'not_null' check, that means it **should not be null**, "
                    "but it currently is."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


        return response['message']['content']
