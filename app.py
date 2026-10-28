# app.py
from flask import Flask
from agent import run_diagnostics
import sys
import io
import html

app = Flask(__name__)

@app.route('/')
def home():
    # Capture the agent's terminal output
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    
    try:
        run_diagnostics()
    except Exception as e:
        print(f"Error running diagnostics: {e}")
        
    output = new_stdout.getvalue()
    sys.stdout = old_stdout
    safe_output = html.escape(output)
    
    # Premium Cyberpunk/Necromancer Dashboard UI
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Phantom Debugger | Ghost in the Machine</title>
        <style>
            :root {{
                --primary-glow: #00ff41;
                --bg-color: #050505;
                --panel-bg: rgba(0, 20, 0, 0.7);
            }}
            body {{
                background-color: var(--bg-color);
                color: var(--primary-glow);
                font-family: 'Courier New', Courier, monospace;
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                overflow-x: hidden;
            }}
            .scanlines {{
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                            linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
                background-size: 100% 2px, 3px 100%;
                pointer-events: none;
                z-index: 50;
            }}
            .dashboard {{
                width: 100%;
                max-width: 1000px;
                background: var(--panel-bg);
                border: 1px solid var(--primary-glow);
                box-shadow: 0 0 15px rgba(0, 255, 65, 0.3), inset 0 0 20px rgba(0, 255, 65, 0.1);
                padding: 30px;
                border-radius: 5px;
                position: relative;
                z-index: 10;
            }}
            .header {{
                text-align: center;
                border-bottom: 2px solid var(--primary-glow);
                padding-bottom: 20px;
                margin-bottom: 20px;
            }}
            /* Glitch Effect */
            .glitch {{
                font-size: 2.5em;
                font-weight: bold;
                text-transform: uppercase;
                position: relative;
                text-shadow: 0.05em 0 0 rgba(255,0,0,0.75), -0.025em -0.05em 0 rgba(0,255,0,0.75), 0.025em 0.05em 0 rgba(0,0,255,0.75);
                animation: glitch 500ms infinite;
                margin: 0;
            }}
            @keyframes glitch {{
                0% {{ text-shadow: 0.05em 0 0 rgba(255,0,0,0.75), -0.05em -0.025em 0 rgba(0,255,0,0.75), -0.025em 0.05em 0 rgba(0,0,255,0.75); }}
                14% {{ text-shadow: 0.05em 0 0 rgba(255,0,0,0.75), -0.05em -0.025em 0 rgba(0,255,0,0.75), -0.025em 0.05em 0 rgba(0,0,255,0.75); }}
                15% {{ text-shadow: -0.05em -0.025em 0 rgba(255,0,0,0.75), 0.025em 0.025em 0 rgba(0,255,0,0.75), -0.05em -0.05em 0 rgba(0,0,255,0.75); }}
                49% {{ text-shadow: -0.05em -0.025em 0 rgba(255,0,0,0.75), 0.025em 0.025em 0 rgba(0,255,0,0.75), -0.05em -0.05em 0 rgba(0,0,255,0.75); }}
                50% {{ text-shadow: 0.025em 0.05em 0 rgba(255,0,0,0.75), 0.05em 0 0 rgba(0,255,0,0.75), 0 -0.05em 0 rgba(0,0,255,0.75); }}
                99% {{ text-shadow: 0.025em 0.05em 0 rgba(255,0,0,0.75), 0.05em 0 0 rgba(0,255,0,0.75), 0 -0.05em 0 rgba(0,0,255,0.75); }}
                100% {{ text-shadow: -0.025em 0 0 rgba(255,0,0,0.75), -0.025em -0.025em 0 rgba(0,255,0,0.75), -0.025em -0.05em 0 rgba(0,0,255,0.75); }}
            }}
            .subtitle {{
                font-size: 1.1em;
                letter-spacing: 2px;
                color: #888;
                margin-top: 10px;
            }}
            .console-window {{
                background: #000;
                padding: 20px;
                border: 1px solid #333;
                height: 400px;
                overflow-y: auto;
                box-shadow: inset 0 0 10px #000;
            }}
            pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
                font-size: 16px;
                line-height: 1.5;
                margin: 0;
            }}
            .cursor {{
                display: inline-block;
                width: 10px;
                height: 1.2em;
                background-color: var(--primary-glow);
                vertical-align: middle;
                animation: blink 1s step-end infinite;
            }}
            @keyframes blink {{ 50% {{ opacity: 0; }} }}
            .footer {{
                text-align: right;
                margin-top: 20px;
                font-size: 0.9em;
                color: #555;
            }}
            .team-name {{
                color: var(--primary-glow);
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="scanlines"></div>
        <div class="dashboard">
            <div class="header">
                <h1 class="glitch">PHANTOM_DEBUGGER.exe</h1>
                <div class="subtitle">AUTONOMOUS NECROMANCER PROTOCOL v1.0</div>
            </div>
            
            <div class="console-window" id="console">
                <pre id="output-text"></pre>
                <span class="cursor"></span>
            </div>
            
            <div class="footer">
                ENGINEERED BY <span class="team-name">TEAM NEXTGEN-ERA</span>
            </div>
        </div>

        <!-- Hidden data -->
        <div id="raw-data" style="display:none;">{safe_output}</div>

        <script>
            const terminal = document.getElementById('output-text');
            const finalData = document.getElementById('raw-data').innerText;
            const consoleWindow = document.getElementById('console');
            
            // The Boot Sequence Array
            const bootSequence = [
                "> INITIATING SECURE UPLINK...",
                "> BYPASSING MAINFRAME FIREWALLS... [OK]",
                "> TEAM NEXTGEN-ERA CREDENTIALS ACCEPTED.",
                "> ESTABLISHING CONNECTION TO MONGODB ATLAS (MEMORY VAULT)...",
                "> RETRIEVING DEAD PROCESS LOGS...",
                "> LOG IDENTIFIED. STATUS: FATAL.",
                "> AWAKENING GOOGLE GEMMA (OPEN-WEIGHT REASONING ENGINE)...",
                "> EXECUTING AUTOPSY...",
                "--------------------------------------------------",
                " "
            ];

            let seqIndex = 0;
            let charIndex = 0;

            function scrollToBottom() {{
                consoleWindow.scrollTop = consoleWindow.scrollHeight;
            }}

            // Step 1: Type out the fake boot sequence
            function typeBootSequence() {{
                if (seqIndex < bootSequence.length) {{
                    terminal.innerHTML += bootSequence[seqIndex] + "\\n";
                    seqIndex++;
                    scrollToBottom();
                    setTimeout(typeBootSequence, Math.random() * 400 + 200); // Random delay between 200ms-600ms
                }} else {{
                    setTimeout(typeFinalData, 500); // Wait half a second before printing real AI output
                }}
            }}

            // Step 2: Type out the actual output from Gemma & Python
            function typeFinalData() {{
                if (charIndex < finalData.length) {{
                    terminal.innerHTML += finalData.charAt(charIndex);
                    charIndex++;
                    scrollToBottom();
                    setTimeout(typeFinalData, 15); // Fast typing for the AI output
                }}
            }}

            // Start the sequence
            setTimeout(typeBootSequence, 1000);
        </script>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
