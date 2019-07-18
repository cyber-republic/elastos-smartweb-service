# Flask settings
FLASK_SERVER_NAME = 'localhost:8888'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/elastos_admin'
SQLALCHEMY_TRACK_MODIFICATIONS = False

#GMU Net

#Wallet Service
WALLET_SERVICE_URL = 'http://localhost:8091/api/1'
WALLET_API_BALANCE = '/balance'