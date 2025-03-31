"""
This module defines a decorator that assigns window properties (name, title, geometry, icon)
to a class.
"""

from PyQt5.QtGui import QIcon

def Window(
        name: str, 
        title: str, 
        geometry: list, 
        icon: QIcon, 
        resizable: bool = True
    ):
    """
    A decorator that assigns window properties (name, title, geometry) to a class.

    This decorator allows you to configure the title, geometry, and icon of a 
    window for a given class.

    Args:
        name (str): The name of the window.
        title (str): The title of the window.
        geometry (list): The geometry of the window (ax: int, ay: int, aw: int, ah: int).
        icon (QIcon): The icon of the window.
        resizable (bool, optional): The ability to resize the window. Defaults to True.
    
    Returns:
        function: A decorator that adds the window properties to the class.
    """
    def decorator(cls):
        """
        A decorator that assigns window properties.

        Args:
            cls (type): The class to be decorated.

        Returns:
            type: The decorated class with window properties.
        """
        originalInit = cls.__init__

        def newInit(self, *args, **kwargs):
            """
            Initializes the decorated class with window settings.

            Args:
                *args: Positional arguments passed to the original class initializer.
                **kwargs: Keyword arguments passed to the original class initializer.
            """
            originalInit(self, *args, **kwargs)

            # Assign window properties
            self.name = name
            self.title = title
            self.windowGeometry = geometry
            self.windowParent = None

            self.setWindowTitle(self.title)
            self.setGeometry(*self.windowGeometry)

            if not resizable:
                ah, aw = geometry[-2:]
                self.setFixedSize(ah, aw)

            self.setWindowIcon(icon)

        cls.__init__ = newInit

        cls.title = title

        return cls

    return decorator
