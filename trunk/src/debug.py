import os
import webapp2



class DebugHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        
        folder = os.path.dirname(__file__)
        for dirname, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                self.response.write(os.path.join(dirname, filename) + '\n')

handler = webapp2.WSGIApplication([('/debug', DebugHandler)], debug=True)