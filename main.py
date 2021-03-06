import webapp2
import jinja2
from google.appengine.api import users
import os
import time
from profile_model import Show
from profile_model import Profile
from seed_data import seed_data
from google.appengine.api import urlfetch
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def force_signup(handler):
    user = users.get_current_user()
    if not user:
        handler.redirect('/login')
        return None
    my_profile = Profile.query().filter(Profile.user_id == user.user_id()).get()
    if not my_profile:
        handler.redirect('/nickname')
    return user, my_profile


class MainHandler(webapp2.RequestHandler):
  def get(self):
    welcome_template = JINJA_ENVIRONMENT.get_template("templates/welcome.html")
    user = users.get_current_user()
    if not user:
        self.redirect('/login')
        return

    nickname = user.nickname()
    login_url = users.create_logout_url('/')
    login_text = "sign out"

    self.response.write(welcome_template.render({
        "nickname": nickname,
        "login_url" : login_url,
        "login_text": login_text}))

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    login_template = JINJA_ENVIRONMENT.get_template("templates/login.html")
    user = users.get_current_user()
    if user:
        self.redirect('/')
        return

    login_url = users.create_login_url('/')
    login_text = "Sign in"
    nickname = "guest"

    self.response.write(login_template.render({
        "nickname": nickname,
        "login_url" : login_url,
        "login_text": login_text}))


class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        _, my_profile = force_signup(self)
        if not my_profile:
            return
        show_list_template = JINJA_ENVIRONMENT.get_template("templates/profile.html")
        your_shows = Show.query().filter(Show.user == my_profile.key).order(Show.show_name).fetch()
        all_shows = Show.query().order(Show.show_name).fetch()
        dict_for_template = {
            'profile': my_profile,
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
        _, my_profile = force_signup(self)
        if not my_profile:
            return

        list_template = JINJA_ENVIRONMENT.get_template("templates/list.html")
#Gets the search text
        user_search = self.request.get('user_search_html')
#If there isnt a search return nothing
        if not user_search:
            self.response.write(list_template.render())
        else:
            user_search2 =  user_search.replace(" ", "+")
            url = 'https://api.themoviedb.org/3/search/tv?api_key=affe4b9cbbe43b30bf85a6ae31037c7d&query=%s' %(user_search2)
            result = urlfetch.fetch(url)
            result_decoded = result.content.decode('utf-8')
            result_json = json.loads(result_decoded)
#If there arent results then disply text
            if not result_json['results']:
                result_dict = {
                    "nothing_here": '"' + user_search + '" didn\'t match any results.'
                }
                self.response.write(list_template.render(result_dict))
            else:
                result_dict = {
                    "shows": result_json['results'][:10],
                }
                self.response.write(list_template.render(result_dict))

    def post(self):
        my_user, my_profile = force_signup(self)
        if not my_profile:
            return

        # We ar assuming the user has a profile at this point
        my_profile = Profile.query().filter(Profile.user_id == my_user.user_id ()).fetch(1)[0]
        the_show_wanted = self.request.get('user-show')
        show_poster = self.request.get('poster_path')
        #put shows into the database
        show_record = Show()
        show_record.show_name = the_show_wanted
        show_record.poster_path = show_poster
        show_record.user = my_profile.key
        show_record.put()
        time.sleep(0.1)
        self.redirect('/list')

class Friends(webapp2.RequestHandler):
    def get(self):
        my_user, my_profile = force_signup(self)
        if not my_profile:
            return
        friends_template = JINJA_ENVIRONMENT.get_template("templates/friends.html")
        all_shows = Show.query().order(Show.user, Show.show_name).filter(Show.user != my_profile.key).fetch()
        all_profiles = Profile.query().filter(Profile.user_id != my_user.user_id()).order(Profile.user_id, Profile.nickname).fetch()

        shows_mapping = {}

        for profile in all_profiles:
            shows_mapping[profile.key.id()] = {'profile': profile, 'shows': []}

        for show in all_shows:
            user_id = show.user.id()
            shows_mapping[user_id]['shows'].append(show)
        dict_for_template = {
            'shows_mapping': shows_mapping,
        }

        self.response.write(friends_template.render(dict_for_template))

class NickName(webapp2.RequestHandler):
    def get(self):
        my_user = users.get_current_user()
        profile_template = JINJA_ENVIRONMENT.get_template("templates/nickname.html")
        my_profile = Profile.query().filter(Profile.user_id == my_user.user_id ()).get()

        dict_for_template = {
            'profile': my_profile
        }
        self.response.write(profile_template.render(dict_for_template))

    def post(self):
        my_user, my_profile = force_signup(self)
        if not my_profile:
            my_profile = Profile()
        my_nickname = self.request.get('nickname')
        my_profile.nickname = my_nickname
        my_profile.user_id = my_user.user_id()
        my_profile.put()
        time.sleep(0.1)
        self.redirect('/')

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/login', LoginHandler),
  ('/profile', ProfileHandler),
  ('/list', List),
  ('/friends', Friends),
  ('/nickname', NickName),
], debug=True)
