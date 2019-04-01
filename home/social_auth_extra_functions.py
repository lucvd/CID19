

def save_extra_data(user, response, is_new, *args, **kwargs):

    try:
        if is_new:
            user.profile.headline = response['headline']
            user.profile.linkedin = response['publicProfileUrl']
        else:
            if user.profile.headline is '' and response['headline']:
                user.profile.headline = response['headline']
            if user.profile.linkedin is '' and response['publicProfileUrl']:
                user.profile.linkedin = response['publicProfileUrl']
    except Exception as e:
        print("Exception in save_extra_data:")
        print(e) # TODO log this