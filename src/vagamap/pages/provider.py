import webapp2
import wtforms
import jinja2
import new
import base
from vagamap.models import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(base.folder))

def execute(code):
    module = new.module('usercode')
    exec code in module.__dict__
    return module 
    
class ProviderForm(wtforms.Form):
    code = wtforms.TextAreaField('Code',  [wtforms.validators.Required(), ] )

class TestPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        name = self.request.get('name')
        provider = db.Key.from_path('Employee', 'asalieri')

        form = ProviderForm(self.request.POST)
        output = ''
        if self.request.method == 'POST' and form.validate():
            try:
                usercode = execute(form.code.data)
                output = usercode.test()
            except Exception as e:
                output = str(e)
            
        template_values = {
            'form':form, 
            'output':output
        }

        template = jinja_environment.get_template('templates/code_editor.html')
        self.response.out.write(template.render(template_values))
        

    def post(self):
        self.get()


editor = webapp2.WSGIApplication([('/provider/edit', TestPage)], debug=True)
