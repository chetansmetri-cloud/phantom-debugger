# agent.py
import os
import requests
from database import connect_to_vault

# We will use the free Hugging Face API to access Gemma 
HF_API_KEY = os.environ.get("HF_API_KEY", "YOUR_HUGGINGFACE_TOKEN_HERE")
GEMMA_API_URL = "https://api-inference.huggingface.co/models/google/gemma-2b-it"

def ask_gemma(prompt):
    """Sends the autopsy report to Google Gemma for a resolution."""
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 100}}
    
    print("🧠 Consulting Gemma (The Phantom Brain)...")
    try:
        response = requests.post(GEMMA_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()[0]['generated_text']
        return result.replace(prompt, "").strip()
    except Exception as e:
        return f"⚠️ Gemma failed to respond: {e}"

def run_diagnostics():
    """Main workflow: Pull dead log, ask Gemma, return fix."""
    db_collection = connect_to_vault()
    if db_collection is None:
        return "Database connection failed."
        
    # Retrieve a 'dead' log from our ancient texts
    dead_process = db_collection.find_one({"status": "dead"})
    if not dead_process:
        return "No dead processes found. System is healthy."
        
    error_context = f"Error Code: {dead_process['error_code']} - {dead_process['log_pattern']}"
    
    # Format the prompt for Gemma (matching the Ghost in the Machine theme)
    prompt = (
        f"You are a necromancer AI debugging a legacy system. "
        f"A process died with this error: {error_context}. "
        f"The ancient texts suggest this fix: {dead_process['resolution']}. "
        f"Write a short, spooky command-line message applying this fix."
    )
    
    fix_message = ask_gemma(prompt)
    
    print("\n--- PHANTOM DEBUGGER OUTPUT ---")
    print(f"Target: {error_context}")
    print(f"Resolution: {fix_message}")
    print("-------------------------------\n")

if __name__ == "__main__":
    run_diagnostics()
