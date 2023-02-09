# Learning WSGI
I want to understand a little bit more how the Web Server Gateway Interface works, so why not implement the simplest possible web server + web app?

- `web_server` is a simple WSGI web server.

- `application` is a dummy WSGI-compliant application, meaning that one could plug it into other WSGI web servers.

Obs: heavily based on [Ryan Wilson-Perkin's work](https://github.com/ryanwilsonperkin/wsgi-tutorial)

## How to run
Start the web server
```shell
python web_server.py
```

Just call the endpoint somehow (browser, terminal, etc)
```shell
curl http://localhost:8000
```