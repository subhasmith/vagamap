import webapp2
from google.appengine.api import urlfetch
from BeautifulSoup import BeautifulStoneSoup
import urllib

class BlogMap(webapp2.RequestHandler):
    def get(self):
        url = """http://vagasapien.blogspot.com/feeds/posts/default"""
        response = urlfetch.fetch(url)
        if response.status_code != 200: return
        
        centered = self.request.get('centered')
        zoom = self.request.get('zoom')
        maptype = self.request.get('maptype')
        length = self.request.get('length')
        
        feed = BeautifulStoneSoup(response.content)
        points = feed("georss:point")
        if not points: return
        latitude, longitude = points[0].text.split()
        
        route = []
        if length:
            length = int(length)
        else:
            length = 20
        for point in reversed(points[:length]):
            node = ','.join(point.text.split())
            route.append(node)
            
        path = str("color:red|weight:5|" + '|'.join(route))
        markers = 'color:red|{},{}'.format(latitude, longitude)
        
        #map_url="""http://maps.googleapis.com/maps/api/staticmap?center={}""".format(latitude + "," + longitude)
        #map_url += "&zoom=5&size=280x280&sensor=false"
        #self.redirect(map_url)
        
        params = {
                  'size':'265x265',
                  #'maptype':'satellite',
                  'sensor':'false',
                  'markers':markers
                  }
        
        if centered and centered.lower() == 'true':
            params['center'] = '{},{}'.format(latitude, longitude)
        
        if zoom:
            params['zoom'] = zoom
            
        if maptype:
            params['maptype'] = maptype
        
        if length > 0:
            params['path'] = path
        
        map_url = r"http://maps.googleapis.com/maps/api/staticmap?" + urllib.urlencode(params)
        #self.redirect(map_url)
        map_data = urlfetch.fetch(map_url)
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(map_data.content)
                
        

handler = webapp2.WSGIApplication([('/handlers/misc/blogmap', BlogMap)], debug=True)