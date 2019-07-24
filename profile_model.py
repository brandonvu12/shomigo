from google.appengine.ext import ndb



class Profile(ndb.Model):
        username =  ndb.StringProperty(required=True)
