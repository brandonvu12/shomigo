from google.appengine.ext import ndb



class Watched(ndb.Model):
    show_watched = ndb.StringProperty(required = True)
    user_id = ndb.StringProperty()

class Profile(ndb.Model):
     nickname = ndb.StringProperty(required = True)
     user_id = ndb.StringProperty()
     joined_on = ndb.DateTimeProperty(auto_now_add = True)
     updated_on = ndb.DateTimeProperty(auto_now = True)
