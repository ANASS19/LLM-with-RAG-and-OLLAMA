# my_flask_app/rag_pipeline/vectorestore/vectorestore.py
import os
import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings

class CSVChromaVectorStore:
    """
    Loads a CSV from the specified path, reads the 'text' column,
    and creates a Chroma-based vector store using the provided embedder.
    """
    def __init__(self, csv_path: str, embedding: Embeddings, collection_name: str = "csv_collection"):
        self.csv_path = csv_path
        self.embedding = embedding
        self.collection_name = collection_name
        self.vectorstore = None

    def create_collection(self):
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found at {self.csv_path}")
        df = pd.read_csv(self.csv_path)
        if 'text' not in df.columns:
            raise ValueError("CSV must contain a 'text' column")
        documents = df['text'].tolist()
        metadatas = df.to_dict(orient='records')
        self.vectorstore = Chroma.from_texts(
            documents,
            self.embedding,
            collection_name=self.collection_name,
            metadatas=metadatas
        )
        return self.vectorstore

    def get_vectorstore(self):
        if self.vectorstore is None:
            self.create_collection()
        return self.vectorstore
