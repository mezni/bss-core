# run_dev.py
import subprocess
import sys
import time


def run_development_servers():
    print("🚀 Starting FastAPI backend and Streamlit frontend...")

    # Start FastAPI using uv
    fastapi_process = subprocess.Popen(
        [
            "uv",
            "run",
            "uvicorn",
            "src.main:app",
            "--reload",
            "--port",
            "8000",
        ]
    )

    # Start Streamlit using uv
    streamlit_process = subprocess.Popen(
        ["uv", "run", "streamlit", "run", "frontend/app.py"]
    )

    try:
        # Monitor processes and keep script alive
        while True:
            time.sleep(1)
            if (
                fastapi_process.poll() is not None
                or streamlit_process.poll() is not None
            ):
                print("⚠️ One of the servers stopped unexpectedly. Shutting down...")
                break
    except KeyboardInterrupt:
        print("\n🛑 Stopping development servers...")
        fastapi_process.terminate()
        streamlit_process.terminate()
        fastapi_process.wait()
        streamlit_process.wait()
        print("👋 All servers stopped successfully.")


if __name__ == "__main__":
    run_development_servers()
