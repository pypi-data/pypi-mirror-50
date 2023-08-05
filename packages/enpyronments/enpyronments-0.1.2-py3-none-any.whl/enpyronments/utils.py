""" 
Helper classes
"""


import sys


class UsePath():
    """Quick class to use as a context manager when importing from a relative path. While in this manager's context,
    avoid making changes to sys.path, as this manager inserts a value at the first position on enter, and removes
    whichever element is in that position on exit.
    """

    def __init__(self, path):
        """ Saves ``path`` to the UsePath instance """
        self.path = path

    def __enter__(self):
        """ Appends ``path`` to ``sys.path``, at index 0 (the start) """
        sys.path.insert(0, self.path)

    def __exit__(self, *args):
        """ Removes the item at ``sys.path``'s index 0 (should be ``path``). """
        sys.path.pop(0)


class Sensitive():
    """ Flags a setting as sensitive, indicating to the Settings object that
    this setting should be hidden when ``Settings.masked`` is invoked. """

    def __init__(self, obj, stars:int=10):
        """ Create a new ``Sensitive`` instance around ``obj``. You may optionally
        pass stars=(int > 0) the number of asterisks to display when
        Settings.masked is invoked (default 10). """

        self.obj = obj

        if stars <= 0:
            raise AttributeError('Stars must be greater than 0.')

        self.stars = stars

    def __str__(self):
        """ Returns the str() of the wrapped object """
        return str(self.obj)

    def __repr__(self):
        """ Returns "Sensitive: " and the repr() of the wrapped object """
        return f"Sensitive ({repr(self.obj)})"

    def mask(self):
        """ Returns the masked value of the object (a str of asterisks with 
        length equal to ``self.stars``)"""
        return "*" * self.stars
