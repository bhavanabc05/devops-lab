from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@app.route("/")
def index():
    count = r.incr("visits")
    return jsonify({
        "message": "Hello from DevOps Lab!",
        "visits": count,
        "hostname": os.uname().nodename
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/reset", methods=["POST"])
def reset():
    r.set("visits", 0)
    return jsonify({"message": "reset done", "visits": 0})

@app.route("/stats")
def stats():
    visits = r.get("visits") or 0
    return jsonify({
        "visits": int(visits),
        "hostname": os.uname().nodename,
        "redis_host": REDIS_HOST
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
