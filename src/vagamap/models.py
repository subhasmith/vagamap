from google.appengine.ext import db
import datetime

class Provider(db.Model):
    name = db.StringProperty(required=True)
    code = db.StringProperty(multiline=True)
    test_input = db.StringProperty(multiline=True)
    test_data = db.StringProperty(multiline=True)
    last_updated = db.DateProperty(default=datetime.datetime.now())
    last_invoked = db.DateProperty()
    
