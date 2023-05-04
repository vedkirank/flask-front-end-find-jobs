from flask import Blueprint
# Creating Blueprint
main = Blueprint('main',__name__,static_folder='static',template_folder='templates')

from . import authentication,signup,jobs