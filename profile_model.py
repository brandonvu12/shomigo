from google.appengine.ext import ndb



class Watched(ndb.Model):
    show_watched = ndb.StringProperty(required = True)
    user_id = ndb.StringProperty()
