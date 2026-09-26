"""WibDroid Tools local web application."""
from flask import Flask, render_template
from api.routes import api


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["JSON_SORT_KEYS"] = False
    app.register_blueprint(api, url_prefix="/api")

    @app.get("/")
    def index():
        return render_template("index.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8765, debug=False)
