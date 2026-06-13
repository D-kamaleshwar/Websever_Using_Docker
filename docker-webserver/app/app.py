# app/app.py
from flask import Flask, jsonify
import os, datetime

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html><body style="font-family:sans-serif;padding:40px">
    <h1>Docker Web Server — Running!</h1>
    <p>Container ID: <code>{}</code></p>
    <p>Time: {}</p>
    <a href="/api/health">Check health API</a>
    </body></html>
    """.format(os.environ.get("HOSTNAME", "unknown"), datetime.datetime.now())

@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "container": os.environ.get("HOSTNAME", "unknown"),
        "timestamp": str(datetime.datetime.now())
    })

@app.route("/api/info")
def info():
    return jsonify({
        "app": "Docker Web Server Project",
        "version": "1.0.0",
        "python_version": os.sys.version
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)