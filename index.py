from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import jwt

# Custom modules and packages
import appconfig

app = Flask(__name__)
app.config.from_object("appconfig.DefaultConfig")
CORS(app)

# @TODO
# Remove this when all data are stored in data exchange layer
temp_data = json.load(open('service.json'))


@app.route(appconfig.API_PREFIX + "/login/", methods=['POST'])
def login():
    retResp = {"success": False, "message": ""}
    httpCode = 400

    if not request.is_json:
        retResp["message"] = "Invalid request body type, expected JSON"
        return jsonify(retResp), httpCode

    incomData = request.get_json()
    username = incomData.get("username", "")
    password = incomData.get("password", "")

    try:
        resp = requests.get(appconfig.LOGIN_API, auth=(username, password))
    except (requests.ConnectionError, requests.ConnectTimeout) as e:
        retResp["message"] = e.__str__()
        httpCode = 500
    else:
        httpCode = resp.status_code

        if resp.status_code == 200:
            respData = resp.json()
            accessToken = respData.get("accessToken", "")
            webAccessToken = jwt.encode(
                    {"key": accessToken},
                    appconfig.SECRET,
                    algorithm='HS256').decode()
            retResp = {
                    "access_token": webAccessToken,
                    "userId": respData.get("userId", "")}
        else:
            retResp["message"] = getRtrnMsg(resp.status_code)
    finally:
        return jsonify(retResp), httpCode


@app.route(appconfig.API_PREFIX + "/dataCollections/")
def getDataBuckets():
    query = {"open": True}
    retResp = {"success": False, "message": ""}
    httpCode = 400

    try:
        resp = requests.get(appconfig.COLLECTION_API, params=query)
    except (requests.ConnectionError, requests.ConnectTimeout) as e:
        retResp["message"] = e.__str__()
        httpCode = 500
    else:
        httpCode = resp.status_code

        if resp.status_code == 200:
            retResp = resp.json()
        else:
            retResp["message"] = getRtrnMsg(resp.status_code)
    finally:
        return jsonify(retResp), httpCode


@app.route(appconfig.API_PREFIX + "/cityServices/")
def getCityServices():
    return jsonify(temp_data), 200


def getRtrnMsg(code):
    return {
            400: "Bad request",
            401: "Wrong username or password",
            500: "external service error",
            200: ""}.get(code, "Unknown external service error: " + str(code))
