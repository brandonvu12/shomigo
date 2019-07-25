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

class MainHandler(webapp2.RequestHandler):
  def get(self):
    login_template = JINJA_ENVIRONMENT.get_template("templates/login.html")
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        login_url = users.create_logout_url('/')
        login_text = "sign out"
    else:
        login_url = users.create_login_url('/')
        login_text = "Sign in"
        nickname = "guest"

    self.response.write(login_template.render({
        "nickname": nickname,
        "login_url" : login_url,
        "login_text": login_text}))

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
#Gets the search text
        user_search = self.request.get('user_search_html')
#If there isnt a search return nothing
        if not user_search:
            self.response.write(list_template.render())
        else:
            user_search =  user_search.replace(" ", "+")
            url = 'https://api.themoviedb.org/3/search/tv?api_key=affe4b9cbbe43b30bf85a6ae31037c7d&query=%s' %(user_search)
            result = urlfetch.fetch(url)
            result_decoded = result.content.decode('utf-8')
            result_json = json.loads(result_decoded)
#If there arent results then disply text
            if not result_json['results']:
                result_dict = {
                    "show_return1": "No shows match your search",
                }
                self.response.write(list_template.render(result_dict))
            else:
                number_of_results = len(result_json['results'])
                result_show1 = result_json['results'][0]['name']
                result_date1 = result_json['results'][0]['first_air_date']
                result_poster1 = result_json['results'][0]['poster_path']
                poster_url1 = "https://image.tmdb.org/t/p/w185%s" %(result_poster1)
                if number_of_results >= 5:
                    result_show2 = result_json['results'][1]['name']
                    result_date2 = result_json['results'][1]['first_air_date']
                    result_poster2 = result_json['results'][1]['poster_path']
                    result_show3 = result_json['results'][2]['name']
                    result_date3 = result_json['results'][2]['first_air_date']
                    result_poster3 = result_json['results'][2]['poster_path']
                    result_show4 = result_json['results'][3]['name']
                    result_date4 = result_json['results'][3]['first_air_date']
                    result_poster4 = result_json['results'][3]['poster_path']
                    result_show5 = result_json['results'][4]['name']
                    result_date5 = result_json['results'][4]['first_air_date']
                    result_poster5 = result_json['results'][4]['poster_path']
                    poster_url2 = "https://image.tmdb.org/t/p/w185%s" %(result_poster2)
                    poster_url3 = "https://image.tmdb.org/t/p/w185%s" %(result_poster3)
                    poster_url4 = "https://image.tmdb.org/t/p/w185%s" %(result_poster4)
                    poster_url5 = "https://image.tmdb.org/t/p/w185%s" %(result_poster5)

                elif number_of_results >= 4:
                    result_show2 = result_json['results'][1]['name']
                    result_date2 = result_json['results'][1]['first_air_date']
                    result_poster2 = result_json['results'][1]['poster_path']
                    result_show3 = result_json['results'][2]['name']
                    result_date3 = result_json['results'][2]['first_air_date']
                    result_poster3 = result_json['results'][2]['poster_path']
                    result_show4 = result_json['results'][3]['name']
                    result_date4 = result_json['results'][3]['first_air_date']
                    result_poster4 = result_json['results'][3]['poster_path']
                    result_show5 = ""
                    result_date5 = ""
                    result_poster5 = ""
                    poster_url2 = "https://image.tmdb.org/t/p/w185%s" %(result_poster2)
                    poster_url3 = "https://image.tmdb.org/t/p/w185%s" %(result_poster3)
                    poster_url4 = "https://image.tmdb.org/t/p/w185%s" %(result_poster4)
                    poster_url5 = ""

                elif number_of_results >= 3:
                    result_show2 = result_json['results'][1]['name']
                    result_date2 = result_json['results'][1]['first_air_date']
                    result_poster2 = result_json['results'][1]['poster_path']
                    result_show3 = result_json['results'][2]['name']
                    result_date3 = result_json['results'][2]['first_air_date']
                    result_poster3 = result_json['results'][2]['poster_path']
                    result_show4 = ""
                    result_date4 = ""
                    result_poster4 = ""
                    result_show5 = ""
                    result_date5 = ""
                    result_poster5 = ""
                    poster_url2 = "https://image.tmdb.org/t/p/w185%s" %(result_poster2)
                    poster_url3 = "https://image.tmdb.org/t/p/w185%s" %(result_poster3)
                    poster_url4 = ""
                    poster_url5 = ""
                elif number_of_results >= 2:
                    result_show2 = result_json['results'][1]['name']
                    result_date2 = result_json['results'][1]['first_air_date']
                    result_poster2 = result_json['results'][1]['poster_path']
                    result_show3 = ""
                    result_date3 = ""
                    result_poster3 = ""
                    result_show4 = ""
                    result_date4 = ""
                    result_poster4 = ""
                    result_show5 = ""
                    result_date5 = ""
                    result_poster5 = ""
                    poster_url2 = "https://image.tmdb.org/t/p/w185%s" %(result_poster2)
                    poster_url3 = ""
                    poster_url4 = ""
                    poster_url5 = ""
                else:
                    result_show2 = ""
                    result_date2 = ""
                    result_poster2 = ""
                    result_show3 = ""
                    result_date3 = ""
                    result_poster3 = ""
                    result_show4 = ""
                    result_date4 = ""
                    result_poster4 = ""
                    result_show5 = ""
                    result_date5 = ""
                    result_poster5 = ""
                    poster_url2 = ""
                    poster_url3 = ""
                    poster_url4 = ""
                    poster_url5 = ""
                result_dict = {
                    "show_return1": result_show1,
                    "show_date1": result_date1,
                    "show_poster1": poster_url1,
                    "show_return2": result_show2,
                    "show_date2": result_date2,
                    "show_poster2": poster_url2,
                    "show_return3": result_show3,
                    "show_date3": result_date3,
                    "show_poster3": poster_url3,
                    "show_return4": result_show4,
                    "show_date4": result_date4,
                    "show_poster4": poster_url4,
                    "show_return5": result_show5,
                    "show_date5": result_date5,
                    "show_poster5": poster_url5,

                }

                self.response.write(list_template.render(result_dict))

class Friends(webapp2.RequestHandler):
    def get(self):
        friends_template = JINJA_ENVIRONMENT.get_template("templates/friends.html")
        all_shows = Show.query().order(-Show.show_name).fetch()
        all_profiles = Profile.query().order(-Profile.nickname).fetch()

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
