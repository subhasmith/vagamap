import webapp2
import wtforms
import jinja2
import new
import base
from wtforms.ext.appengine.db import model_form
from vagamap.models import *
import logging

jinja_environment = base.jinja_environment

class PlaceForm(model_form(Place)):
    pass

class ListPlaceHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        query = Place.all()
        query.order = "provider"
        query.order = "name"
        places = query.fetch(limit=50)
        logging.info('places fetched: {}'.format(len(places)))
        
        template_values = {
            'places':places
        }

        template = jinja_environment.get_template('place_list.html')
        self.response.out.write(template.render(template_values))
        
    def post(self):
        self.redirect('/place/edit')


place_list = webapp2.WSGIApplication([('/place/list', ListPlaceHandler)], debug=True)