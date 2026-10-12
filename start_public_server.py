import os
import subprocess
import re
import time
import sys

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"e:\Rotor"
BIN_CLOUDFLARED = os.path.join(BASE_DIR, "bin", "cloudflared.exe")

# 1. Start Flask app
print("Starting Flask app...")
flask_proc = subprocess.Popen(
    [sys.executable, os.path.join(BASE_DIR, "app.py")],
    cwd=BASE_DIR,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(3)

# 2. Start Cloudflare Tunnel
print("Starting Cloudflare Tunnel...")
cf_proc = subprocess.Popen(
    [BIN_CLOUDFLARED, "tunnel", "--url", "http://127.0.0.1:5000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

tunnel_url = None
start_t = time.time()

while time.time() - start_t < 30:
    line = cf_proc.stdout.readline()
    if not line:
        continue
    match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
    if match:
        tunnel_url = match.group(0)
        break

if tunnel_url:
    print("\n" + "="*60)
    print("PUBLIC LIVE TUNNEL ACTIVE!")
    print("Open on any Mobile / Laptop anywhere:")
    print(tunnel_url)
    print("="*60 + "\n")
    with open(os.path.join(BASE_DIR, "public_url.txt"), "w") as f:
        f.write(tunnel_url)
else:
    print("Failed to capture Cloudflare URL within 30 seconds.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    flask_proc.terminate()
    cf_proc.terminate()
