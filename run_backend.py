"""Run this file directly with Python to restart the backend."""
import subprocess, sys, os, signal, time

# Kill anything on port 8000
try:
    result = subprocess.run(
        ['netstat', '-ano'],
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        if ':8000' in line and 'LISTENING' in line:
            pid = line.strip().split()[-1]
            subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
            print(f"Killed PID {pid} on port 8000")
            time.sleep(1)
except Exception as e:
    print(f"Kill step: {e}")

# Install Pillow
print("Installing Pillow...")
subprocess.run([sys.executable, '-m', 'pip', 'install', 'Pillow'], check=False)

# Start server
backend_dir = os.path.join(os.path.dirname(__file__), 'comfy-backend')
server_py = os.path.join(backend_dir, 'server.py')
print(f"\nStarting backend: {server_py}")
os.chdir(backend_dir)
os.execv(sys.executable, [sys.executable, server_py])
