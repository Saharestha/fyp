from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.picker import MDDatePicker
from kivy.uix.screenmanager import Screen, ScreenManager

class LoginPage(Screen):
    pass

class CalendarPage(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class Scheduler(MDApp):
    def build(self):
        self.theme_cls.colors = ""
        self.theme_cls.primary_palette = "Red"
        return Builder.load_file('scheduler.kv')

    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)

    def on_cancel(self, instance, value):
        pass


    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def get_date(self, the_date):
        print(the_date)

Scheduler().run()
