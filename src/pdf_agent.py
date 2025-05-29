import pdfplumber
from transformers import pipeline

class PDFAgent:
    def __init__(self, memory):
        self.memory = memory
        self.llm_extractor = pipeline("text2text-generation", model="google/flan-t5-base")  # Replace with GPT-4 API if needed

    def process(self, input_path, thread_id):
        # Extract text from PDF
        with pdfplumber.open(input_path) as pdf:
            text = "".join(page.extract_text() or "" for page in pdf.pages)

        # LLM prompts for each field
        def extract_field(prompt):
            try:
                output = self.llm_extractor(prompt, max_new_tokens=30)[0]["generated_text"]
                return output.strip()
            except Exception as e:
                return "unknown"

        invoice_number = extract_field(f"Extract the invoice number from this document:\n{text}")
        amount = extract_field(f"Extract the total amount in dollars from this document:\n{text}")
        date = extract_field(f"Extract the invoice date from this document:\n{text}")

        formatted_data = {
            "invoice_number": invoice_number,
            "amount": amount,
            "date": date
        }

        # Detect anomalies
        anomalies = []
        for key, value in formatted_data.items():
            if value in ["", "unknown"]:
                anomalies.append(f"Missing or unclear: {key}")

        result = {
            "formatted_data": formatted_data,
            "anomalies": anomalies
        }

        # Save to memory
        self.memory.save(input_path, "pdf", result)

        return result
