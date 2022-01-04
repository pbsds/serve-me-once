from typing import Union
import http.server
import threading
import random
import time


def gen_random_port() -> int:
    return random.randrange(4000, 65535)

def serve_once(
        data      : Union[str, bytes],
        host      : str               = "",
        port      : int               = 8080,
        mime_type : str               = "text/html",
        timeout   : float             = 0,
        ):
    """
    Serves the content in `data` over HTTP once.
    Use `timeout` to decide how long you bare to wait.
    A daemonized thread will sleep for the whole timeout.
    """
    assert timeout >= 0
    if isinstance(data, str):
        data = data.encode()

    class HTTPHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", mime_type)
            self.end_headers()

            self.wfile.write(data)
            self.wfile.flush()

            self.server.shutdown() # blocking

    with http.server.ThreadingHTTPServer((host, port), HTTPHandler) as httpd:
        running = True
        def timeout_thread():
            time.sleep(timeout)
            if running:
                print("Serve timeout")
                httpd.shutdown()

        if timeout:
            threading.Thread(target=timeout_thread, daemon=True).start()

        print(f"Serving at http://{host or 'localhost'}:{port}/")
        httpd.serve_forever(poll_interval=0.5) # blocking

        running = False

    print("Serving stopped")

def serve_once_in_background(
        data      : Union[str, bytes],
        host      : str               = "",
        port      : int               = 8080,
        mime_type : str               = "text/html",
        timeout   : float             = 0,
        ) -> str:
    threading.Thread(
        target = serve_once,
        daemon = True,
        kwargs = dict(
            data      = data,
            host      = host,
            port      = port,
            mime_type = mime_type,
            timeout   = timeout,
        ),
    ).start()
    return f"http://{host or 'localhost'}:{port}/"
