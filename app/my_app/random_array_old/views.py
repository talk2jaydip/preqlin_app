from flask import Blueprint
from my_app.random_array.models import MESSAGES

random_array_bp = Blueprint('random_array', __name__)


@random_array_bp.route('/')
@random_array_bp.route('/random_array')
def random_array_():
    return MESSAGES['default']


