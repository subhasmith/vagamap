from google.appengine.ext import db
from vagamap.util import to_module
import sys
from cStringIO import StringIO
import traceback
import datetime

class Provider(db.Model):
    name = db.StringProperty(required=True)
    code = db.StringProperty(multiline=True)
    test_input = db.StringProperty(multiline=True)
    last_updated = db.DateTimeProperty(auto_now=True)
    last_invoked = db.DateProperty()
    last_load_count = db.IntegerProperty()
    last_output = db.StringProperty(multiline=True)
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
                places = usercode.execute()
                for place in places:
                    if not place.key_name.startswith(self.key_name):
                        raise Exception("Place key name '{}' must start with '{}::'.".format(place.key_name, self.key_name))
                    place.put()
                    self.last_load_count += 1
            else:
                raise Exception("No execute() function in provider code.")
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
    description = db.StringProperty(multiline=True)
    images = db.StringListProperty()
    
    