## Flask App which serves the WebAssembly frontend for the chat
## client. Experimental

from pathlib import Path

from flask import Flask, send_from_directory, abort, Response
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(root: str | Path) -> Flask:
    if not root.exists():
        raise RuntimeError(f"Static root does not exist: {root}")


    app = Flask(__name__, static_folder=None)

    root = Path(root).resolve()

    #app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    @app.after_request
    def add_headers(response: Response) -> Response:
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_files(path: str):
        target = (root / path).resolve()

        # For emergencies if it somehow gets misconfigured
        if str(target) == "/" or str(target) == "":
            raise RuntimeError("Do not serve the root directory!")

        # Block directory traversal
        if not str(target).startswith(str(root)):
            abort(403)

        if target.is_dir():
            index = target / "App.html"
            if index.exists():
                return send_from_directory(target, "App.html")
            abort(404)

        if target.exists():
            return send_from_directory(target.parent, target.name)

        abort(404)

    return app

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    ROOT = (BASE_DIR / "../app/Build/wasm").resolve()

    HOST = "0.0.0.0"
    PORT = 4999

    app = create_app(ROOT)
    app.run(host=HOST, port=PORT)