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

temp_data = json.load(open('service.json'))


@app.route(appconfig.API_PREFIX + "/login/", methods=['POST'])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    retResp = {"status": "failed", "message": "", "data": None}
    httpCode = 400

    try:
        resp = requests.get(appconfig.LOGIN_API, auth=(username, password))
    except requests.ConnectionError:
        retResp["message"] = "couldn't connect to external service"
    except requests.ConnectTimeout:
        retResp["message"] = "connection to external service timeout"
    else:
        retResp["message"] = getRtrnMsg(resp.status_code)

        if resp.status_code == 200:
            retResp["status"] = "successful"
            retResp["data"] = {
                    "access_token": jwt.encode({
                        "rol": resp.json().get("role", "user"),
                        "key": resp.json().get("accessToken", "")},
                        appconfig.SECRET,
                        algorithm="HS256").decode(),
                    "userId": resp.json().get("userId", "")}
            httpCode = 200
    finally:
        return jsonify(retResp), httpCode


@app.route(appconfig.API_PREFIX + "/dataBuckets/")
def getDataBuckets():
    query = {"open": True}
    retResp = {"status": "failed", "message": "", "data": []}
    httpCode = 400

    try:
        resp = requests.get(appconfig.COLLECTION_API, params=query)
    except requests.ConnectionError:
        retResp["message"] = "couldn't connect to external service"
    except requests.ConnectTimeout:
        retResp["message"] = "connection to external service timeout"
    else:
        retResp["message"] = getRtrnMsg(resp.status_code)

        if resp.status_code == 200:
            retResp["status"] = "successful"
            retResp["data"] = resp.json()
            httpCode = 200
    finally:
        return jsonify(retResp), httpCode


@app.route(appconfig.API_PREFIX + "/cityServices/")
def getCityServices():
    return jsonify({
        "status": "successful",
        "message": "This is just a temporary data.",
        "data": temp_data}), 200


def getRtrnMsg(code):
    return {
            400: "Bad request",
            500: "external service error",
            200: ""}.get(code, "Unknown external service error: " + str(code))
