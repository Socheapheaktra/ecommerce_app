from flask.views import MethodView
from flask_smorest import abort, Blueprint

from models import CountryModel
from schemas import *

blp = Blueprint("Country", __name__, description="Operations on Countries.")

@blp.route('/country')
class CountryOperation(MethodView):
    def get(self):
        """Return List of Countries from database"""
        abort(501)

    def post(self):
        """Add new Country record into database"""
        abort(501)

@blp.route('/country/<int:country_id>')
class CountryUpdate(MethodView):
    def get(self, country_id):
        """Return one record of country from database based on ID"""
        abort(501)

    def delete(self, country_id):
        """Delete a country from database based on ID"""
        abort(501)