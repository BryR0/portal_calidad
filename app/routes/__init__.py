from flask import Blueprint

auth_bp  = Blueprint('auth',  __name__)
nc_bp    = Blueprint('nc',    __name__, url_prefix='/nc')
main_bp  = Blueprint('main',  __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from . import auth, nc, main, admin
