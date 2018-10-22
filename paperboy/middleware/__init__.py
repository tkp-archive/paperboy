# CORS middleware
from falcon_cors import CORS as CORSMiddleware

# Authentication middlewares
from falcon_helpers.middlewares.auth_required import AuthRequiredMiddleware
from falcon_helpers.middlewares.load_user import LoadUserMiddleware

# SQLAlchemy middleware
from falcon_helpers.middlewares.sqla import SQLAlchemySessionMiddleware

# Form handling middleware
from falcon_multipart.middleware import MultipartMiddleware

# Dummy auth
from .dummy import DummyUserMiddleware, DummyAuthRequiredMiddleware

# No auth
from .none import NoUserMiddleware, NoAuthRequiredMiddleware
