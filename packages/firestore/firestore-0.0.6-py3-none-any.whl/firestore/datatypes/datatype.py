


class Datatype(object):
    """
    Super class for document valid datatypes, Datatype can be used
    directly as well as all classes inherently inherit
    commonalities from Datatype
    """
    def __init__(self, *args, **kwargs):
        pass
    
    def __get__(self, obj, instance):
        """
        Descriptor protocol get binding accessor method
        """
        pass
    
    def __set__(self, obj, value):
        """Descriptor protocol set binding method, making
        this a data descriptor and setting precedence of this
        object over the containing obj's dictionary of instance
        attributes.
        """
        pass
