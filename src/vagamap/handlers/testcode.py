'''
Created on Dec 24, 2011

@author: Matt
'''
import webapp2
from cStringIO import StringIO
import sys
import traceback

from vagamap.util import to_module

class CodeTester(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        code = self.request.get('code')
        test_data = self.request.get('input')
        
        old_stdout = sys.stdout
        sys.stdout = out = StringIO()
        try:
            usercode = to_module(code, test_data)
            if hasattr(usercode, 'test'):
                usercode.test()
        except:
            traceback.print_exc(file=out)
            #output = str(e)
        finally:
            sys.stdout = old_stdout
        
        output = str(out.getvalue())
        self.response.out.write(output)

handler = webapp2.WSGIApplication([('/handlers/testcode', CodeTester)], debug=True)