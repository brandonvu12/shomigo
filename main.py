import webapp2
from google.appengine.api import users


class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      self.response.write("You're logged in!")
    else:
      # This line creates a URL to log in with your Google Credentials.
      login_url = users.create_login_url('/')
      # This line uses string templating to create an anchor (link) element.
      login_html_element = '<a href="%s">Sign in</a>' % login_url
      # This line puts that URL on screen in a clickable anchor elememt.
      self.response.write('Please log in.<b>' + login_html_element)

app = webapp2.WSGIApplication([
  ('/', MainHandler)
], debug=True)
