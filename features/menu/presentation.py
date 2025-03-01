__all__ = ("MenuScreen",)
from os.path import join, dirname, basename
import asynckivy as ak
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, BoundedNumericProperty
from kivy.uix.behaviors import TouchRippleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from features.basescreen import BaseScreen

from components.behaviors import AdaptiveBehavior
from components.scrim import DialogScrim
from libs import shorten_text
from sjfirebase.tools.mixin import FirestoreMixin

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class MenuList(RecycleDataViewBehavior, TouchRippleButtonBehavior, BoxLayout):
    price = NumericProperty()
    meal = StringProperty()
    meal_description = StringProperty()
    image = StringProperty()
    content_text = StringProperty()
    data = None

    def refresh_view_attrs(self, rv, index, data):
        self.data = data
        self.data = dict(price=self.price, meal=self.meal, meal_description=self.meal_description, price_description="Best price you can get", pack=200, image=self.image, content_text=self.content_text)
        super().refresh_view_attrs(rv, index, data)

    def on_release(self, *args) -> None:
        self.parent.root.open_sheet(self.data)

    def shorten_text(self):
        if not self.meal_description:
            return
        self.content_text = shorten_text(
            self.meal_description,
            self.ids.content.width,
            lines=2,
            suffix="...",
            font_size=self.ids.content.font_size
        )


class ExtraList(BoxLayout, AdaptiveBehavior):
    name = StringProperty("Meat")
    active = BooleanProperty(False)
    price = NumericProperty(200)
    increment = BooleanProperty()
    quantity = BoundedNumericProperty(1, min=1, max=5, errorhandler=lambda x: 5 if x > 5 else 1)


class MenuScreen(BaseScreen, FirestoreMixin):
    is_sheet_open = BooleanProperty(False)
    meal_id = StringProperty()
    restaurant_id = StringProperty()

    def on_enter(self, *args):
        self.ids.cover_image.source = self.get_extra("cover_image")
        self.restaurant_id = self.get_extra("document_id")
        self.ids.business_name.text = self.get_extra("business_name")
        self.ids.starting_price.text = str(self.get_extra("starting_price"))
        if not self.ids.rv.data:
            self.get_pagination_of_documents(
                f"vendor/RMol1naULxRQl40TRXuy7q37yJ12/menu",
                25,
                lambda _, data: setattr(self.ids.rv, "data", data)
            )

    def open_sheet(self, data):
        if self.is_sheet_open:
            return
        self.is_sheet_open = True
        self.add_widget(DialogScrim(), index=1)
        Animation(y=0, d=.2).start(self.ids.bottom_sheet)
        self.add_meal(data)
        # self.meal_id = data["meal_id"]

    def add_meal(self, data):
        self.ids.meal.text = data["meal"]
        self.ids.meal_description.text = \
            f"{data['meal_description']}. {data['price_description']}"
        self.ids.price.price = data["price"]
        self.ids.price.pack = data["pack"]
        self.ids.btn.total_price = data["price"] + data["pack"]
        self.ids.meal_image.source = data["image"]
        # ak.start(self.add_extras(data["extras"]))
        ak.start(self.add_extras(None))

    async def add_extras(self, data):
        # for extra in data:
        #     await ak.sleep(0)
        #     extra_widget = ExtraList(
        #         name=extra["name"],
        #         price=extra["price"],
        #     )
        #     extra_widget.bind(
        #         quantity=self.change_extra_price,
        #         active=self.update_extras_price
        #     )
        #     self.ids.extra_container.add_widget(extra_widget)
        await ak.sleep(0)
        self.ids.extra_container.add_widget(ExtraList())

    def close_sheet(self):
        self.is_sheet_open = False
        Animation(y=-self.height - dp(100), d=.2).start(self.ids.bottom_sheet)
        self.remove_widget(self.children[1])
        self.clear_meal()

    def clear_meal(self):
        self.ids.meal.text = ""
        self.ids.meal_description.text = ""
        self.ids.price.pack = 0
        self.ids.meal_image.source = ""
        self.ids.price.price = 0
        self.ids.btn.total_price = 0
        self.ids.extra_container.clear_widgets()

    def move_eb(self):
        eb = self.ids.eb
        cover_image = self.ids.cover_image
        empty = self.ids.empty
        scroll_distance_traveled = self.ids.rv.scroll_distance_traveled
        bar_title = self.ids.bar_title

        # set the bar_title title
        if (eb.y + eb.height - bar_title.height) >= bar_title.y:
            self.ids.bar_title.opacity = 1
        else:
            self.ids.bar_title.opacity = 0

        # move eb widget
        if eb.y >= self.height and scroll_distance_traveled[1] >= cover_image.height:
            # if eb.y == 0:
            #     return
            eb.y = self.height
        else:
            eb.y = eb.y_ + scroll_distance_traveled[1]

        # move empty widget
        if empty.y >= 0 and scroll_distance_traveled[1] >= cover_image.height:
            if eb.y == 0:
                return
            empty.y = 0
        else:
            empty.y = empty.y_ + scroll_distance_traveled[1]
