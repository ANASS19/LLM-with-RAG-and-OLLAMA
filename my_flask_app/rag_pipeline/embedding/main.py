from langchain_ollama import OllamaEmbeddings

class OllamaNomicEmbedder:
    def __init__(self):
        # If your version supports specifying deployment_id instead of model_name:
        self.model = OllamaEmbeddings(model="nomic-embed-text:latest")

    def get_model(self):
        return self.model

    @classmethod
    def factory(cls):
        instance = cls()
        return instance.get_model()
