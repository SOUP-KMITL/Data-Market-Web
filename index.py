from flask import Flask, request, render_template, url_for, redirect, abort, jsonify
import requests
import json

# Custom modules and packages
import appconfig

app = Flask(__name__)
app.config.from_object("appconfig.DefaultConfig")

temp_data = json.load(open('service.json'))


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
        if resp.status_code != 200:
            retResp["message"] = "external service error: " + str(resp.status_code)
        else:
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
