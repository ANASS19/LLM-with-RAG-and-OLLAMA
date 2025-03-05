# my_flask_app/rag_pipeline/retriever/retriever.py
import os
try:
    from langchain.retrievers.self_query import SelfQueryRetriever
except ImportError:
    SelfQueryRetriever = None

from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
from my_flask_app.rag_pipeline.embedding.main import OllamaNomicEmbedder
from my_flask_app.rag_pipeline.vectorestore.vectorestore import CSVChromaVectorStore
from my_flask_app.rag_pipeline.llm.main import modelcreation
class RAGPipeline:
    """
    Sets up a retrieval-augmented generation pipeline using Ollama-based embeddings,
    a Chroma vector store, and a self-query retriever (if available).
    """
    def __init__(self, csv_path="my_flask_app/data/data.csv"):
        
        self.csv_path = csv_path
        self.qa_chain = self._create_rag_pipeline()

    def _create_rag_pipeline(self):
        embedder = OllamaNomicEmbedder.factory()
        vectorstore_obj = CSVChromaVectorStore(self.csv_path, embedder)
        vectorstore = vectorstore_obj.get_vectorstore()
        llm = modelcreation().get_model()   
        if SelfQueryRetriever is not None:
            try:
                retriever = SelfQueryRetriever.from_llm(llm, vectorstore)
            except Exception as e:
                print("SelfQueryRetriever not available; using fallback retriever:", e)
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        else:
            print("SelfQueryRetriever is not installed; using fallback retriever.")
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        return qa_chain

    def process_query(self, query: str) -> str:
        result = self.qa_chain.run(query)
        return result
