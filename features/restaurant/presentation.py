__all__ = ("HomeScreen",)

from os.path import join, dirname, basename
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class HomeScreen(Screen):
    pass
