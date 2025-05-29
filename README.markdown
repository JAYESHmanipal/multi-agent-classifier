```markdown
# Multi-Agent System for File Processing

## Overview
This project implements a multi-agent system to process different file types (JSON, email, PDF) using specialized agents. The system consists of:
- **Classifier Agent**: Identifies the file format and intent.
- **JSON Agent**: Processes JSON files (e.g., orders).
- **Email Agent**: Processes email files (e.g., RFQs).
- **PDF Agent**: Processes PDF files (e.g., invoices).
- **Shared Memory**: Stores processed data in a SQLite database (`memory.db`).

The system processes input files, logs results to `outputs/logs.txt`, and saves processed data to `outputs/memory.db`. 

## Folder Structure
```
multi-agent-system/
├── inputs/
│   ├── order.json        # Sample JSON file (order data)
│   ├── rfq.eml           # Sample email file (request for quote)
│   ├── invoice.pdf       # Sample PDF file (invoice)
├── outputs/
│   ├── logs.txt          # Output logs from processing
├── src/
│   ├── classifier.py     # Classifier Agent to identify file format and intent
│   ├── email_agent.py    # Email Agent to process .eml files
│   ├── json_agent.py     # JSON Agent to process .json files
│   ├── main.py           # Main script to orchestrate the agents
│   ├── memory.py         # Shared Memory implementation using SQLite
│   ├── pdf_agent.py      # PDF Agent to process .pdf files
│   ├── query_memory.py   # Utility script to query memory.db
│   ├── test_regex.py     # Utility script to test regex for email parsing
│   ├── extract_pdf_text.py # Utility script to extract text from invoice.pdf
├── demo.mp4              # Video demo of the project
├── README.md             # Project documentation
├── .gitignore            # Git ignore file to exclude unnecessary files
```

## Prerequisites
- **Python 3.10+**: Ensure Python is installed on your system.
- **Dependencies**:
  - `mailparser`: For parsing email files.
  - `pdfplumber`: For extracting text from PDF files.
- **Optional**: SQLite (to directly query `memory.db`).

## Setup Instructions

## Running the Project
1. **Ensure Input Files Are Present**:
   - The `inputs/` folder should contain:
     - `order.json`: A sample order in JSON format.
     - `rfq.eml`: A sample request for quote email.
     - `invoice.pdf`: A sample invoice in PDF format.

2. **Run the Main Script**:
   ```
   python src/main.py
   ```
   - The script processes each file in `inputs/`.
   - Results are logged to `outputs/logs.txt`.
   - Processed data is stored in `outputs/memory.db`.

3. **View Outputs**:
   - **Logs**: Check `outputs/logs.txt` for processing results.
   - **Database**: Query `outputs/memory.db` to see stored data.
     - If SQLite is installed:
       ```
       sqlite3 outputs/memory.db "SELECT * FROM memory;"
       ```
     - Alternatively, use the provided script:
       ```
       python src/query_memory.py
       ```

## Sample Input Files
- **`order.json`**:
  ```json
  {
    "order_id": "ORD-456",
    "customer": "Jane Doe",
    "amount": 1000,
    "date": "2025-05-29"
  }
  ```
- **`rfq.eml`**:
  ```
  From: john@example.com
  To: sales@company.com
  Subject: Request for Quote
  Date: Thu, 29 May 2025 09:44:00 +0530

  Dear Sales Team,

  Please provide a quote for 100 units of Widget X by tomorrow. This is urgent.

  Regards,
  John Doe
  ```
- **`invoice.pdf`**:
  - A PDF file containing:
    ```
    Invoice #INV-123
    Amount: $500.00
    Date: 2025-05-29
    ```

## Sample Output
- **`logs.txt`**:
  ```
  Thread ID: b3ab956e-81ae-45fc-b5f4-c82b0e58e7c5
  Input: inputs/order.json
  Format: json, Intent: unknown
  Result: {'formatted_data': {'order_id': 'ORD-456', 'customer': 'Jane Doe', 'amount': 1000, 'date': '2025-05-29'}, 'anomalies': []}
  --------------------------------------------------
  Thread ID: c29fa164-b9a3-4122-8c44-cd65d95b7e4a
  Input: inputs/rfq.eml
  Format: email, Intent: rfq
  Result: {'sender': 'john@example.com', 'intent': 'rfq', 'urgency': 'high', 'subject': 'Request for Quote'}
  --------------------------------------------------
  Thread ID: 6e5d461c-78e1-4400-a7a5-c02cadeaf673
  Input: inputs/invoice.pdf
  Format: pdf, Intent: invoice
  Result: {'formatted_data': {'invoice_number': 'unknown', 'amount': 500.0, 'date': '2025-05-29'}, 'anomalies': ['Missing field: invoice_number']}
  --------------------------------------------------
  ```

- **`memory.db`** (queried using `query_memory.py`):
  ```
  ('b3ab956e-81ae-45fc-b5f4-c82b0e58e7c5', 'inputs/order.json', 'json', '2025-05-29T<time>', "{'order_id': 'ORD-456', 'customer': 'Jane Doe', 'amount': 1000, 'date': '2025-05-29'}")
  ('c29fa164-b9a3-4122-8c44-cd65d95b7e4a', 'inputs/rfq.eml', 'email', '2025-05-29T<time>', "{'sender': 'john@example.com', 'intent': 'rfq', 'urgency': 'high', 'subject': 'Request for Quote'}")
  ('6e5d461c-78e1-4400-a7a5-c02cadeaf673', 'inputs/invoice.pdf', 'pdf', '2025-05-29T<time>', "{'invoice_number': 'unknown', 'amount': 500.0, 'date': '2025-05-29'}")
  ```
