import asyncio
import websockets
import json
import os
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.parse import urlparse, parse_qs
from .event_collector import get_event_stream

TIMELINE_HTML = os.path.join(os.path.dirname(__file__), 'neural_timeline.html')
WS_PATH = '/consciousness/timeline'
BUFFER_DURATION = 60 * 60  # 1 hour in seconds

class TimelineHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path.startswith('/neural_timeline.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(TIMELINE_HTML, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, 'File Not Found')

def start_http_server(port=8080):
    server = HTTPServer(('0.0.0.0', port), TimelineHTTPRequestHandler)
    print(f"Serving neural_timeline.html at http://localhost:{port}")
    server.serve_forever()

class TimelineWebSocketServer:
    def __init__(self):
        self.clients = set()
        self.event_buffer = []  # List of (timestamp, event)
        self.lock = asyncio.Lock()

    async def register(self, websocket, event_types):
        async with self.lock:
            self.clients.add((websocket, event_types))

    async def unregister(self, websocket):
        async with self.lock:
            self.clients = {(ws, types) for (ws, types) in self.clients if ws != websocket}

    async def broadcast(self, event):
        async with self.lock:
            # Remove disconnected clients
            disconnected = set()
            for ws, types in self.clients:
                if types and event['type'] not in types:
                    continue
                try:
                    await ws.send(json.dumps(event))
                except Exception:
                    disconnected.add(ws)
            for ws in disconnected:
                self.clients = {(w, t) for (w, t) in self.clients if w != ws}

    def buffer_event(self, event):
        now = time.time()
        self.event_buffer.append((now, event))
        # Remove events older than 1 hour
        cutoff = now - BUFFER_DURATION
        self.event_buffer = [(ts, ev) for (ts, ev) in self.event_buffer if ts >= cutoff]

    def get_recent_events(self, event_types=None):
        now = time.time()
        cutoff = now - BUFFER_DURATION
        events = [ev for (ts, ev) in self.event_buffer if ts >= cutoff]
        if event_types:
            events = [ev for ev in events if ev['type'] in event_types]
        return events

    async def handler(self, websocket, path):
        # Only accept connections on the correct path
        parsed = urlparse(path)
        if parsed.path != WS_PATH:
            await websocket.close()
            return
        # Parse event type filters
        query = parse_qs(parsed.query)
        types = query.get('types', [None])[0]
        event_types = set(types.split(',')) if types else None
        await self.register(websocket, event_types)
        print(f"[WS] Client connected: {websocket.remote_address} (types={event_types})")
        # Send buffered events
        for event in self.get_recent_events(event_types):
            try:
                await websocket.send(json.dumps(event))
            except Exception:
                pass
        try:
            async for _ in websocket:
                pass  # No incoming messages expected
        except Exception:
            pass
        finally:
            await self.unregister(websocket)
            print(f"[WS] Client disconnected: {websocket.remote_address}")

async def event_broadcaster(server: TimelineWebSocketServer):
    async for event in get_event_stream():
        server.buffer_event(event)
        await server.broadcast(event)

async def start_ws_server(server: TimelineWebSocketServer, port=8080):
    async with websockets.serve(server.handler, '0.0.0.0', port, subprotocols=None):
        print(f"WebSocket server running at ws://localhost:{port}{WS_PATH}")
        await asyncio.Future()  # run forever

def main():
    http_thread = Thread(target=start_http_server, args=(8080,), daemon=True)
    http_thread.start()
    server = TimelineWebSocketServer()
    loop = asyncio.get_event_loop()
    loop.create_task(event_broadcaster(server))
    loop.run_until_complete(start_ws_server(server, 8080))

if __name__ == '__main__':
    main() 