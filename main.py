import webapp2
import jinja2
from google.appengine.api import users
import os
import time
from profile_model import Show
from profile_model import Profile
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
        my_profiles = Profile.query().filter(Profile.user_id == my_user.user_id ()).fetch(1)
        if len(my_profiles) == 1:
            my_profile = my_profiles[0]
        else:
            my_profile = Profile()
        your_shows = Show.query().filter(Show.user == my_profile.key).order(-Show.show_name).fetch()
        all_shows = Show.query().order(-Show.show_name).fetch()
        dict_for_template = {
            'shows': your_shows,
            'all_shows': all_shows,
        }
        self.response.write(show_list_template.render(dict_for_template))

    def post(self):
        my_user = users.get_current_user()
        # We ar assuming the user has a profile at this point
        my_profile = Profile.query().filter(Profile.user_id == my_user.user_id ()).fetch(1)[0]
        the_show_wanted = self.request.get('user-show')
        #put shows into the database
        show_record = Show()
        show_record.show_name = the_show_wanted
        show_record.user = my_profile.key
        show_record.put()
        time.sleep(0.1)
        self.redirect('/profile')

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
        all_shows = Show.query().order(-Show.show_name).fetch()
        dict_for_template = {
            'friend_shows': all_shows,
        }
        self.response.write(friends_template.render(dict_for_template))

class NickName(webapp2.RequestHandler):
    def get(self):
        my_user = users.get_current_user()
        profile_template = JINJA_ENVIRONMENT.get_template("templates/nickname.html")
        my_profiles = Profile.query().filter(Profile.user_id == my_user.user_id ()).fetch(1)
        if len(my_profiles) == 1:
            my_profile = my_profiles[0]
        else:
            my_profile = None
        dict_for_template = {
            'profile': my_profile
        }
        self.response.write(profile_template.render(dict_for_template))

    def post(self):
        my_user = users.get_current_user()
        my_nickname = self.request.get('nickname')

        my_profiles = Profile.query().filter(Profile.user_id == my_user.user_id ()).fetch(1)
        if len(my_profiles) == 1:
            my_profile = my_profiles[0]
        else:
            my_profile = Profile()

        my_profile.nickname = my_nickname
        my_profile.user_id = my_user.user_id()
        my_profile.put()
        self.redirect('/profile')

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/profile', ProfileHandler),
  ('/list', List),
  ('/friends', Friends),
  ('/nickname', NickName),

], debug=True)
