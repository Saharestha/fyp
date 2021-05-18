from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from helpers import username_helper


class Scheduler(MDApp):
    def build(self):

        layout1 = MDBoxLayout(orientation='vertical', padding=100)
        self.theme_cls.theme_style= "Dark"
        self.theme_cls.primary_palette="Blue"

        button = MDRectangleFlatButton(text='Show', pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                       on_release=self.show_data)
        self.username = Builder.load_string(username_helper)

        layout1.add_widget(self.username)

        layout1.add_widget(button)



    def show_data(self, obj):
        if self.username.text is "":
            check = "Please enter username"
        else:
            check = self.username.text + ' does not exist'
        close_btn = MDFlatButton(text='close', on_release=self.close_dialog)
        more_btn = MDFlatButton(text='more')
        self.dialog = MDDialog(title='Username', text=check,
                            size_hint=(0.5, 0.5), buttons={close_btn, more_btn})

        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()


Scheduler().run()

