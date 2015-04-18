import re 
import logging

from functools import wraps
from flask import render_template
from flask.ext.login import current_user


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


def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    # convert = lambda text: int(text.numero) if text.numero.isdigit() else text.numero 
    # alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    # return sorted(l, key = alphanum_key)
    return l