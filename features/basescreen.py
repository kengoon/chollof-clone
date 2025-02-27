from kivy.clock import mainthread
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


class BaseScreen(Screen):
    data_source = ObjectProperty(None)

    @mainthread
    def toast(self, text, length_long=True):
        from kvdroid.tools import toast
        toast(text, length_long)
