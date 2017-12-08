# Example configuration
class DefaultConfig(object):
    DEBUG = True
    #  SERVER_NAME = "webservice:5000"


API_VER    = 1

EXT_API_PORT    = 8080
#  EXT_API_GATEWAY = "http://api.smartcity.kmitl.io:" + str(EXT_API_PORT) + "/api/v1"
EXT_API_GATEWAY = "http://203.154.59.55:" + str(EXT_API_PORT) + "/api/v1"

#  Production (public server) configuration
#  API_PREFIX     = "/web"
#  COLLECTION_API = "http://collection-service:" + str(EXT_API_PORT) + "/api/v1/collections"
#  LOGIN_API      = "http://user-service:" + str(EXT_API_PORT) + "/api/v1/users/login"

#  Development (local) configuration
API_PREFIX     = "/api/v" + str(API_VER) + "/web"
COLLECTION_API = EXT_API_GATEWAY + "/collections"
LOGIN_API      = EXT_API_GATEWAY + "/users/login"

SECRET = "some secret"
