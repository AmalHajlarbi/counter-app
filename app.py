import os
import socket
from flask import Flask
import redis

app = Flask(__name__)

# Connexion à Redis via le nom DNS du service
db = redis.Redis(
    host=os.getenv("REDIS_HOST", "db-service"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)

@app.route("/")
def index():
    try:
        hits = db.incr("hits")
    except redis.exceptions.ConnectionError:
        return "Erreur : impossible de joindre Redis (db-service).", 503
    container_id = socket.gethostname()  # = ID court du conteneur
    return f"Bonjour ! Cette page a été vue {hits} fois. Je suis le conteneur {container_id}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
