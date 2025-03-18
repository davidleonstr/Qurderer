"""
This module defines a decorator used to add a `name` attribute to screen classes.

The `Screen` decorator is used to assign a unique name to a screen class. This name can 
be accessed through the `name` attribute of the decorated screen class. It also adds a 
`screenName` class-level attribute to the decorated class.

Functions provided:
    - Screen: A decorator that assigns a `name` attribute to a class.
"""

def Screen(name: str):
    """
    A decorator that adds a `name` attribute to a screen class.

    This decorator assigns a unique `name` to a screen class. The `name` is set as 
    both an instance attribute (`self.name`) and a class-level attribute (`screenName`).

    Args:
        name (str): The name to assign to the screen class.

    Returns:
        decorator: A class decorator that adds the `name` attribute to the class.
    """

    def decorator(cls):
        """
        Decorates a class to add a `name` attribute.

        Args:
            cls: The class to decorate.

        Returns:
            cls: The decorated class with a `name` attribute.
        """
        originalInit = cls.__init__

        def newInit(self, *args, **kwargs):
            """
            Initializes the decorated class and assigns the `name` attribute.

            Args:
                *args: Positional arguments passed to the original class initializer.
                **kwargs: Keyword arguments passed to the original class initializer.
            """
            self.name = name
            originalInit(self, *args, **kwargs)

        cls.__init__ = newInit
        cls.screenName = name

        return cls
    
    return decorator
