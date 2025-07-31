import uvicorn
import asyncio
import sys
from dotenv import load_dotenv

from database_models.models import init_db

def main():
    """Main entry point for running the application."""
    load_dotenv()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "initdb":
            print("Initializing database...")
            asyncio.run(init_db())
            print("Database initialization complete.")
            return
        elif command == "forfeit_worker":
            print("Starting forfeit worker...")
            # In a real app, you would import and run your worker loop here.
            # e.g., from bot.workers import run_forfeit_check; asyncio.run(run_forfeit_check())
            print("Worker functionality to be implemented.")
            return

    # Default action: run the web server
    print("Starting FastAPI web server...")
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True # Set to False in production
    )

if __name__ == "__main__":
    main()