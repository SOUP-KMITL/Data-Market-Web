# Example configuration
class DefaultConfig(object):
    DEBUG = True
    #  SERVER_NAME = "webservice:5000"


API_VER = "/v1"
#  API_PREFIX = "/api" + API_VER
API_PREFIX = "/web"

EXT_API_PORT = 8080
EXT_API_VER = "/v1"
EXT_API_GATEWAY = "http://api.smartcity.kmitl.io:" + str(EXT_API_PORT) + "/api" + EXT_API_VER

#  Production (public server) configuration
#  COLLECTION_API = "http://collection-service:" + str(EXT_API_PORT) + "/api" + EXT_API_VER + "/collections"

#  Development (local) configuration
COLLECTION_API = EXT_API_GATEWAY + "/collections"
