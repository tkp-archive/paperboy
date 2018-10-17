from falcon_auth import FalconAuthMiddleware as AuthMiddleware, BasicAuthBackend

user_loader = lambda username, password: { 'username': username }
auth_backend = BasicAuthBackend(user_loader)
