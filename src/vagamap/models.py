from google.appengine.ext import db
from vagamap.util import to_module
import sys
from cStringIO import StringIO
import traceback
import datetime

class Provider(db.Model):
    name = db.StringProperty(required=True)
    code = db.TextProperty()
    test_input = db.TextProperty()
    last_updated = db.DateTimeProperty(auto_now=True)
    last_invoked = db.DateTimeProperty()
    last_load_count = db.IntegerProperty(default=0)
    last_output = db.TextProperty()
    exception = db.BooleanProperty(default=False)
    
    def run(self):
        self.last_invoked = datetime.datetime.now()
        self.last_load_count = 0
        self.last_output = ''
        self.exception = False
        
        old_stdout = sys.stdout
        sys.stdout = out = StringIO()
        try:
            usercode = to_module(self.code, self.test_input)
            if hasattr(usercode, 'run'):
                places = usercode.run()
                for place in places:
                    place.provider = self.name
                    
                    query = Place.all()
                    query.filter("provider =", place.provider)
                    query.filter("name =", place.name)
                    existing = query.get()
                    
                    if existing:
                        print ">> updating: '{}'".format(place.name)
                        ignore =  ['name', 'provider', 'modified_properties'] + existing.modified_properties
                        changed = False
                        for key in place.properties():
                            if key in ignore: continue
                            if not getattr(existing, key) == getattr(place, key):
                                setattr(existing, key, getattr(place, key))
                                print '    .{}'.format(key)
                                changed = True
                        if changed:
                            existing.put()
                    else:
                        print ">> creating: '{}'".format(place.name)
                        place.put()
                    self.last_load_count += 1
            else:
                raise Exception("No run() function in provider code.")
        except:
            self.exception = True
            traceback.print_exc(file=out)
        finally:
            sys.stdout = old_stdout
        self.last_output = str(out.getvalue())
        self.put()
    
class Place(db.Model):
    name = db.StringProperty(required=True)
    provider = db.StringProperty()
    coordinates = db.GeoPtProperty()
    description = db.TextProperty()
    images = db.StringListProperty()
    modified_properties = db.StringListProperty()
    