import os, json, shutil, tempfile, subprocess
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

HERE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=None)
CORS(app)

binarypath = os.path.abspath(os.environ.get("vigilbinary", os.path.join(HERE, "main")))

# Optional shared-secret auth. If VIGIL_TOKEN is set in the environment,
# every /scan request must include header "X-Vigil-Token: <that value>".
# Strongly recommended if this is ever reachable from the public internet,
# since /scan executes whatever script is uploaded to it.
VIGIL_TOKEN = os.environ.get("VIGIL_TOKEN", "")


def require_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if VIGIL_TOKEN:
            supplied = request.headers.get("X-Vigil-Token", "")
            if supplied != VIGIL_TOKEN:
                return jsonify(error="unauthorized"), 401
        return fn(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    return send_from_directory(HERE, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    if filename in ("script.js", "style.css"):
        return send_from_directory(HERE, filename)
    return jsonify(error="not found"), 404


@app.route("/scan", methods=["POST"])
@require_token
def scan():
    if "script" not in request.files:
        return jsonify(error="No script uploaded"), 400

    raw = request.files["script"].read(20481)
    if len(raw) > 20480:
        return jsonify(error="Script too big"), 400

    work_dir = tempfile.mkdtemp()
    script = os.path.join(work_dir, "script.sh")

    try:
        with open(script, "wb") as f:
            f.write(raw)

        args = [binarypath]
        if request.form.get("enforce", "true") == "true":
            args.append("-k")
        args += ["bash", script]

        result = subprocess.run(args, cwd=work_dir, timeout=180)

        entries = []
        alert_file = os.path.join(work_dir, "alerts.jsonl")

        if os.path.exists(alert_file):
            with open(alert_file) as f:
                for line in f:
                    try:
                        entries.append(json.loads(line))
                    except Exception:
                        pass

        return jsonify(status=result.returncode, entries=entries)

    except subprocess.TimeoutExpired:
        return jsonify(error="scan timed out"), 504

    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
