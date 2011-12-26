import webapp2
import wtforms
import jinja2
import new
import base
from wtforms.ext.appengine.db import model_form
from vagamap.models import *

jinja_environment = base.jinja_environment

def execute(code):
    module = new.module('usercode')
    exec code in module.__dict__
    return module 

class ProviderForm(model_form(Provider)):
    pass

class EditProviderHandler(webapp2.RequestHandler):
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

        template = jinja_environment.get_template('provider_edit.html')
        self.response.out.write(template.render(template_values))
        
    def post(self):
        self.get()

class ListProviderHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        query = Provider.all()
        query.order = "name"
        providers = query.fetch(limit=50)
        
        template_values = {
            'providers':providers
        }

        template = jinja_environment.get_template('provider_list.html')
        self.response.out.write(template.render(template_values))
        
    def post(self):
        self.redirect('/provider/edit')
        
        
        
        
        
        
        
        
        
        

edit = webapp2.WSGIApplication([('/provider/edit', EditProviderHandler)], debug=True)
list = webapp2.WSGIApplication([('/provider/list', ListProviderHandler)], debug=True)
