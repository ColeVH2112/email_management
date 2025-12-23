from utils.llm_client import call_llama

def run(email_text):
    system_prompt = """
    You are a spam filter. 
    Analyze the email inside <EMAIL> tags.
    
    If it is spam, marketing, or a scam, reply with exactly one word: DELETE.
    If it is personal, school, or work related, reply with exactly one word: KEEP.
    
    Do not explain. Do not apologize. Just output the word.
    """
    
    safe_prompt = f"<EMAIL>\n{email_text}\n</EMAIL>"
    
    # We call the LLM, but we don't force JSON parsing anymore.
    # We just grab the raw text string.
    response = call_llama(safe_prompt, system_prompt, format_type="text")
    
    # Simple logic: Did it say "DELETE"?
    if "DELETE" in response.upper():
        return {"action": "DELETE", "reason": "Flagged by Gatekeeper"}
    else:
        return {"action": "KEEP", "reason": "Safe"}
    
