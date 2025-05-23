"""
Behaviors/Touch
===============

.. rubric:: Provides easy access to events.

The following events are available:

- on_long_touch
- on_double_tap
- on_triple_tap

Usage
-----

.. code-block:: python

    from kivy.lang import Builder
    from kivy.properties import StringProperty

    from kivymd.app import MDApp
    from kivymd.uix.behaviors import TouchBehavior
    from kivymd.uix.button import MDButton

    KV = '''
    <TouchBehaviorButton>
        style: "elevated"

        MDButtonText:
            text: root.text


    MDScreen:
        bg_color: self.theme_cls.backgroundColor

        TouchBehaviorButton:
            text: "TouchBehavior"
            pos_hint: {"center_x": .5, "center_y": .5}
    '''


    class TouchBehaviorButton(MDButton, TouchBehavior):
        text = StringProperty()

        def on_long_touch(self, *args):
            print("<on_long_touch> event")

        def on_double_tap(self, *args):
            print("<on_double_tap> event")

        def on_triple_tap(self, *args):
            print("<on_triple_tap> event")


    class Example(MDApp):
        def build(self):
            return Builder.load_string(KV)


    Example().run()
"""

__all__ = ("TouchBehavior",)

from functools import partial

from kivy.clock import Clock
from kivy.properties import NumericProperty


class TouchBehavior:
    duration_long_touch = NumericProperty(0.4)
    """
    Time for a long touch.

    :attr:`duration_long_touch` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0.4`.
    """

    def __init__(self, *args, **kwargs):
        self.register_event_type('on_double_tap')
        self.register_event_type('on_triple_tap')
        self.register_event_type('on_long_touch')
        super().__init__(*args, **kwargs)
        self.bind(
            on_touch_down=self.create_clock, on_touch_up=self.delete_clock
        )

    def create_clock(self, _, touch, *args):
        if self.collide_point(touch.x, touch.y):
            if self not in touch.ud:
                callback = lambda x=touch: self.dispatch('on_long_touch', x)
                Clock.schedule_once(callback, self.duration_long_touch)
                touch.ud[self] = callback

        if touch.is_double_tap:
            self.dispatch("on_double_tap", touch, *args)
        if touch.is_triple_tap:
            self.dispatch("on_triple_tap", touch, *args)

    def delete_clock(self, widget, touch, *args):
        """Removes a key event from `touch.ud`."""

        if self.collide_point(touch.x, touch.y):
            if self in touch.ud:
                Clock.unschedule(touch.ud[self])
                del touch.ud[self]

    def on_long_touch(self, touch, *args):
        """Fired when the widget is pressed for a long time."""

    def on_double_tap(self, touch, *args):
        """Fired by double-clicking on the widget."""

    def on_triple_tap(self, touch, *args):
        """Fired by triple clicking on the widget."""
