import webapp2
from google.appengine.api import urlfetch
import BeautifulSoup
from kml import Kml, Place, Style, IconStyle, Coordinate, LineString, LineStyle
import datetime

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    return s

class BlogKml(webapp2.RequestHandler):
    def get(self):
        url = """http://vagasapien.blogspot.com/feeds/posts/default"""
        response = urlfetch.fetch(url)
        if response.status_code != 200: return
        
        soup = BeautifulSoup.BeautifulSoup(response.content)
        
        kml = Kml("Vagasapien")
        waypoint_style = Style(
            "waypoint",
            IconStyle(
            "http://maps.google.com/mapfiles/ms/micons/red.png")
            )
        current_style = Style(
            "current",
            IconStyle(
            "http://maps.google.com/mapfiles/ms/micons/red-dot.png")
            )
        line_style = Style(
            "line",
            LineStyle(
                "A00000FF",
                5)
            )
        coordinates = []
        first = True
        
        pub_months = {}
        pub_years = {}
        
        for entry in soup('entry'):
            published = entry('published')[0].text
            published = datetime.datetime.strptime(published[:19], '%Y-%m-%dT%H:%M:%S')
            pub_key = published.strftime("%Y/%m")
            pub_months[pub_key] = pub_months.get(pub_key, 0) + 1
            pub_yr_key = published.strftime("%Y")
            pub_years[pub_yr_key] = pub_years.get(pub_yr_key, 0) + 1
        
        for entry in soup('entry'):
            title = entry('title')[0].text
            href = entry('link', {'rel':'alternate'})[0]['href']
            content = unescape(entry('content')[0].text)
            points = entry('georss:point')
            if not points: continue
            latitude, longitude = entry('georss:point')[0].text.split()
            #thumbnails = entry('media:thumbnail')
            #thumbnail = thumbnails[0]['url'] if thumbnails else None
            published = entry('published')[0].text
            published = datetime.datetime.strptime(published[:19], '%Y-%m-%dT%H:%M:%S')
        
            coordinate = Coordinate(latitude, longitude)
            style = current_style if first else waypoint_style
            first = False
            content = "<p>" + datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %p") + "</p>" + \
                    "<br /><p>" + content + "</p><br />" + \
                    '<p><a href="{}" >View Full Blog Entry</a></p>'.format(href)
            pub_key = published.strftime("%Y/%m")
            pub_count = pub_months[pub_key]
            pub_yr_key = published.strftime("%Y")
            pub_yr_count = pub_years[pub_yr_key]
            year_sort = str(5000 - int(published.strftime("%Y")))
            month_sort = str(50 - int(published.strftime("%m")))
            place = Place('<a href="{}" >{}</a>'.format(href, title),
                          content,
                          coordinate,
                          style,
                          folder=year_sort + "|" + published.strftime("%Y") + " ({})/".format(pub_yr_count) + month_sort + "|" + published.strftime("%B") + " ({})".format(pub_count)) 
            coordinates.append(coordinate)
            kml.places.append(place)
        kml.lines.append(LineString("Route", line_style, coordinates))
        
        self.response.headers['Content-Type'] = "text/xml"
        self.response.out.write(kml.to_string())
                
handler = webapp2.WSGIApplication([('/handlers/misc/blogkml', BlogKml)], debug=True)