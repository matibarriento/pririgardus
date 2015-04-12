from functools import wraps
from flask import render_template
from flask.ext.login import current_user
import logging

logger = logging.getLogger('PRG')


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            for rol in current_user.roles:
                if rol.descripcion in roles:
                    return f(*args, **kwargs)
                    break
            return render_template("index.html")
        return wrapped
    return wrapper
