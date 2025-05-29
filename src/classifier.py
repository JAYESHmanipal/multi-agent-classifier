import os
from transformers import pipeline

class ClassifierAgent:
    def __init__(self, memory):
        self.memory = memory
        self.llm_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def classify(self, input_path):
        print(f"Classifying {input_path}...")
        thread_id = None

        # Format classification
        _, ext = os.path.splitext(input_path)
        ext = ext.lower()
        if ext == ".json":
            format_ = "json"
        elif ext == ".eml":
            format_ = "email"
        elif ext == ".pdf":
            format_ = "pdf"
        else:
            format_ = None

        intent = "unknown"

        # Load text content from file
        content = self._extract_text(input_path, format_)
        if content:
            # Intent classification using LLM
            intent = self._classify_intent_llm(content)

        if format_:
            classification_data = {"format": format_, "intent": intent}
            thread_id = self.memory.save(input_path, format_, classification_data)
            print(f"Saved to memory with thread_id: {thread_id}")
        else:
            print("Format not recognized")

        return format_, intent, thread_id

    def _extract_text(self, input_path, format_):
        try:
            if format_ == "email" or format_ == "json":
                with open(input_path, "r", encoding="utf-8") as f:
                    return f.read()
            elif format_ == "pdf":
                from PyPDF2 import PdfReader
                reader = PdfReader(input_path)
                return " ".join(page.extract_text() for page in reader.pages if page.extract_text())
        except Exception as e:
            print(f"Failed to extract text from {input_path}: {e}")
            return ""

    def _classify_intent_llm(self, text):
        candidate_labels = ["invoice", "rfq", "complaint", "regulation", "query", "other"]
        try:
            result = self.llm_classifier(text, candidate_labels)
            return result['labels'][0]  # Top intent
        except Exception as e:
            print(f"LLM classification failed: {e}")
            return "unknown"
