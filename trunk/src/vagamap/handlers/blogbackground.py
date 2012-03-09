import webapp2
from google.appengine.api import urlfetch
from BeautifulSoup import BeautifulStoneSoup
import urllib
import PIL
import PIL.Image
import PIL.ImageFilter
import StringIO
import PIL.ImageEnhance
from google.appengine.api import memcache
import logging

class BlogBackground(webapp2.RequestHandler):
    def get(self):
        centered = self.request.get('centered')
        zoom = self.request.get('zoom')
        maptype = self.request.get('maptype')
        color = self.request.get('color')
        brightness = self.request.get('brightness')
        quality = self.request.get('quality')
        blur = self.request.get('blur')
        yoffset = self.request.get('yoffset')
        xoffset = self.request.get('xoffset')
        style = self.request.get('style')
         
        url = """http://vagasapien.blogspot.com/feeds/posts/default"""
        response = urlfetch.fetch(url)
        if response.status_code != 200: return
        
        
        
        feed = BeautifulStoneSoup(response.content)
        points = feed("georss:point")
        if not points: 
            latitude = "52.91"
            longitude = "-1.4"
        else:
            latitude, longitude = points[0].text.split()
        
        # check for post in memory
        args = (centered, zoom, maptype, color, brightness, quality, blur, latitude, longitude, yoffset, xoffset, style)
        memkey = "blogbackground(" + ",".join(args) + ")"
        cached_image = memcache.get(memkey)
        if cached_image is not None:
            logging.debug("got cached blog background image")
            self.response.headers['Content-Type'] = "image/jpeg"
            self.response.out.write(cached_image)
            return
        
        if yoffset:
            latitude = float(latitude) + float(yoffset)
        
        if xoffset:
            longitude = float(longitude) + float(xoffset)
        
        params = {
                  'size':'640x568',
                  'scale':2,
                  #'maptype':'satellite',
                  'sensor':'false'
                  #'markers':markers
                  }
        
        if centered and centered.lower() == 'true':
            params['center'] = '{},{}'.format(latitude, longitude)
        
        if zoom:
            params['zoom'] = zoom
            
        if maptype:
            params['maptype'] = maptype
            
        if style:
            params['style'] = style
        
        #if length > 0:
        #    params['path'] = path
        
        map_url = r"http://maps.googleapis.com/maps/api/staticmap?" + urllib.urlencode(params)
        #self.redirect(map_url)
        map_data = urlfetch.fetch(map_url).content 
        map_image = PIL.Image.open(StringIO.StringIO(map_data))
                
        map_image = map_image.convert("RGB")
        map_image = map_image.resize((1800, 1600), PIL.Image.BICUBIC)
        
        if not (blur and blur.lower() == 'false'):
            map_image = map_image.filter(PIL.ImageFilter.BLUR)
        
        if brightness:
            enhancer = PIL.ImageEnhance.Brightness(map_image)
            map_image = enhancer.enhance(float(brightness))
        
        if color:
            enhancer = PIL.ImageEnhance.Color(map_image)
            map_image = enhancer.enhance(float(color))
                
        map_data_out = StringIO.StringIO()
        if quality:
            qual = int(quality)
        else:
            qual = 30
        map_image.save(map_data_out, format="JPEG", quality=qual)
        
        memcache.add(memkey, map_data_out.getvalue(), 21600)
        
        self.response.headers['Content-Type'] = "image/jpeg"
        self.response.out.write(map_data_out.getvalue())
                
        

handler = webapp2.WSGIApplication([('/handlers/misc/blogbackground', BlogBackground)], debug=True)