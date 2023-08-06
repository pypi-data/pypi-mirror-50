"""
``serve()`` call this function to start the server.

``@route()`` use this decorator to define the route, pass path as argument

``Response()`` return this function with arguments, the arguments can be JSON type or String.
"""

from .sidanwebframework import serve, Response, route, Render

name = 'sidanwebframework'

__all__ = [
    'serve', 'Response', 'route', 'Render'
]