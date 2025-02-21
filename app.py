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

# This will track where we last read the file
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
            max_tokens=5  # adjust as needed
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

class TailEventHandler(FileSystemEventHandler):
    """Watchdog event handler that reads only new appended data."""
    def on_modified(self, event):
        global last_position
        if event.src_path == MONITOR_FILE:
            try:
                with open(MONITOR_FILE, 'r', encoding='utf-8') as f:
                    f.seek(last_position)
                    new_data = f.read()
                    last_position = f.tell()
                if new_data:
                    print(f"New data detected: {new_data!r}")
                    update_explanation(new_data)
            except Exception as e:
                print(f"Error reading new data from file: {e}")

if __name__ == "__main__":
    if os.access(MONITOR_FILE, os.R_OK):
        print("Read access granted.")
    else:
        print("Read access denied.")
        exit(1)

    # Initialize last_position to the current end of file to avoid processing old content
    if os.path.exists(MONITOR_FILE):
        with open(MONITOR_FILE, 'r', encoding='utf-8') as f:
            f.seek(0, os.SEEK_END)
            last_position = f.tell()

    event_handler = TailEventHandler()
    observer = Observer()
    # Monitor the directory that contains the file (not the file itself)
    observer.schedule(event_handler, path=os.path.dirname(MONITOR_FILE), recursive=False)
    observer.start()
    print(f"Monitoring file: {MONITOR_FILE}")

    try:
        # Use a small sleep interval to be responsive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
