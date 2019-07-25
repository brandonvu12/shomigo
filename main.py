import webapp2
import jinja2
from google.appengine.api import users
import os
from profile_model import Watched
from seed_data import seed_data
from google.appengine.api import urlfetch

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

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        my_user = users.get_current_user()
        show_list_template = JINJA_ENVIRONMENT.get_template("templates/profile.html")
        your_shows = Watched.query().order(-Watched.show_watched).fetch()
        all_shows = Watched.query().order(-Watched.show_watched).fetch()
        dict_for_template = {
            'you_watched': your_shows,
        }
        self.response.write(show_list_template.render(dict_for_template))

    def post(self):
        the_show_wanted = self.request.get('user-show')

        #put into database
        show_record = Watched(show_watched = the_show_wanted)
        show_record.put()

class List(webapp2.RequestHandler):
    def get(self):
        list_template = JINJA_ENVIRONMENT.get_template("templates/list.html")
        #gets the search text and gets it from the api
        user_search = self.request.get('user_search_html')
        url = 'https://api.themoviedb.org/3/search/tv?api_key=affe4b9cbbe43b30bf85a6ae31037c7d&query=%s' %(user_search)
        result = urlfetch.fetch(url)
        result_dict = {
            "show_return": result.content.decode('utf-8'),
        }
        self.response.write(list_template.render(result_dict))

class Friends(webapp2.RequestHandler):
    def get(self):
        friends_template = JINJA_ENVIRONMENT.get_template("templates/friends.html")
        all_shows = Watched.query().order(-Watched.show_watched).fetch()
        dict_for_template = {
            'friend_shows': all_shows,
        }
        self.response.write(friends_template.render(dict_for_template))

class LoadDataHandler(webapp2.RequestHandler):
    def get(self):
        seed_data()

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/profile', ProfileHandler),
  ('/list', List),
  ('/friends', Friends),
], debug=True)
