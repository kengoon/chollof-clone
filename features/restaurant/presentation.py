__all__ = ("RestaurantScreen",)

from datetime import datetime
from os.path import join, dirname, basename

from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from features.basescreen import BaseScreen
from kivy.lang import Builder

from ui.theme import Theme

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class RestaurantList(ButtonBehavior, BoxLayout):
    cover_image = StringProperty("https://nsacc.org.ng/wp-content/uploads/2021/07/Osogbo-Nigeria.jpeg")
    business_name = StringProperty("Amen")
    starting_price = StringProperty("200")
    category = StringProperty("Chollof")
    restaurant_id = StringProperty()
    opening_time = StringProperty()
    closing_time = StringProperty()

    def on_release(self):
        return
        if self.opening_time < str(datetime.now().time()) < self.closing_time:
            self.parent.root.put_extra("restaurant_id", self.restaurant_id)
            self.parent.root.put_extra("starting_price", self.starting_price)
            self.parent.root.put_extra("business_name", self.business_name)
            self.parent.root.put_extra("cover_image", self.cover_image)
            self.parent.root.switch_screen("menu screen")
        else:
            self.parent.root.toast("Restaurant is closed for the day")


class RestaurantScreen(BaseScreen):
    pass
