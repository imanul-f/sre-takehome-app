# app_v3.py (or app_v4.py)
from flask import Flask, request
import sqlite3
import datetime
import os

# --- NEW: Import Prometheus Client ---
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import time
# --- END NEW ---

DATABASE = 'access_log.db'

app = Flask(__name__)

# --- NEW: Define Prometheus Metrics ---
# Example 1: Counter for total requests
REQUEST_COUNT = Counter('my_web_app_requests_total', 'Total Requests', ['method', 'endpoint', 'status'])

# Example 2: Histogram for request duration
REQUEST_DURATION = Histogram('my_web_app_request_duration_seconds', 'Request Duration in seconds', ['method', 'endpoint'])
# --- END NEW ---

def init_db():
    """Initializes the SQLite database, creating the table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            remote_addr TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database '{DATABASE}' initialized.")

def log_access(remote_addr):
    """Logs an access event to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO log (timestamp, remote_addr) VALUES (?, ?)',
                (datetime.datetime.now().isoformat(), remote_addr))
    conn.commit()
    conn.close()

# --- NEW: Add a /metrics endpoint ---
@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY)
# --- END NEW ---

@app.route('/')
def log_and_serve():
    """Route that logs the access, measures duration, and returns a response."""
    start_time = time.time() # Record start time

    # Get the client's IP address using request.remote_addr
    client_ip = request.remote_addr
    log_access(client_ip)

    # Calculate duration
    duration = time.time() - start_time

    # --- NEW: Update Prometheus Metrics ---
    REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint or 'unknown', status='200').inc()
    REQUEST_DURATION.labels(method=request.method, endpoint=request.endpoint or 'unknown').observe(duration)
    # --- END NEW ---

    return "Access logged successfully!"

if __name__ == '__main__':
    # Initialize the database when the script is run directly
    init_db()
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000)
