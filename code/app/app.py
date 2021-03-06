import os
import celery.states as states
import uuid

from functools import wraps
from app.scraper.service import Service
from app.services.authentication.auth import Auth
from app.services.authentication.hmac import HmacAuth
from flask import Flask, g, json, request, send_file
from flask_cors import CORS
from app.worker import celery


app = Flask(__name__)
CORS(app)

PREFIX = "/api/v1"


def auth_decorator(function):
    @wraps(function)
    def auth_wrapper(*args, **kwargs):
        try:
            bearer_token = request.headers.get("Authorization")
            Auth().decode_auth_token(bearer_token.split(" ")[1])
        except Exception:
            return json_response({}, 401, "Not Authenticated")
        return function(*args, **kwargs)

    return auth_wrapper


def external_service_decorator(function):
    @wraps(function)
    def external_service_wrapper(*args, **kwargs):
        try:
            if False == HmacAuth().is_valid_hexdigest(
                request.args.get("k"), request.data.decode()
            ):
                return json_response({}, 403, "Forbidden")
        except Exception:
            return json_response({}, 500, "Internal Server Error")
        return function(*args, **kwargs)

    return external_service_wrapper


@app.route(PREFIX + "/login", methods=["POST"])
def login():
    try:
        data = json.loads(request.data)

        if not HmacAuth().is_valid_hexdigest(
            os.environ.get("APP_EMAIL"), data["email"]
        ) or not HmacAuth().is_valid_hexdigest(
            os.environ.get("APP_PASSWORD"), data["password"]
        ):
            return json_response({}, 401, "Unauthorized")

        return json_response(
            {"token": Auth().generate_token_for_user_id(1)}, message="success"
        )
    except Exception as exeption:
        return json_response({}, 500, "Internal server error")


@app.route(PREFIX + "/logout", methods=["POST"])
@auth_decorator
def logout():
    return json_response({}, 405, "Not implemented")


@app.route(PREFIX + "/evidences/telegram", methods=["POST"])
@external_service_decorator
def add_telegram_evidence():
    data = json.loads(request.data)
    evidence_uuid = str(uuid.uuid4())
    evidence = {
        "uuid": evidence_uuid,
        "parent": None,
        "keywords": ",".join(data["keywords"]),
        "source": "telegram",
        "step": 1,
        "total_steps": 1,
        "url": data["url"],
        "title": data["title"],
        "urls_found": data["urls_found"],
        "urls_queryable": data["urls_queryable"],
        "keywords_found": data["keywords_found"],
        "has_form": False,
        "has_input_password": False,
    }
    return json_response(Service().save_telegram_evidence(evidence), 202, "Accepted")


@app.route(PREFIX + "/tasks/check-status", methods=["GET"])
@auth_decorator
def check_task():
    if os.path.exists(os.environ.get("TASK_PATH")):
        with open(os.environ.get("TASK_PATH"), "r") as f:
            task_id = f.read()
            f.close()
            res = celery.AsyncResult(task_id)
            if res.state == states.PENDING:
                return json_response({}, 202, res.state)
            else:
                return json_response({}, 202, res.result)
    return json_response({}, 404, "No tasks pending")


@app.route(PREFIX + "/crawl", methods=["POST"])
@auth_decorator
def crawl():
    try:
        if os.path.exists(os.environ.get("TASK_PATH")):
            return json_response({}, 409, "Another task is not yet completed")

        data = json.loads(request.data)

        if None == data["parent"]:
            if os.path.exists(os.environ.get("EXPORT_PATH")):
                os.remove(os.environ.get("EXPORT_PATH"))
           # Service().delete_all_evidences()

        task = celery.send_task(
            "tasks.investigate",
            args=[],
            kwargs={
                "urls_list": tuple(data["urls"]),
                "step": 1,
                "total_steps": int(data["totalsteps"]),
                "keywords": tuple(data["keywords"]),
                "parent": data["parent"],
            },
        )

        with open(os.environ.get("TASK_PATH"), "w") as f:
            f.write(task.id)

        return json_response({}, 200, "Task started")
    except Exception as e:
        return json_response({"error": str(e)}, 500, "Internal Server Error")


@app.route(PREFIX + "/evidences", methods=["GET"])
@auth_decorator
def get_evidences():
    limit = request.args.get("limit", default=10)
    page = request.args.get("page", default=1)
    query_filter = request.args.get("query", default="")
    only_keywords_found = (
        request.args.get("only_keywords_found", default="false") == "true"
    )
    return json_response(
        Service().get_evidences(limit, page, query_filter, only_keywords_found),
        200,
        "Evidences found",
    )


@app.route(PREFIX + "/evidences/export", methods=["GET"])
@auth_decorator
def get_evidences_export():
    file = os.environ.get("EXPORT_PATH")
    if not os.path.isfile(file):
        return json_response({}, 404, "File not found")
    return send_file(
        file,
        mimetype="text/csv",
        attachment_filename="evidences.csv",
        as_attachment=True,
    )


@app.route(PREFIX + "/map/<uuid>", methods=["GET"])
@auth_decorator
def get_evidences_map(uuid):
    limit = request.args.get("limit", default=10)
    page = request.args.get("page", default=1)
    return json_response(
        Service().get_evidences_map(uuid, limit, page), 200, "Map found"
    )


@app.route(PREFIX + "/map", methods=["GET"])
@auth_decorator
def get_evidences_map_first():
    limit = request.args.get("limit", default=10)
    page = request.args.get("page", default=1)
    return json_response(
        Service().get_evidences_map(None, limit, page), 200, "Map found"
    )


@app.route(PREFIX + "/health")
def health_check():
    return json_response({}, 200, "OK")


@app.route(PREFIX + "/")
@auth_decorator
def index():
    return json_response({"body": "Not your lucky day!"}, 200, "Not your lucky day!")


def json_response(payload, status=200, message="OK"):
    body = {"status_code": status, "message": message, "data": payload}
    return (json.dumps(body), status, {"content-type": "application/json"})


if __name__ == "__main__":
    app.run()
