"""
This module defines a decorator that assigns window properties (name, title, geometry, and icon)
to a class, with optional support for managing multiple screens.

The `Window` decorator allows configuring window attributes and supports screen management through
the use of a stacked widget. It also provides functionality to switch between screens and track the 
history of screens visited.

Functions:
    - Window: A decorator to add window properties and manage screens for a class.
"""

from PyQt5.QtGui import QIcon

def Window(name: str, title: str, geometry: list, icon: QIcon = QIcon()):
    """
    A decorator that assigns window properties (name, title, geometry) to a class,
    with optional support for managing multiple screens.

    This decorator allows you to configure the title, geometry, and icon of a 
    window for a given class. It also supports additional functionality such as 
    managing multiple screens, if required.

    Args:
        name (str): The name of the window.
        title (str): The title of the window.
        geometry (list): The geometry of the window (usually a list with width and height).
        icon (QIcon, optional): The icon of the window (default is an empty QIcon).
    
    Returns:
        function: A decorator that adds the window properties to the class and 
                  optionally manages screens.
    """
    def decorator(cls):
        """
        A decorator that assigns window properties and optionally manages screens for the class.

        Args:
            cls (type): The class to be decorated.

        Returns:
            type: The decorated class with window properties and screen management functionality.
        """
        originalInit = cls.__init__

        def newInit(self, *args, **kwargs):
            """
            Initializes the decorated class with window settings and optional screen management.

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
            self.setWindowIcon(icon)

        cls.__init__ = newInit

        return cls

    return decorator
