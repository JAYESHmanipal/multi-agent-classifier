import re

raw_email = """From: john@example.com
To: sales@company.com
Subject: Request for Quote
Date: Thu, 29 May 2025 09:44:00 +0530

Dear Sales Team,

Please provide a quote for 100 units of Widget X by tomorrow. This is urgent.

Regards,
John Doe"""

subject_match = re.search(r"Subject:\s*(.+)", raw_email)
subject = subject_match.group(1).strip() if subject_match else "unknown"
print("Test extracted subject:", subject)