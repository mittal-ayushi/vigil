FROM python:3.11-slim

# strace + build-essential (gcc AND the libc headers like stdio.h) + bash (target for scanned scripts)
RUN apt-get update && apt-get install -y --no-install-recommends \
    strace \
    build-essential \
    bash \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN gcc -o main main.c -Wall -Wextra \
    && chmod +x main \
    && pip install --no-cache-dir flask flask-cors gunicorn

# Render/Railway/Fly.io all inject PORT; default to 8080 for local `docker run`.
ENV PORT=8080
EXPOSE 8080

# strace needs ptrace permissions. Most platforms grant this to containers
# by default; on plain Docker you may need: docker run --cap-add=SYS_PTRACE
# One worker, generous timeout: scans are short-lived but can take up to ~2 minutes.
CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:${PORT} --timeout 200 server:app"]
