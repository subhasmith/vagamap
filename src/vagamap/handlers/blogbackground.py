import webapp2
from google.appengine.api import urlfetch
from BeautifulSoup import BeautifulStoneSoup
import urllib
import PIL
import PIL.Image
import PIL.ImageFilter
import StringIO
import PIL.ImageEnhance
import PIL.ImageOps
from google.appengine.api import memcache
import logging
import re

ENDPOINT = "http://api.flickr.com/services/rest/"
NSID = "76867575@N02"
API_KEY = "bce442cfd26e3f51e1d30207672cdaff"

class BlogBackground(webapp2.RequestHandler):
    def get_most_recent_photo_id(self, back=0):
        params = {
            'method':'flickr.people.getPublicPhotos',
            'api_key':API_KEY,
            'user_id':NSID,
            'per_page':(back + 1)
            }
    
        response = urlfetch.fetch(ENDPOINT + "?" + urllib.urlencode(params)).content
        soup = BeautifulStoneSoup(response)
        return soup('photo')[back]['id']

    def get_photo_url(self, photo_id, size_label):
        params = {
        'method':'flickr.photos.getSizes',
        'api_key':API_KEY,
        'photo_id':photo_id
        }
        soup = BeautifulStoneSoup(urlfetch.fetch(ENDPOINT + "?" + urllib.urlencode(params)).content)
        sizes = soup('size', {'label':size_label})
        if not sizes: return None
        return sizes[0]['source']
    
    def get_flickr_image(self, back=0, size="Medium"):
        photo_id = self.get_most_recent_photo_id(back=back)
        url = self.get_photo_url(photo_id, size)
        image = PIL.Image.open(StringIO.StringIO(urlfetch.fetch(url).content)).convert("RGBA")
        image = PIL.ImageOps.expand(image, border=10, fill='white')
        return image
    
    
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
        
        i1r = self.request.get('i1r')
        i1x = self.request.get('i1x')
        i1y = self.request.get('i1y')
        i1s = self.request.get('i1s')
        
        i2r = self.request.get('i2r')
        i2x = self.request.get('i2x')
        i2y = self.request.get('i2y')
        i2s = self.request.get('i2s')
         
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
        args = (centered, zoom, maptype, color, brightness, quality, blur, latitude, longitude, yoffset, xoffset, style, i1r, i1x, i1y, i1s, i2r, i2x, i2y, i2s)
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
        
        # composite last image from flickr
        if i1x and i1y and i1r:
            try:
                if not i1s:
                    i1s = 'Medium'
                flickr_image = self.get_flickr_image(back=0, size=i1s)
                if flickr_image:
                    flickr_image = flickr_image.rotate(int(i1r), PIL.Image.BICUBIC, True)
                    map_image.paste(flickr_image, (int(i1x), int(i1y)), flickr_image)
            except:
                logging.exception("Error loading flickr image 1.")
        
        # composite next to last image from flickr
        if i2x and i2y and i2r:
            try:
                if not i2s:
                    i2s = 'Medium'
                flickr_image2 = self.get_flickr_image(back=1, size=i2s)
                if flickr_image2:
                    flickr_image2 = flickr_image2.rotate(int(i2r), PIL.Image.BICUBIC, True)
                    map_image.paste(flickr_image2, (int(i2x), int(i2y)), flickr_image2)
            except:
                logging.exception("Error loading flickr image 2.")
        
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
        2
        memcache.add(memkey, map_data_out.getvalue(), 21600)
        
        self.response.headers['Content-Type'] = "image/jpeg"
        self.response.out.write(map_data_out.getvalue())

handler = webapp2.WSGIApplication([('/handlers/misc/blogbackground', BlogBackground)], debug=True)