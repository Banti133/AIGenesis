import os
from dotenv import load_dotenv
from google import genai
from typing import List, Dict, Tuple
import numpy as np
import re

load_dotenv()


class Document:
    def __init__(self, content: str, metadata: Dict = None):
        self.content = content
        self.metadata = metadata or {}
        self.id = id(self)


class AdvancedRAGAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-2.5-flash"

        self.documents: List[Document] = []
        self.document_embeddings: Dict[int, np.ndarray] = {}

    # ================= EMBEDDINGS =================
    def embed_text(self, text: str) -> np.ndarray:
        result = self.client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return np.array(result.embeddings[0].values)

    # ================= ADD DOCUMENT =================
    def add_document(self, content: str, metadata: Dict = None):
        doc = Document(content, metadata)
        self.documents.append(doc)
        self.document_embeddings[doc.id] = self.embed_text(content)
        print(f"✓ Added document {len(self.documents)}")

    def add_documents_from_text(self, text: str, chunk_size: int = 500):
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunk = ""

        for sentence in sentences:
            if len(chunk) + len(sentence) > chunk_size:
                self.add_document(chunk.strip())
                chunk = ""
            chunk += sentence + " "

        if chunk.strip():
            self.add_document(chunk.strip())

    def load_from_file(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            self.add_documents_from_text(f.read())
        print(f"✓ Loaded file {filepath}")

    # ================= SIMILARITY =================
    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def retrieve_relevant_documents(self, query: str, top_k: int = 3):
        query_embedding = self.embed_text(query)
        scores = []

        for doc in self.documents:
            sim = self.cosine_similarity(query_embedding, self.document_embeddings[doc.id])
            scores.append((doc, float(sim)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    # ================= GENERATION =================
    def answer_question(self, question: str, top_k: int = 3):
        relevant_docs = self.retrieve_relevant_documents(question, top_k)

        if not relevant_docs:
            return {"answer": "No information found.", "sources": []}

        context = "\n\n".join([doc.content for doc, _ in relevant_docs])

        prompt = f"""
Answer the question using ONLY the context below.
If answer not present, say you don't know.

Context:
{context}

Question: {question}
Answer:
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        return {
            "answer": response.text,
            "sources": [doc.content[:100] for doc, _ in relevant_docs]
        }

    # ================= STATS =================
    def get_stats(self):
        return {
            "documents": len(self.documents),
            "embeddings": len(self.document_embeddings)
        }


# ================= INTERACTIVE MODE =================
def interactive_rag():
    print("📚 Advanced RAG Agent (Embedding Powered)")
    agent = AdvancedRAGAgent()

    # Sample knowledge
    agent.add_document("Python is used for AI, data science, and automation.")
    agent.add_document("Machine learning models learn patterns from data.")
    agent.add_document("Neural networks are inspired by the human brain.")

    while True:
        q = input("\nAsk: ")
        if q.lower() in ["exit", "quit"]:
            break

        result = agent.answer_question(q)
        print("\nAnswer:", result["answer"])
        print("\nSources:", result["sources"])


if __name__ == "__main__":
    interactive_rag()
