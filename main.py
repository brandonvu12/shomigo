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
    login_template = JINJA_ENVIRONMENT.get_template("templates/login.html")
    user = users.get_current_user()
    if user:
        self.response.write(login_template.render())
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        greeting = '{} (<a href="{}">sign out</a>)'.format(
        nickname, logout_url)
    else:
        login_url = users.create_login_url('/')
        greeting = '<a href="{}">Sign in</a>'.format(login_url)
    self.response.write(greeting)

class Profile(webapp2.RequestHandler):
    def get(self):
        profile_template = JINJA_ENVIRONMENT.get_template("templates/profile.html")
        self.response.write(profile_template.render())
        my_list = []

class List(webapp2.RequestHandler):
    def get(self):
        list_template = JINJA_ENVIRONMENT.get_template("templates/list.html")
        self.response.write(list_template.render())

class Friends(webapp2.RequestHandler):
    def get(self):
        friends_template = JINJA_ENVIRONMENT.get_template("templates/friends.html")
        self.response.write(friends_template.render())


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/profile', Profile),
  ('/list', List),
  ('/friends', Friends),
], debug=True)
