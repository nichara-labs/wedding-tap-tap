import socket
import threading
import time
from collections.abc import Generator
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pytest


# Module scope to speed this up
@pytest.fixture(scope="module")
def port() -> int:
    """Get an available port on the system."""
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def http_server(port: int) -> Generator[str]:
    """Returns the url of a http server listening on localhost."""

    # Run the server in a thread, so we can stop it after the fixture is destroyed
    server = HTTPServer(("localhost", port), SimpleHTTPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Wait a moment for server to start
    time.sleep(0.1)

    yield f"http://localhost:{port}"

    # Cleanup
    server.shutdown()
    server.server_close()
