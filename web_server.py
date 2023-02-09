import socket
from typing import Any
from application import application

HOST = ""
PORT = 8000
MAX_SIZE = 1024
CRLF = "\r\n"

def setup_socket(sock: socket.socket) -> None:
    """Setup socket"""
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)

def parse_request(request: str) -> list[str]:
    """Parse HTTP request
    
    Returns method, path and protocol
    """
    return request.split()

def format_header_key(key: str) -> str:
    return "HTTP_" + key.upper().replace("-", "_").replace(" ", "_")

def parse_header(header: str):
    """Parses HTTP header"""
    k, v = header.split(":", maxsplit=1)
    return (format_header_key(k), v.strip())

def parse_http(http: str) -> dict[str, Any]:
    """Parses raw HTTP request
    
    Example:
        `Connected by: ('127.0.0.1', 33906)\r\n`
        `GET / HTTP/1.1\r\n`
        `Host: localhost:8000\r\n`
        `User-Agent: curl/7.81.0\r\n`
        `Accept: */*`
    """
    request, *headers = http.split(CRLF)
    method, path, protocol = parse_request(request)
    headers = dict(
        parse_header(header) for header in headers
    )

    return {
        "PATH_INFO": path,
        "REQUEST_METHOD": method,
        "SERVER_PROTOCOL": protocol,
        **headers
    }

with socket.socket() as sock:
    setup_socket(sock)

    while True:
        conn, addr = sock.accept()
        with conn:
            print(f"Connected by: {addr}")
            http_request = conn.recv(MAX_SIZE).decode("utf-8").strip()
            environ = parse_http(http_request)

            def start_response(status, headers):
                conn.sendall(f"HTTP/1.1 {status}{CRLF}".encode("utf-8"))
                for (key, value) in headers:
                    conn.sendall(f"{key}: {value}{CRLF}".encode("utf-8"))
                conn.sendall(CRLF.encode("utf-8"))

            response_chunks = application(environ, start_response)

            for chunk in response_chunks:
                conn.sendall(chunk)