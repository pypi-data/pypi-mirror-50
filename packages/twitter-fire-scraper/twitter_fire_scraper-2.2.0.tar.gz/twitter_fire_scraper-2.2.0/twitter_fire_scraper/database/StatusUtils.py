from tweepy import Status


def status_from_dict(d: dict) -> Status:
    return Status().parse(None, d)
