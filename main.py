import webapp2
import jinja2
from google.appengine.api import users
import os
from profile_model import Watched
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

class Profile(webapp2.RequestHandler):
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

# class EditProfileHandler(webapp2.RequestHandler):
#     def get(self):
#         personal_key_string = self.request get('personal_key')
#         personal_key = ndb.key(urlsafe = personal_key_string)
#         personal = personal_key.get()
#         user = uses.get_current_user()
#         if  BLAH.creator != user.user_id():
#             pass
#         else:

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
            result_show1 = result_json['results'][0]['name']
            result_date1 = result_json['results'][0]['first_air_date']
#Sends it to the html file
            result_dict = {
                "show_return1": result_show1,
                "show_date1": result_date1,
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
  ('/profile', Profile),
  ('/list', List),
  ('/friends', Friends),
], debug=True)
