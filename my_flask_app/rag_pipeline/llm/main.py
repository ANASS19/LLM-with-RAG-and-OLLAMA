# my_flask_app/model.py
from langchain_ollama import OllamaLLM

class modelcreation:
    def __init__(self):
        self.model = OllamaLLM(
            model="llama3.2:latest",
            verbose=True,
            streaming=False,
            endpoint="http://localhost:11434/api/generate",
        )

    def get_model(self):
        return self.model
