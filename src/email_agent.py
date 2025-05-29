import mailparser
import re
from classifier import ClassifierAgent  # Make sure this is correctly imported

class EmailAgent:
    def __init__(self, memory):
        self.memory = memory
        self.classifier = ClassifierAgent(memory)  # Use existing classifier with LLM

    def process(self, input_path, thread_id):
        # Parse email
        email = mailparser.parse_from_file(input_path)
        sender = email.from_[0][1] if email.from_ else "unknown"
        body = email.text_plain[0] if email.text_plain else ""

        # Extract subject manually
        with open(input_path, "r", encoding="utf-8") as f:
            raw_email = f.read()
        subject_match = re.search(r"Subject:\s*(.+)", raw_email)
        subject = subject_match.group(1).strip() if subject_match else "unknown"

        # Use LLM for better intent
        intent = self.classifier._classify_intent_llm(body)

        # Use LLM to classify urgency (custom trick: classify as high/medium/low urgency)
        urgency = self._classify_urgency_llm(body)

        result = {
            "sender": sender,
            "intent": intent,
            "urgency": urgency,
            "subject": subject
        }

        self.memory.save(input_path, "email", result)
        return result

    def _classify_urgency_llm(self, text):
        # Custom LLM-based urgency classification
        labels = ["high urgency", "medium urgency", "low urgency"]
        try:
            result = self.classifier.llm_classifier(text, labels)
            top_label = result['labels'][0]
            return top_label.replace(" urgency", "")  # returns 'high', 'medium', or 'low'
        except Exception as e:
            print(f"Urgency LLM classification failed: {e}")
            return "normal"
