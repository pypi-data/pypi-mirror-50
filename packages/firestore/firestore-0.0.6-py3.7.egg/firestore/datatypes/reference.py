from .datatype import Datatype


class Reference(Datatype):
    """Firestore referable elements i.e. Project ID,
    Document ID etc.
    """
    def __init__(self, *args, **kwargs):
        super(Reference, self).__init__(**kwargs)
        self.reference_path = args[0]
