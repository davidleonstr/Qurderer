"""
This module defines a simple in-memory session storage class and a decorator to inject
this session storage into a class.

The `SessionStorage` class provides methods for storing, retrieving, and removing 
items from a session. The `useSessionStorage` decorator adds a `sessionStorage` 
attribute to a class, which allows easy access to the session storage.
"""

from dataclasses import dataclass

@dataclass
class SessionStorage:
    """
    A class that simulates session storage in memory.

    This class provides methods for storing, retrieving, and removing key-value pairs
    in memory, which mimics a session storage mechanism.

    Attributes:
        _storage (dict): A dictionary to store session data.
    """
    
    _storage = {}

    def getItem(self, item: str):
        """
        Retrieves an item from the session storage.

        Args:
            item (str): The key of the item to retrieve.

        Returns:
            The value associated with the provided key, or None if the key does not exist.
        """
        return self._storage.get(item)

    def setItem(self, name: str, value) -> None:
        """
        Adds or updates an item in the session storage.

        Args:
            name (str): The key to store the item under.
            value: The value to associate with the given key.
        """
        self._storage[name] = value
    
    def removeItem(self, item: str) -> None:
        """
        Removes an item from the session storage.

        Args:
            item (str): The key of the item to remove.
        """
        self._storage.pop(item, None)

# Create a global sessionStorage instance
sessionStorage = SessionStorage()

def useSessionStorage():
    """
    A decorator that injects session storage into a class.

    This decorator adds a `sessionStorage` attribute to the class, making it 
    accessible from instances of the class.

    Returns:
        decorator: A class decorator that adds the `sessionStorage` attribute.
    """

    def decorator(cls):
        """
        Decorates a class to inject session storage.

        Args:
            cls: The class to decorate.

        Returns:
            cls: The decorated class with the `sessionStorage` attribute.
        """
        originalInit = cls.__init__

        def newInit(self, *args, **kwargs):
            """
            Initializes the decorated class and adds session storage.

            Args:
                *args: Positional arguments passed to the original class initializer.
                **kwargs: Keyword arguments passed to the original class initializer.
            """
            originalInit(self, *args, **kwargs)
            self.sessionStorage = sessionStorage

        cls.__init__ = newInit

        cls.sessionStorage = sessionStorage

        return cls
    
    return decorator
