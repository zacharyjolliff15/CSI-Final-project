import os
import time
import webbrowser
import openai
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

openai.api_key = ''

MONITOR_FILE = r'C:\ProgramData\MySQL\MySQL Server 8.0\Data\DESKTOP-BDLUB0E-slow.log'
HTML_FILE = 'index.html'
last_position = 0

def update_explanation(new_content):
    """Call OpenAI to explain the new content, update HTML file, and open in browser."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a senior database administrator and performance tuning expert."},
                {"role": "user", "content": f"Analyze this MySQL slow query log entry. Explain the potential performance issues, suggest optimizations, and recommend indexes if applicable:\n\n{new_content}"}
            ],
            max_tokens=5 
        )
        explanation = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        explanation = "Error generating analysis. Please check the API connection."

    # Get current date/time for report
    analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MySQL Query Analysis Report</title>
    <style>
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --background-color: #f8f9fa;
            --success-color: #27ae60;
        }}

        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: var(--background-color);
            color: var(--primary-color);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .header {{
            background-color: var(--primary-color);
            color: white;
            padding: 1.5rem 0;
            margin-bottom: 2rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        .report-title {{
            font-size: 2.5rem;
            margin: 0;
            font-weight: 300;
            text-align: center;
        }}

        .report-metadata {{
            display: flex;
            justify-content: space-between;
            margin: 1.5rem 0;
            padding: 1rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 3px rgba(0,0,0,0.05);
        }}

        .explanation-box {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin: 2rem 0;
            white-space: pre-wrap;
            font-family: 'Consolas', monospace;
            line-height: 1.8;
            border-left: 4px solid var(--secondary-color);
            position: relative;
        }}

        .explanation-box::before {{
            content: 'Query Analysis';
            position: absolute;
            top: -15px;
            left: -4px;
            background: var(--secondary-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 4px 4px 0 0;
            font-size: 0.9rem;
            font-weight: bold;
        }}

        .status-indicator {{
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            background: var(--success-color);
            color: white;
            font-weight: bold;
        }}

        .status-indicator::before {{
            content: '';
            display: block;
            width: 10px;
            height: 10px;
            background: white;
            border-radius: 50%;
            margin-right: 0.5rem;
        }}

        footer {{
            text-align: center;
            padding: 2rem;
            color: #666;
            border-top: 1px solid #eee;
            margin-top: 3rem;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}
            
            .report-metadata {{
                flex-direction: column;
                gap: 1rem;
            }}
            
            .report-title {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="report-title">MySQL Query Analysis Report</h1>
        </div>
    </header>

    <div class="container">
        <div class="report-metadata">
            <div>
                <h3>Analysis Status</h3>
                <div class="status-indicator">
                    Complete
                </div>
            </div>
            <div>
                <h3>Analysis Date</h3>
                <p>{analysis_date}</p>
            </div>
            <div>
                <h3>Log Source</h3>
                <p>{os.path.basename(MONITOR_FILE)}</p>
            </div>
        </div>

        <div class="explanation-box">
            {explanation}
        </div>
    </div>

    <footer>
        <div class="container">
            <p>© 2024. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
"""

    try:
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
    except Exception as e:
        print(f"Error writing HTML file: {e}")
        return

    file_url = 'file://' + os.path.realpath(HTML_FILE)
    webbrowser.open(file_url)
    print("HTML display updated.")

def poll_file():
    global last_position
    with open(MONITOR_FILE, 'r', encoding='utf-8') as f:
        f.seek(0, os.SEEK_END)
        last_position = f.tell()

    while True:
        try:
            with open(MONITOR_FILE, 'r', encoding='utf-8') as f:
                f.seek(last_position)
                new_data = f.read()
                if new_data:
                    print(f"New data detected: {new_data[:100]}...")  # Truncate log for console
                    update_explanation(new_data)
                last_position = f.tell()
        except Exception as e:
            print(f"Error reading file: {e}")
        time.sleep(1)  # Reduced polling frequency

if __name__ == "__main__":
    poll_file()