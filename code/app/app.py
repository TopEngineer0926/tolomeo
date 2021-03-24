import os

from functools import wraps
from app.scraper.schema import UserSchema
from app.scraper.service import Service
from app.services.authentication.auth import Auth
from flask import Flask, g, json, request
from flask_cors import CORS

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
            return json_response("Not Authenticated", 401)
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
            return json_response("Unauthorized", 403)

        return json_response(
            {"status": "success", "token": Auth().generate_token_for_user_id(1)}
        )
    except Exception as exeption:
        return json_response("Internal server error", 500)


@app.route(PREFIX + "/logout", methods=["POST"])
@auth_decorator
def logout():
    return json_response("Successfully logged out", 200)


@app.route(PREFIX + "/users/<email>", methods=["GET"])
def user(email):
    return json_response(Service().find_all_users(email))


@app.route(PREFIX + "/users/<email>", methods=["DELETE"])
def delete(email):
    if Service().delete_user_for(email):
        return json_response({})
    else:
        return json_response({"error": "User not found"}, 404)


@app.route(PREFIX + "/users", methods=["POST"])
def create():
    try:
        user_repo = UserSchema().load(json.loads(request.data))

        if user_repo.errors:
            return json_response({"error": user_repo.errors}, 422)

        new_user = Service().create_user(user_repo)
        return json_response(new_user)
    except Exception as error:
        return str(error)


@app.route(PREFIX + "/crawl", methods=["POST"])
@auth_decorator
def crawl():
    return json_response("Scraper successfully started", 200)


@app.route(PREFIX + "/evidences", methods=["GET"])
@auth_decorator
def get_evidences():
    limit = request.args.get("limit", default=10)
    page = request.args.get("page", default=1)
    return json_response(Service().get_evidences(limit, page))


@app.route(PREFIX + "/map/<uuid>", methods=["GET"])
@auth_decorator
def get_evidences_map(uuid):
    limit = request.args.get("limit", default=10)
    page = request.args.get("page", default=1)
    return json_response(Service().get_evidences_map(uuid, limit, page))


@app.route(PREFIX + "/map", methods=["GET"])
@auth_decorator
def get_evidences_map_first():
    limit = request.args.get("limit", default=10)
    page = request.args.get("page", default=1)
    return json_response(Service().get_evidences_map(None, limit, page))


@app.route(PREFIX + "/")
@auth_decorator
def index():
    return "Not your lucky day!"


def json_response(payload, status=200):
    return (json.dumps(payload), status, {"content-type": "application/json"})


if __name__ == "__main__":
    app.run()
