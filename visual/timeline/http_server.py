import os
import sys
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from functools import partial
import mimetypes

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

TIMELINE_HTML = os.path.join(os.path.dirname(__file__), 'neural_timeline.html')
PORT = 8081

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/neural_timeline.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(TIMELINE_HTML, 'rb') as f:
                self.wfile.write(f.read())
        else:
            # Serve static files with correct MIME type
            file_path = os.path.join(os.path.dirname(__file__), self.path.lstrip('/'))
            if os.path.isfile(file_path):
                mime, _ = mimetypes.guess_type(file_path)
                self.send_response(200)
                self.send_header('Content-type', mime or 'application/octet-stream')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, 'File Not Found')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

# Auto-reload support (dev mode)
def start_server_with_reload(port=PORT, dev_mode=False):
    def restart_server():
        print('File change detected. Restarting server...')
        os.execv(sys.executable, [sys.executable] + sys.argv)

    if dev_mode and WATCHDOG_AVAILABLE:
        class ReloadHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                if event.src_path.endswith('.html') or event.src_path.endswith('.js') or event.src_path.endswith('.css'):
                    restart_server()
        observer = Observer()
        observer.schedule(ReloadHandler(), os.path.dirname(__file__), recursive=True)
        observer.start()
        print('Auto-reload enabled (watchdog)')

    server = ThreadedHTTPServer(('0.0.0.0', port), CORSRequestHandler)
    print(f"Serving neural_timeline.html at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down server...')
    finally:
        if dev_mode and WATCHDOG_AVAILABLE:
            observer.stop()
            observer.join()

if __name__ == '__main__':
    dev_mode = '--dev' in sys.argv
    start_server_with_reload(PORT, dev_mode=dev_mode) 