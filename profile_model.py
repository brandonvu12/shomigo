from google.appengine.ext import ndb



class Profile(ndb.Model):
    name =  ndb.KeyProperty(required = True)
    shows = ndb.StringProperty(required = False)
