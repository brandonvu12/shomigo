import webapp2
import jinja2
from google.appengine.api import users
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
  def get(self):
      login_template = JINJA_ENVIRONMENT.get_template("login.html")
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
        nickname, logout_url)
    else:
        login_url = users.create_login_url('/')
        greeting = '<a href="{}">Sign in</a>'.format(login_url)
    self.response.write(greeting)
    login_template = JINJA_ENVIRONMENT.get_template('login.html')
    self.response.write(login_template.render())


app = webapp2.WSGIApplication([
  ('/', MainHandler)
], debug=True)
