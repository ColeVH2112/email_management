import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

def call_llama(prompt, system_role):
    payload = {
        "model" : MODEL,
        "prompt" : prompt,
        "system" : system_role,
        "stream" : False,
        "formate" : "json",
        "options" : {"temperature" : 0.1}
        }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return json.loads(response.json()['response'])

    except json.JSONDecodeError:
        print(f"LLM output error: model returned invalid JSON")
        return {}
    
    except Exception as e:
        print (f"LLM Error: {e}")
        return {}

