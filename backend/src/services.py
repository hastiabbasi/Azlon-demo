#./backend/src/services.py
import traceback
import asyncio
import time
from src.client import client
from src.functions.functions import (
    generate_code, run_locally, validate_output, pre_flight_run
)
from src.workflows.workflow import AutonomousCodingWorkflow

async def main():
    try:
        await client.start_service(
            workflows=[AutonomousCodingWorkflow],
            functions=[generate_code, run_locally, validate_output, pre_flight_run],
        )
    except Exception as e:
        print(f"Error starting service: traceback: {traceback.format_exc()}")
        print(f"Error starting service: {e}")
        raise

def run_services():
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Service failed: {e}")
    # Keep the process alive for inspection
    while True:
        time.sleep(1)

if __name__ == "__main__":
    run_services()

    # For dev mount containers in docker compose, set restack env variables to local, and uncomment this:
    # import webbrowser
    # from pathlib import Path

    # from watchfiles import run_process
    # def watch_services() -> None:
    #     watch_path = Path.cwd()
    #     logging.info("Watching %s and its subdirectories for changes...", watch_path)
    #     webbrowser.open("http://localhost:5233")
    #     webbrowser.open("http://localhost:8080")
    #     run_process(watch_path, recursive=True, target=run_services)

