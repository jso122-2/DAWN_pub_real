#!/usr/bin/env python3
"""
KAN-Cairrn Standalone Server

Standalone server script that can be run directly without relative import issues.
"""

import sys
import os
import uvicorn
from pathlib import Path

# Add parent directory to Python path to enable absolute imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Now we can import using absolute paths
try:
    from cairrn_kan.interfaces.spline_api import SplineAPIServer
    from cairrn_kan.models import KANTopology, NavigationResult
    from cairrn_kan.core.kan_topology import KANTopologyManager
    from cairrn_kan.core.spline_neurons import SplineNeuronManager
    from cairrn_kan.cursor.function_navigator import FunctionNavigator
    from cairrn_kan.cursor.interpretability import SplineInterpreter
    
    print("✅ All imports successful")
    IMPORTS_OK = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    IMPORTS_OK = False


def create_app():
    """Create and configure the FastAPI app"""
    
    if not IMPORTS_OK:
        # Create minimal fallback app
        from fastapi import FastAPI
        app = FastAPI(title="KAN-Cairrn API (Fallback Mode)")
        
        @app.get("/")
        async def root():
            return {"status": "fallback_mode", "message": "KAN-Cairrn system not fully available"}
        
        @app.get("/health")
        async def health():
            return {"status": "limited", "imports_available": False}
        
        return app
    
    # Create full KAN-Cairrn system
    try:
        # Initialize components
        spline_manager = SplineNeuronManager()
        topology_manager = KANTopologyManager()
        kan_topology = topology_manager.create_topology()
        function_navigator = FunctionNavigator(kan_topology)
        spline_interpreter = SplineInterpreter()
        
        # Create API server
        api_server = SplineAPIServer(
            kan_topology=kan_topology,
            function_navigator=function_navigator,
            spline_interpreter=spline_interpreter
        )
        
        app = api_server.get_app()
        
        # Add custom endpoints
        @app.get("/")
        async def root():
            return {
                "name": "KAN-Cairrn Spline API",
                "version": "1.0.0",
                "status": "active",
                "endpoints": {
                    "neurons": "/kan/neurons",
                    "navigation": "/cursor/navigate-splines",
                    "topology": "/kan/topology",
                    "health": "/health",
                    "docs": "/docs"
                }
            }
        
        print("✅ KAN-Cairrn server initialized successfully")
        return app
        
    except Exception as e:
        print(f"❌ Failed to initialize KAN-Cairrn system: {e}")
        
        # Fallback app
        from fastapi import FastAPI
        app = FastAPI(title="KAN-Cairrn API (Error Mode)")
        
        @app.get("/")
        async def root():
            return {"status": "error", "message": f"Initialization failed: {str(e)}"}
        
        return app


# Create the app instance
app = create_app()


def main():
    """Main server entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="KAN-Cairrn Spline API Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host address")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--log-level", default="info", help="Log level")
    
    args = parser.parse_args()
    
    print(f"🚀 Starting KAN-Cairrn server on {args.host}:{args.port}")
    print(f"📖 API documentation available at http://{args.host}:{args.port}/docs")
    
    uvicorn.run(
        "server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level,
        reload_dirs=[str(current_dir)] if args.reload else None
    )


if __name__ == "__main__":
    main() 