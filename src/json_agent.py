import json
from classifier import ClassifierAgent  # Import your existing LLM-enhanced classifier

class JSONAgent:
    def __init__(self, memory):
        self.memory = memory
        self.classifier = ClassifierAgent(memory)

    def process(self, input_path, thread_id):
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return {"error": f"Failed to parse JSON: {str(e)}"}

        # Step 1: Basic schema validation
        required_fields = ["order_id", "customer", "amount", "date"]
        formatted_data = {field: data.get(field, "unknown") for field in required_fields}

        # Step 2: Check for simple anomalies
        anomalies = []
        for field, value in formatted_data.items():
            if value == "unknown":
                anomalies.append(f"Missing field: {field}")

        # Step 3: Use LLM to classify intent of the JSON content
        try:
            json_text = json.dumps(data, indent=2)
            intent = self.classifier._classify_intent_llm(json_text)
        except Exception as e:
            print(f"LLM intent classification failed: {e}")
            intent = "unknown"

        # Optionally: Use LLM to detect data quality/contextual issues
        context_anomaly = self._llm_check_for_anomalies(json_text)
        if context_anomaly:
            anomalies.append(context_anomaly)

        result = {
            "formatted_data": formatted_data,
            "intent": intent,
            "anomalies": anomalies
        }

        self.memory.save(input_path, "json", result)
        return result

    def _llm_check_for_anomalies(self, text):
        try:
            prompt = (
                "Analyze the following JSON and identify if there are any contextual anomalies, "
                "such as unreasonable amounts, incorrect data types, or suspicious values. "
                "Respond with a short sentence or 'None' if all looks good.\n\n"
                f"{text}"
            )
            result = self.classifier.llm_classifier(prompt, ["anomaly detected", "none"])
            return "Potential contextual anomaly" if result["labels"][0] == "anomaly detected" else None
        except Exception as e:
            print(f"LLM anomaly check failed: {e}")
            return None
