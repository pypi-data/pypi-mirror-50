# Standard Library
from datetime import datetime
from uuid import uuid4

# 3rd Party
from flask import Blueprint, current_app, g, request

bp = Blueprint("metrics", __name__)  # pylint: disable=invalid-name


def init_app(app):
    def start_timer():
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        g.logger = current_app.logger.bind(request_id=request_id)
        g.request_id = request_id
        g.start = datetime.now()

    app.before_request(start_timer)

    def log_request(response):
        if request.path == "/favicon.ico":
            return response

        now = datetime.now()

        if hasattr(g, "start"):
            duration = int(round((now - g.start).microseconds / 1000, 2))
        else:
            duration = -1

        user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        host = request.host.split(":", 1)[0]

        log_params = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration": duration,
            "ip": user_ip,
            "host": host,
        }

        request_id = getattr(g, "request_id", None)

        if request_id:
            log_params["request_id"] = request_id

        if response.status_code < 400:
            current_app.logger.info("Request succeeded", **log_params)
        elif response.status_code < 500:
            current_app.logger.info("Bad Request", **log_params)
        else:
            current_app.logger.error("Internal Server Error", **log_params)

        return response

    app.after_request(log_request)
