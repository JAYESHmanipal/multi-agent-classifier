import os
from classifier import ClassifierAgent
from json_agent import JSONAgent
from email_agent import EmailAgent
from pdf_agent import PDFAgent
from memory import SharedMemory

def main(input_path):
    # Initialize components
    memory = SharedMemory()
    classifier = ClassifierAgent(memory)
    json_agent = JSONAgent(memory)
    email_agent = EmailAgent(memory)
    pdf_agent = PDFAgent(memory)

    # Classify input
    format_, intent, thread_id = classifier.classify(input_path)
    if not format_:
        print(f"Error: {thread_id}")
        return

    print(f"Classified: format={format_}, intent={intent}, thread_id={thread_id}")

    # Route to appropriate agent
    result = None
    if format_ == "json":
        result = json_agent.process(input_path, thread_id)
    elif format_ == "email":
        result = email_agent.process(input_path, thread_id)
    elif format_ == "pdf":
        result = pdf_agent.process(input_path, thread_id)

    # Log result
    log_dir = "outputs"
    log_file = os.path.join(log_dir, "logs.txt")
    print(f"Attempting to log to: {os.path.abspath(log_file)}")
    try:
        os.makedirs(log_dir, exist_ok=True)
        print(f"Log directory {log_dir} exists or was created.")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"Thread ID: {thread_id}\n")
            f.write(f"Input: {input_path}\n")
            f.write(f"Format: {format_}, Intent: {intent}\n")
            f.write(f"Result: {result}\n")
            f.write("-" * 50 + "\n")
        print(f"Successfully wrote to {log_file}")
    except Exception as e:
        print(f"Failed to write to log file: {e}")

    print("Result:", result)

if __name__ == "__main__":
    # Test with sample inputs
    input_files = ["inputs/order.json", "inputs/rfq.eml", "inputs/invoice.pdf"]
    print("Current directory:", os.getcwd())
    for input_file in input_files:
        resolved_path = os.path.abspath(input_file)
        print(f"Resolved path for {input_file}: {resolved_path}")
        if os.path.exists(input_file):
            print(f"\nProcessing {input_file}...")
            main(input_file)
        else:
            print(f"File not found: {input_file}")