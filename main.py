from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivy.properties import BooleanProperty
import sqlite3 as sql
from kivy.clock import Clock
from functools import partial
from pages import *
from kivy.config import Config
from kivy.core.window import Window
Window.size = (450, 680)


db = sql.connect('D:\Documents\MIU\SPSDScheduler_FYP\scheduler.db')
cur = db.cursor()

query_select = "SELECT * from user_info"




class MyMDTextField(MDTextField):
    password_mode = BooleanProperty(True)


class Scheduler(MDApp):
    dialog = None
    def build(self):
        self.strng = Builder.load_file("sch_kv.kv")
        return self.strng

    def check_login_username(self):
        self.user_name_login = self.strng.get_screen('LoginPage').ids.user_name.text
        self.user_pass_login = self.strng.get_screen('LoginPage').ids.user_pass.text
        cur.execute(query_select)
        login_data = cur.fetchall()

        if self.user_name_login != '' or self.user_pass_login != '':
            print("hi")
            if self.user_name_login.isdigit() or ' ' in self.user_name_login:
                self.strng.get_screen('LoginPage').ids.user_name.helper_text = "Invalid Username"
                self.strng.get_screen('LoginPage').ids.user_name.error = True

            else:
                for user_info in login_data:
                    if user_info[1] == self.user_name_login and user_info[3] == self.user_pass_login:
                        self.strng.get_screen('Home').manager.current = 'Home'
                        break

                    if not user_info[1] == self.user_name_login or not user_info[3] == self.user_pass_login:
                        self.strng.get_screen('LoginPage').ids.error_text.text = "Incorrect Username or Password"
                        self.strng.get_screen('LoginPage').ids.error_text.height = "3dp"
                        break



    def calendarPicker(self):
        date_dialog = MDDatePicker(callback=self.got_date)
        date_dialog.open()

    def got_date(self, the_date):
        print(the_date)


Scheduler().run()
