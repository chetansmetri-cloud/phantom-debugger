# app.py
from flask import Flask
from agent import run_diagnostics
import sys
import io

app = Flask(__name__)

@app.route('/')
def home():
    # Capture the output of your agent to display on the webpage
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    
    # Run the AI agent
    try:
        run_diagnostics()
    except Exception as e:
        print(f"Error running diagnostics: {e}")
        
    output = new_stdout.getvalue()
    sys.stdout = old_stdout
    
    # Display it on a spooky black webpage
    return f"""
    <body style="background-color: black; color: #00ff00; font-family: monospace; padding: 20px;">
        <h1>👻 Phantom Debugger Live</h1>
        <pre style="font-size: 16px;">{output}</pre>
    </body>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
