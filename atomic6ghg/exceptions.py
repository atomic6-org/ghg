""" Custom exceptions """


class YearMapException(Exception):
    """ This exception is raised if a year can't be mapped to factors """


class YearValueException(Exception):
    """ This exception is raised if a year cannot be typed as an int """
