import os
import celery.states as states

from functools import wraps
from app.scraper.schema import UserSchema
from app.scraper.service import Service
from app.services.authentication.auth import Auth
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


@app.route(PREFIX + "/login", methods=["POST"])
def login():
    try:
        data = json.loads(request.data)
        if (
            os.environ.get("APP_EMAIL") != data["email"]
            or os.environ.get("APP_PASSWORD") != data["password"]
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


@app.route(PREFIX + "/users/<email>", methods=["GET"])
def user(email):
    return json_response(Service().find_all_users(email), 200, "User found")


@app.route(PREFIX + "/users/<email>", methods=["DELETE"])
def delete(email):
    if Service().delete_user_for(email):
        return json_response({}, 200,"Deleted seccessfully")
    else:
        return json_response({}, 404, "User not found")


@app.route(PREFIX + "/users", methods=["POST"])
def create():
    try:
        user_repo = UserSchema().load(json.loads(request.data))

        if user_repo.errors:
            return json_response({"error": user_repo.errors}, 422, "Unprocessable entity")

        new_user = Service().create_user(user_repo)
        return json_response(new_user, 200, "User created")
    except Exception as error:
        return json_response({"error": str(error)}, 500, "Internal Server Error")


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
            Service().delete_all_evidences()

        task = celery.send_task(
            "tasks.investigate",
            args=[],
            kwargs={
                "urls_list": tuple(data["urls"]),
                "step": data["step"],
                "total_steps": data["totalsteps"],
                "keywords": tuple(data["keywords"]),
                "parent": data["parent"],
            },
        )

        with open(os.environ.get("TASK_PATH"), "w") as f:
            f.write(task.id)

        return json_response({"worker_id": task.id}, 200, "Task started")
    except Exception as e:
        return json_response({"error": str(e)}, 500, "Internal Server Error")


@app.route(PREFIX + "/evidences", methods=["GET"])
@auth_decorator
def get_evidences():
    limit = request.args.get("limit", default=10)
    page = request.args.get("page", default=1)
    return json_response(Service().get_evidences(limit, page), 200, "Evidences found")


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
    return json_response(Service().get_evidences_map(uuid, limit, page), 200, "Map found")


@app.route(PREFIX + "/map", methods=["GET"])
@auth_decorator
def get_evidences_map_first():
    limit = request.args.get("limit", default=10)
    page = request.args.get("page", default=1)
    return json_response(Service().get_evidences_map(None, limit, page), 200, "Map found")


@app.route(PREFIX + "/health")
def health_check():
    return json_response({}, 200, "OK")


@app.route(PREFIX + "/")
@auth_decorator
def index():
    return json_response({"body": "Not your lucky day!"}, 200, "Not your lucky day!")


def json_response(payload, status=200, message="OK"):
    body = {
        "status_code": status,
        "message":message, 
        "data": payload
    }
    return (json.dumps(body), status, {"content-type": "application/json"})


if __name__ == "__main__":
    app.run()
