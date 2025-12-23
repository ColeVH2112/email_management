from utils.llm_client import call_llama

def run(email_text, analyst_data):
    system_prompt = f"""
    You are an Executive Secretary. Write a concise, one/two sentence summary of this email for your boss.

    CONTEXT FROM ANALYST:
    {analyst_data}

    INSTRUCTIONS:
    - If it's an event, mention the date/time/location clearly.
    - If its a tast, mention the deadline
    - Keep it professional an very concise
    -Do NOT include generic phrase such as "The email discusses..." just state the important facts

    output JSON ONLY: {{"summary": "Your summary text here" }}
    """

    safe_prompt = f"<EMAIL>\n{email_text}\n</EMAIL>"

    print("Secretary writing report...")

    return call_llama(safe_prompt, system_prompt)
