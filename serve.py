import http.server
import socketserver
import os

PORT = 8090
# Serve the dist/ build directory
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
os.chdir(DIRECTORY)


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass  # quiet


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    # Allow address reuse so quick restarts don't fail with "address in use"
    allow_reuse_address = True


if __name__ == "__main__":
    with ThreadingHTTPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving {DIRECTORY} at http://127.0.0.1:{PORT} (threaded)")
        httpd.serve_forever()
