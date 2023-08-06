"""Interact with the graphics libraries via window events.

There are three types of window events to which a caller can subscribe:

- WindowResized: The graphical window was resized.
- WindowMoved: The graphical window was moved (only valid on some platforms).
- WindowClosed: The graphical window was closed.

In order to subscribe to WindowResized or WindowMoved, a client should call
`onwindowXXX`, supplying a callable that takes one argument - a WindowEvent
representing the updated window location and size::

    def show_resize(event):
        print('New width: {}px'.format(event.width))
        print('New height: {}px'.format(event.height))

    onwindowresized(show_resize)

These functions can also be used as decorators::


"""
import campy.private.platform as _platform

class GWindowEvent:
    # TODO(sredmond): Rewrite this as a namedtuple or a dataclass.
    def __init__(self, gwindow, x, y, width, height):
        """Construct a"""
        self._gwindow = gwindow
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def window(self):
        return self._gwindow

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __str__(self):
        return "GWindowEvent(x={}, y={}, width={}, height={})".format(self.x, self.y, self.width, self.height)

@curryable
def onwindowresized(function, add=False, window=None):
    _platform.Platform().event_add_window_changed_handler(function)


def onwindowmoved(function):
    pass

def onwindowclosed(function):
    """
    If it returns a False-y value, the default action is taken.
    If it returns a Truth-y value, the default action is skipped.

    Note that this is OPPOSITE how Javascript does things.

    There can be only one window closed handler per window.
    """
    _platform.Platform().event_set_window_closed_handler(function)

