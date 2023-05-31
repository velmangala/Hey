from functools import wraps
from flask import abort
from flask_login import current_user
from flask_principal import Permission, RoleNeed


def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)  # Unauthorized

            permission = Permission(RoleNeed(*roles))
            if not permission.can():
                abort(403)  # Forbidden

            return func(*args, **kwargs)

        return decorated_view

    return decorator
