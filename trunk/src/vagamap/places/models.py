from google.appengine.ext import db

class Place(db.Model):
    coordinates = db.GeoPtProperty(required=True)
    name = db.StringProperty(required=True)
    html = db.StringProperty()
    icon = db.StringProperty()

    