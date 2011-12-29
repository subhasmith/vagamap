from google.appengine.ext import db
import webapp2
import logging
from vagamap.models import Provider

class CodeTester(webapp2.RequestHandler):
    def post(self):
        key_name = self.request.get('key_name')
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Running provider '{}'".format(key_name))
        
        provider = db.get(db.Key.from_path('Provider', key_name))
        provider.run()
        
    def get(self):
        self.post()

provider_run = webapp2.WSGIApplication([('/handlers/provider/run', CodeTester)], debug=True)