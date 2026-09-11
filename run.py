"""
run.py — Entry point for the Cyclone AI/ML System.

Quick start:
    python run.py              — Run full pipeline (data + train + summary)
    python run.py --quick      — Fast mode (fewer epochs, no hyperparameter tuning)
    python run.py --serve      — Run pipeline then start API server at :8000
    python run.py --data-only  — Only download and prepare data
    python run.py --api-only   — Start API server (assumes models already trained)
"""

import sys

def main():
    if "--api-only" in sys.argv:
        # Just start the API server
        import uvicorn
        print("Starting Cyclone AI/ML API server...")
        print("  Swagger UI: http://localhost:8000/docs")
        print("  Health:     http://localhost:8000/health")
        uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=False)
    else:
        # Run the full pipeline
        from src.pipeline import main as pipeline_main
        pipeline_main()


if __name__ == "__main__":
    main()
