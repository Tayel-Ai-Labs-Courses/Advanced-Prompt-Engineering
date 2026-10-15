"""
The web server: the only thing the browser talks to.

Two endpoints, and that is the whole API surface:
    GET  /          -> the chat page
    POST /chat      -> {session_id, message} in, {reply, chips, debug} out

Python's standard library only, so this runs with `python3 app.py` on any
machine with Python installed -- no pip, no virtualenv, nothing to break.
"""

import json
import os
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import dialog

HOST = "127.0.0.1"
PORT = 8000
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Conversation memory, in RAM: session_id -> session dict.
# This is why the bot remembers the pizza type while it asks for the size.
# Restarting the server forgets every open conversation, which is fine here;
# a real product would keep this in Redis.
SESSIONS = {}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send_file("index.html", "text/html; charset=utf-8")
        if self.path == "/health":
            return self._send_json({"ok": True, "sessions": len(SESSIONS)})
        self.send_error(404)

    def do_POST(self):
        if self.path != "/chat":
            return self.send_error(404)

        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length) or "{}")
        except json.JSONDecodeError:
            return self._send_json({"error": "bad json"}, status=400)

        session_id = payload.get("session_id") or str(uuid.uuid4())
        message = (payload.get("message") or "").strip()

        session = SESSIONS.setdefault(session_id, dialog.new_session())

        if not message:
            # An empty message means "the page just opened": say hello.
            reply = dialog.greeting()
        else:
            reply = dialog.handle(session, message)

        return self._send_json({
            "session_id": session_id,
            "reply": reply["text"],
            "chips": reply.get("chips", []),
            "debug": reply.get("debug", {}),
        })

    # ----------------------------------------------------------- helpers

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, name, content_type):
        path = os.path.join(STATIC_DIR, name)
        if not os.path.isfile(path):
            return self.send_error(404)
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Quieter console: one line per chat turn instead of per asset.
        if "chat" in (args[0] if args else ""):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    print(f"🍕 Pizza bot running at http://{HOST}:{PORT}  (Ctrl+C to stop)")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
