__all__ = ("CustomLabel",)

from kivy.core.clipboard import Clipboard
from kivy.properties import BooleanProperty
from kivy.uix.label import Label
from components.behaviors import TouchBehavior, AdaptiveBehavior
from ui.theme import Theme
from kivy.lang import Builder
from os.path import join, dirname, basename

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class CustomLabel(Theme, TouchBehavior, Label, AdaptiveBehavior):
    __events__ = ("on_copy",)
    allow_copy = BooleanProperty(False)

    def on_long_touch(self, touch, *args) -> None:
        if self.allow_copy and self.collide_point(*touch.pos):
            Clipboard.copy(self.text)
            self.dispatch("on_copy")

    def on_copy(self) -> None:
        pass


class Icon(CustomLabel):
    pass
