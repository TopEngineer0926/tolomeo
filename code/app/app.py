from code.app.scraper.schema import UserSchema
from flask import Flask, json, g, request
from pymongo import MongoClient, errors
from code.app.scraper.service import Service
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/users/<email>", methods=["GET"])
def user(email):
  return json_response(Service().find_all_users(email))

@app.route("/users/<email>", methods=["DELETE"])
def delete(email):
  if Service().delete_user_for(email):
    return json_response({})
  else:
    return json_response({'error': 'User not found'}, 404)

@app.route("/users", methods=["POST"])
def create():
  try: 
    user_repo = UserSchema().load(json.loads(request.data))

    if user_repo.errors:
      return json_response({'error': user_repo.errors}, 422)

    new_user = Service().create_user(user_repo)
    return json_response(new_user)
  except Exception as error:
    return str(error)

@app.route('/crawl')
def crawl():
    return 'started crawling\n'

@app.route('/')
def index():
    return 'Hello World!'


def json_response(payload, status=200):
  return (json.dumps(payload), status, {'content-type': 'application/json'})


if __name__ == "__main__":
  app.run()
