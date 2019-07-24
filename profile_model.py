from google.appengine.ext import ndb



class Profile(ndb.Model):
        nickname =  ndb.StringProperty(required=True)
