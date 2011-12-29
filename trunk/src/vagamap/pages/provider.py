import webapp2
import wtforms
import jinja2
import new
import base
from wtforms.ext.appengine.db import model_form
from vagamap.models import *
import logging
from google.appengine.api import taskqueue

jinja_environment = base.jinja_environment

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
                key_name = name = form.name.data
                provider = Provider(key_name=name, name=name)
                provider.code = form.code.data
                provider.test_input = form.test_input.data
                provider.put()
                if self.request.get("run"):
                    def run_provider(key_name):
                        provider = db.get(db.Key.from_path('Provider', key_name))
                        provider.running = True;
                        provider.put()
                        taskqueue.add(url='/handlers/provider/run', transactional=True, params={'key_name':key_name})  
                        logging.info("task added")
                    db.run_in_transaction(run_provider, key_name)
                    
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
        
        
        
        
        
        
        
        
        
        

provider_edit = webapp2.WSGIApplication([('/provider/edit', EditProviderHandler)], debug=True)
provider_list = webapp2.WSGIApplication([('/provider/list', ListProviderHandler)], debug=True)
