import webapp2
import base
from wtforms.ext.appengine.db import model_form
from vagamap.models import *

jinja_environment = base.jinja_environment


class CountriesHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        template_values = {
            
        }
        template = jinja_environment.get_template('countries.html')
        self.response.out.write(template.render(template_values))
        
    def post(self):
        self.redirect('/countries')


countries_app = webapp2.WSGIApplication([('/countries', CountriesHandler)], debug=True)