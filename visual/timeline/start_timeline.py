import argparse
import asyncio
import sys
from visual.timeline import timeline_server, event_collector

def main():
    parser = argparse.ArgumentParser(description="Start DAWN Neural Timeline WebSocket server.")
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the server (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind the server (default: 8080)')
    args = parser.parse_args()

    # Start HTTP and WebSocket server
    print(f"[Timeline] Starting server on {args.host}:{args.port}")
    # Use the TimelineWebSocketServer from timeline_server
    server = timeline_server.TimelineWebSocketServer()

    # Start event collector (hooks are set up on import)
    # The event_broadcaster will pull from event_collector.get_event_stream
    loop = asyncio.get_event_loop()
    loop.create_task(timeline_server.event_broadcaster(server))
    loop.run_until_complete(timeline_server.start_ws_server(server, port=args.port))

if __name__ == '__main__':
    main() 