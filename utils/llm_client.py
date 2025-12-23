import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

def call_llama(prompt, system_role, format_type="json"):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "system": system_role,
        "stream": False,
        "options": {"temperature": 0.1}
    }
    
    # Only force JSON mode if we actually asked for it
    if format_type == "json":
        payload["format"] = "json"

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        raw_text = response.json()['response']

        # IF WE WANT TEXT (Gatekeeper/Secretary), just return the string!
        if format_type == "text":
            return raw_text

        # IF WE WANT JSON (Analyst), parse it safely
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            # Regex fallback
            json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            return {}

    except Exception as e:
        print(f"LLLM Error: {e}")
        return {} if format_type == "json" else "Error"
