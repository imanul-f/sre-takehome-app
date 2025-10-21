from flask import Flask
import psutil # pip install psutil

app = Flask(__name__)

@app.route('/')
def os_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent # Use '/' for WSL or 'C:/' if accessing from Windows container

    info = f"CPU Usage: {cpu_percent}%<br>Memory Usage: {memory_percent}%<br>Disk Usage: {disk_percent}%"
    return info

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
