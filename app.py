from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from a tiny Python app running in Docker!")

    # מונע הדפסות ללוג בכל בקשה (אופציונלי)
    def log_message(self, format, *args):
        return


def main():
    server = HTTPServer(("0.0.0.0", 8000), RequestHandler)
    print("Server is running on port 8000...")
    server.serve_forever()


if __name__ == "__main__":
    main()