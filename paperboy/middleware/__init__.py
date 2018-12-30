# CORS middleware
from falcon_cors import CORS as CORSMiddleware  # noqa: F401

# Authentication middlewares
from falcon_helpers.middlewares.auth_required import AuthRequiredMiddleware  # noqa: F401
from falcon_helpers.middlewares.load_user import LoadUserMiddleware  # noqa: F401

# Form handling middleware
from falcon_multipart.middleware import MultipartMiddleware  # noqa: F401

# No auth
from .none import NoUserMiddleware, NoAuthRequiredMiddleware  # noqa: F401

# SQL
from .sqla import SQLUserMiddleware, SQLAuthRequiredMiddleware, SQLAlchemySessionMiddleware  # noqa: F401
