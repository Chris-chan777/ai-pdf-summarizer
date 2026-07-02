class MockAIService:
    """Return deterministic study materials without calling an API."""

    def generate(self, prompt, selected_options):
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        return {
            "materials": [
                {
                    "type": option["value"],
                    "title": option["label"],
                    "content_markdown": (
                        f"这里是模拟生成的{option['label']}。"
                    ),
                }
                for option in selected_options
            ]
        }
