from datetime import datetime


class Timestamp(object):
    """
    Firestore timestamp object. When stored in Cloud Firestore, precise
    only to microseconds; any additional precision is rounded down
    """
    def __init__(self, *args, **kwargs):
        pass
