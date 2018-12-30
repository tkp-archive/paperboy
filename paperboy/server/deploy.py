import os

if os.name == 'nt':
    from .deploy_win import FalconWaitress as FalconDeploy  # noqa: F401
else:
    from .deploy_nix import FalconGunicorn as FalconDeploy  # noqa: F401
