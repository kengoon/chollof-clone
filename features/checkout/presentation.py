__all__ = ("CheckoutScreen",)

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from os.path import join, dirname, basename

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class CheckoutScreen(Screen):
    pass