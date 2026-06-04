import json
import re


class Response:
    def __init__(self, body, status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or []


class Request:
    def __init__(self, scope, receive):
        self.scope = scope
        self.receive = receive
        self.method = scope["method"]
        self.path = scope["path"]

    async def body(self):
        chunks = []
        more = True
        while more:
            event = await self.receive()
            chunks.append(event.get("body", b""))
            more = event.get("more_body", False)
        return b"".join(chunks)

    async def json(self):
        raw = await self.body()
        if not raw:
            return None
        return json.loads(raw)


SWAGGER_UI_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} - API docs</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function () {{
      window.ui = SwaggerUIBundle({{
        url: "/openapi.json",
        dom_id: "#swagger-ui"
      }});
    }};
  </script>
</body>
</html>
"""


class Bamboo:
    def __init__(self, title="Bamboo", version="0.1.0"):
        self.title = title
        self.version = version
        self.routes = []

    def route(self, method, path):
        pattern = self.compile_path(path)
        def decorator(func):
            self.routes.append((method.upper(), path, pattern, func))
            return func
        return decorator

    def get(self, path):
        return self.route("GET", path)

    def post(self, path):
        return self.route("POST", path)

    def put(self, path):
        return self.route("PUT", path)

    def delete(self, path):
        return self.route("DELETE", path)

    def compile_path(self, path):
        segments = [s for s in path.split("/") if s != ""]
        regex_parts = []
        for segment in segments:
            if segment.startswith("{") and segment.endswith("}"):
                name = segment[1:-1]
                regex_parts.append(r"(?P<%s>[^/]+)" % name)
            else:
                regex_parts.append(re.escape(segment))
        if regex_parts:
            regex = "^/" + "/".join(regex_parts) + "/?$"
        else:
            regex = "^/?$"
        return re.compile(regex)

    def openapi(self):
        paths = {}
        for method, path, pattern, handler in self.routes:
            param_names = re.findall(r"{([^}]+)}", path)
            parameters = [
                {
                    "name": name,
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
                for name in param_names
            ]
            doc = (handler.__doc__ or "").strip()
            summary = doc.splitlines()[0] if doc else handler.__name__
            operation = {
                "summary": summary,
                "responses": {"200": {"description": "Successful Response"}},
            }
            if parameters:
                operation["parameters"] = parameters
            paths.setdefault(path, {})[method.lower()] = operation
        return {
            "openapi": "3.0.0",
            "info": {"title": self.title, "version": self.version},
            "paths": paths,
        }

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        request = Request(scope, receive)
        method = request.method
        path = request.path

        if method == "GET" and path == "/openapi.json":
            await self.send_json(send, self.openapi())
            return

        if method == "GET" and path == "/docs":
            await self.send_html(send, SWAGGER_UI_HTML.format(title=self.title))
            return

        for route_method, route_path, pattern, handler in self.routes:
            if route_method != method:
                continue
            match = pattern.match(path)
            if match:
                params = match.groupdict()
                try:
                    result = await handler(request, **params)
                    if isinstance(result, Response):
                        await self.send_response(send, result)
                    else:
                        await self.send_json(send, result)
                except Exception:
                    await self.send_json(send, {"error": "internal server error"}, 500)
                return

        await self.send_json(send, {"error": "not found"}, 404)

    async def send_json(self, send, data, status=200):
        body = json.dumps(data).encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"application/json; charset=utf-8"),
                (b"content-length", str(len(body)).encode()),
            ],
        })
        await send({"type": "http.response.body", "body": body})

    async def send_html(self, send, html, status=200):
        body = html.encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", b"text/html; charset=utf-8"),
                (b"content-length", str(len(body)).encode()),
            ],
        })
        await send({"type": "http.response.body", "body": body})

    async def send_response(self, send, response):
        body = json.dumps(response.body).encode("utf-8")
        headers = [
            (b"content-type", b"application/json; charset=utf-8"),
            (b"content-length", str(len(body)).encode()),
        ]
        headers.extend(response.headers)
        await send({
            "type": "http.response.start",
            "status": response.status,
            "headers": headers,
        })
        await send({"type": "http.response.body", "body": body})
