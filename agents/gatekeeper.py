from utils.llm_client import call_llama

def run(email_text):
    system_prompt = """
    You are an email security filer.
    Analyze the text inside <EMAIL>tags.

    CRITERIA:
    -KEEP: Personal, Professors, Job Offers, Exams, Hackathons, Tech Conferences, VC's.
    - DELETE: Newsletters, Marketing, Spam, Recruiters, Submission notifications.

    Outpute JSON: {"action": "KEEP" or "DELETE", "reason": "Short explanation"}
    """

    safe_prompt = f"<EMAIL>\n{email_text}\n</EMAIL>"

    print("Gatekeeper Analyzing...")

    return call_llama(safe_prompt, system_prompt)
