import os
import time
import webbrowser
import openai
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Use your own OpenAI API key (ensure you keep this secure)
openai.api_key = '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'

MONITOR_DIR = r'C:\ProgramData\MySQL\MySQL Server 8.0\Data\mysql\slow_log.csv'
HTML_FILE = 'index.html'

def process_file(file_path):
    """Read file content, get explanation from OpenAI, update HTML, and open in browser."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please provide a detailed explanation of the following content:\n\n{file_content}"}
            ],
            max_tokens=5
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
    print(f"Processed {file_path} and updated HTML display.")

class FileEventHandler(FileSystemEventHandler):
    """Handler for file system events."""
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file created: {event.src_path}")
            process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            process_file(event.src_path)

if __name__ == "__main__":
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=MONITOR_DIR, recursive=False)
    observer.start()
    print(f"Monitoring folder: {MONITOR_DIR}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
