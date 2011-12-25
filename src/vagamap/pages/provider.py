import webapp2
import wtforms
import jinja2
import new
import base
from wtforms.ext.appengine.db import model_form
from vagamap.models import *

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(base.folder))

def execute(code):
    module = new.module('usercode')
    exec code in module.__dict__
    return module 

class ProviderForm(model_form(Provider)):
    pass

class TestPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        key_name = self.request.get('key_name')
        provider = None
        if key_name:
            provider = db.get(db.Key.from_path('Provider', key_name))

        if self.request.method == 'POST':
            form = ProviderForm(self.request.POST)
            if form.validate():
                name = form.name.data
                provider = Provider(key_name=name, name=name)
                provider.code = form.code.data
                provider.test_input = form.test_input.data
                provider.put()
                self.redirect("./edit?key_name={}".format(name))
        elif provider:
            form = ProviderForm(obj=provider)
        else:
            form = ProviderForm()
            pass
            
        template_values = {
            'form':form
        }

        template = jinja_environment.get_template('templates/code_editor.html')
        self.response.out.write(template.render(template_values))
        

    def post(self):
        self.get()


editor = webapp2.WSGIApplication([('/provider/edit', TestPage)], debug=True)
