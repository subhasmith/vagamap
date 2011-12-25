import webapp2
import wtforms
import jinja2
import os
import new

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def execute(code):
    module = new.module('usercode')
    exec code in module.__dict__
    return module
    
class TestForm(wtforms.Form):
    code = wtforms.TextAreaField('Code',  [wtforms.validators.Required(), ] )

class TestPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        form = TestForm(self.request.POST)
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

        template = jinja_environment.get_template('test.html')
        self.response.out.write(template.render(template_values))
        

    def post(self):
        self.get()


app = webapp2.WSGIApplication([('/', TestPage)], debug=True)
