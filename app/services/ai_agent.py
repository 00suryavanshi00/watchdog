import cohere

class AiAnalyzer:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = cohere.Client(api_key)

    # openai
    # def analyze_code(self, prompt: str) -> str:
    #     response = self.client.chat.completions.create(
    #         model=self.model_name,
    #         messages=[{"role": "user", "content": prompt}]
    #     )
    #     return response.choices[0].message.content

    # cohere
    def analyze_code(self, prompt: str) -> str:

        response = self.client.generate(
            model=self.model_name,  
            prompt=prompt,
            max_tokens=500 
        )
        return response.generations[0].text