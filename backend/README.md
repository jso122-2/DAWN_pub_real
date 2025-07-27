# DAWN Backend

Core backend components for the DAWN consciousness engine.

## Structure

```
backend/
├── api/              # FastAPI endpoints and WebSocket handlers
├── core/             # Core system components
├── monitoring/       # System monitoring tools
├── visualization/    # Debug visualization tools
├── state/           # System state storage
└── logs/            # System logs
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Server

```bash
uvicorn api.dawn_api:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all functions
- Add tests for new features

## Monitoring

The system includes several monitoring tools:
- Wiring Monitor: System connection health
- Butler Diagnostics: System diagnostics
- Helix Bridge: System bridge monitoring

## Visualization

Debug visualization tools are available in the visualization package:
- Tracer Routes: Visualize system communication paths
- State Visualization: Monitor system state changes 