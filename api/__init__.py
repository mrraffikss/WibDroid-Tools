from webapp import app
from api.security_api import security_api
app.register_blueprint(security_api, url_prefix="/api/security")
