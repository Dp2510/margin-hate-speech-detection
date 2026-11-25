import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import joblib
from comment_analysis import analyse_comment

project = Path(__file__).resolve().parent
page = (project / "templates" / "comment_review.html").read_bytes()
models = joblib.load(project / "hate_speech_models.joblib")


class CommentPage(BaseHTTPRequestHandler):
    def reply(self, body, content_type, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass  # The user edited the draft and the browser canceled this response.

    def do_GET(self):
        if self.path == "/":
            self.reply(page, "text/html; charset=utf-8")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/analyse":
            return self.send_error(404)
        if self.headers.get_content_type() != "application/json":
            return self.send_error(415)
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 65536:
                return self.send_error(413)
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict) or not isinstance(data.get("text"), str):
                return self.send_error(400)
        except (ValueError, UnicodeError):
            return self.send_error(400)

        result = analyse_comment(data["text"], models)
        self.reply(json.dumps(result).encode(), "application/json")


if __name__ == "__main__":
    with ThreadingHTTPServer(("127.0.0.1", 5000), CommentPage) as server:
        print("Open http://127.0.0.1:5000 in your browser. Press Ctrl+C to stop.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
