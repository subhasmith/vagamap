import webapp2

class UpdatePlace(webapp2.RequestHandler):
    def post(self):
        latitude = self.request.get['latitude']
        longitude = self.request.get['longitude']
        title = self.request.get['title']
        html = self.request.get['html']
        icon = self.request.get['icon']
        
        if not (latitude and longitude and title):
            #self.response.
            #TODO: ERROR
            return
        
        
                
        

update = webapp2.WSGIApplication([('/handlers/places/update', UpdatePlace)], debug=True)