from profile_model import Watched


def seed_data():
    user_key = Profile(name= user.nickname(), shows = "The Flash").put()
