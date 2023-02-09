def process_request(path):
    return f"Hello from '{path}'!\r\n"

def application(environ, callback):
    path = environ["PATH_INFO"]
    response = process_request(path)
    content_length = len(response)

    callback(
        "200 OK",
        [
            ("Content-Length", str(content_length)),
            ("Content-Type", "text/html")
        ]
    )
    return [response.encode("utf-8")]