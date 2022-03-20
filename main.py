

# -------------------------------------------------
#  External Imports
# -------------------------------------------------
import connexion
from flask_cors import CORS

# -------------------------------------------------
#  Python Imports
# -------------------------------------------------
from os import environ

# -------------------------------------------------
#  Module Imports
# -------------------------------------------------
from errors.v1 import handlers as error_handlers

# -------------------------------------------------
#  Setup
# -------------------------------------------------
# Setup the connexion app - for swagger self documenting API routes
app = connexion.FlaskApp(__name__)
app.add_api('openapi.yaml',
            strict_validation=True,
            arguments={'title': 'Fathat.io Star Wars Project'})

# Our Blueprints, this might be better to create a single blueprint for the api and add to it...???
app.app.register_blueprint(error_handlers.error_handlers)


# Add CORS support
# TODO: add as a feature flag
CORS(app.app)


# -------------------------------------------------
#  Kick off
# -------------------------------------------------
def startup():
    """
        Method to fire any startup config stuff up
    :return:
    """
    pass


if __name__ == '__main__':
    startup()

    # Use host from environment variable if specified, otherwise use the localhost as the default host.
    starwars_api_host = environ.get('STARWARS_API_HOST')
    host = "127.0.0.1" if starwars_api_host is None else starwars_api_host

    # Use port from environment variable if specified, otherwise use 5003 as the default port.
    starwars_api_port = environ.get('STARWARS_API_PORT')
    port = 5003 if starwars_api_port is None else starwars_api_port

    app.run(host=host, port=port)
