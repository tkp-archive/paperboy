# CORS middleware
from falcon_cors import CORS as CORSMiddleware

# Authentication middlewares
from falcon_helpers.middlewares.auth_required import AuthRequiredMiddleware
from falcon_helpers.middlewares.load_user import LoadUserMiddleware

# Form handling middleware
from falcon_multipart.middleware import MultipartMiddleware

# No auth
from .none import NoUserMiddleware, NoAuthRequiredMiddleware

# SQL
from .sqla import SQLUserMiddleware, SQLAuthRequiredMiddleware, SQLAlchemySessionMiddleware
