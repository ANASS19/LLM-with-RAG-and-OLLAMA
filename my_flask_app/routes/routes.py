# my_flask_app/routes/routes.py
from flask import Blueprint, request, jsonify
from my_flask_app.rag_pipeline.retriever.retriever import RAGPipeline
import traceback

api = Blueprint('api', __name__)

@api.route('/llm', methods=['POST'])
def llm_endpoint():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    try:
        openai_api_key = "REPLACE_WITH_YOUR_OPENAI_KEY"  # <-- Set your actual OpenAI key here.
        rag = RAGPipeline(csv_path="my_flask_app/data/data.csv")
        response = rag.process_query(prompt)
        return jsonify({"response": response})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
