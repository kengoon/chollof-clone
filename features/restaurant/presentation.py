__all__ = ("RestaurantScreen",)

from datetime import datetime
from os.path import join, dirname, basename

from kivy.clock import mainthread
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.behaviors import TouchRippleButtonBehavior
from kivy.uix.boxlayout import BoxLayout

from components.bar import win_md_bnb
from features.basescreen import BaseScreen
from kivy.lang import Builder
from sjfirebase.tools.mixin import FirestoreMixin

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class RestaurantList(TouchRippleButtonBehavior, BoxLayout):
    cover_image = StringProperty()
    business_name = StringProperty()
    starting_price = NumericProperty()
    category = StringProperty("Chollof")
    document_id = StringProperty()
    opening_time = StringProperty()
    closing_time = StringProperty()

    def on_release(self):
        if self.opening_time < str(datetime.now().time()) < self.closing_time:
            self.parent.root.put_extra("document_id", self.document_id)
            self.parent.root.put_extra("starting_price", self.starting_price)
            self.parent.root.put_extra("business_name", self.business_name)
            self.parent.root.put_extra("cover_image", self.cover_image)
            self.parent.root.manager.current = "menu screen"
        else:
            self.parent.root.toast("Restaurant is closed for the day")


class RestaurantScreen(BaseScreen, FirestoreMixin):
    @mainthread
    def on_enter(self, *args):
        win_md_bnb.push()
        if not self.ids.rv.data:
            self.get_pagination_of_documents(
                "vendor/RMol1naULxRQl40TRXuy7q37yJ12/details",
                25,
                lambda _, data: (setattr(self.ids.rv, "data", data), print(data))
            )
