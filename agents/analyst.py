from utils.llm_client import call_llama
from datetime import datetime


def run(email_text):
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    system_prompt = f"""
    You are a Data Analyst. Your job is to extract structured data from the email text provided inside <EMAIL> tags. Today is {today} 

    INSTRUCTIONS:
    1. Identify if there is a specific Event, Deadline, or Meeting.
    2. Extract the Date and Time in ISO format (YYYY-MM-DD HH:MM) if possible.
    3. If the email says "Next Tuesday", CALCULATE the date based on today ({today})
    4. If you can not calculate the ISO date, copy the text (e.g. next tuesday, and include the current date ({today}))
    5. Extract the location.
    6. Determine urgency (High/Medium/Low).

    Output JSON ONLY:
    {{
        "has_event" : true/false,
        "event_name" : "short name or null",
        "date: "YYYY-MM-DD or text description",
        "location" : "Location or null",
        "urgency": "High/Medium/Low"
    }}
    """

    safe_prompt = f"<EMAIL>\n{email_text}\n</EMAIL>"

    print("Analyst extracting...")

    return call_llama(safe_prompt, system_prompt)

