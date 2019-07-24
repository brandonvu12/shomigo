from profile_model import Profile


def seed_data():
    nickname = Profile(student_id=423491377, first_name ="Ron", last_name = "Weasley").put()
