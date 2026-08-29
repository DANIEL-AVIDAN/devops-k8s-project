import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = "Hello from the Python microservice!"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))


def main():
    port = int(os.getenv("APP_PORT", "8000"))

    server = HTTPServer(("0.0.0.0", port), RequestHandler)

    print(f"Microservice is listening on port {port}", flush=True)

    server.serve_forever()


if __name__ == "__main__":
    main()