import os
from pathlib import Path

# Webmail URL — Stanford redirects to outlook.office.com, but you can override
# e.g. "https://webmail.stanford.edu" or "https://outlook.office.com/mail/inbox"
OWA_URL = os.getenv("OWA_URL", "https://outlook.office.com/mail/inbox")

# Where to store the saved browser session (cookies)
SESSION_FILE = Path.home() / ".email_management_session.json"

# How long a saved session stays valid before forcing a re-login (hours)
SESSION_MAX_AGE_HOURS = int(os.getenv("SESSION_MAX_AGE_HOURS", "10"))

# Max emails to pull from the inbox each run
MAX_EMAILS = int(os.getenv("MAX_EMAILS", "30"))

# Local Ollama settings
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("LLM_MODEL", "llama3.2")
