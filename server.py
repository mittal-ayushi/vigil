import os, json, shutil, tempfile, subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
binarypath = os.path.abspath(os.environ.get("vigilbinary", "./main"))

@app.route("/scan", methods=["POST"])
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

        result = subprocess.run(args, cwd=work_dir)

        entries = []
        alert_file = os.path.join(work_dir, "alerts.jsonl")

        if os.path.exists(alert_file):
            with open(alert_file) as f:
                for line in f:
                    try:
                        entries.append(json.loads(line))
                    except:
                        pass

        return jsonify(status=result.returncode, entries=entries)

    finally:
        shutil.rmtree(work_dir, ignore_errors=True)

if __name__ == "__main__":
    app.run(port=8080)