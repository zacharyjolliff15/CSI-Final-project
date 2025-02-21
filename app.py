import os
import time
import webbrowser
import openai
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Use your own OpenAI API key (ensure you keep this secure)
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
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please provide a detailed explanation of the following content:\n\n{new_content}"}
            ],
            max_tokens=150  # adjust as needed
        )
        explanation = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        explanation = "Error generating explanation."

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>File Explanation</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 2em;
        }}
        pre {{
            background: #f4f4f4;
            padding: 1em;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <h1>File Explanation</h1>
    <pre>{explanation}</pre>
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
    # Open the file and move the pointer to its end to ignore existing content.
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
                    print(f"New data: {new_data!r}")
                    update_explanation(new_data)
                last_position = f.tell()
        except Exception as e:
            print(f"Error reading file: {e}")
        time.sleep(0.5)  # Poll every half-second 

if __name__ == "__main__":
    poll_file()
