from kivy.uix.screenmanager import Screen, ScreenManager


class CalendarPage(Screen):
    pass


class ProfilePage(Screen):
    pass


class LoginPage(Screen):
    pass


class SignUpPage(Screen):
    pass


class SignUpPage2(Screen):
    pass


class SignUpPage3(Screen):
    pass


class SettingsPage(Screen):
    pass


class Home(Screen):
    pass


class TaskScreen(Screen):
    pass


class EventScreen(Screen):
    pass


sm = ScreenManager()

sm.add_widget(LoginPage(name="LoginPage"))
sm.add_widget(SignUpPage(name="SignUpPage"))
sm.add_widget(SignUpPage2(name="SignUpPage2"))
sm.add_widget(SignUpPage3(name="SignUpPage3"))
sm.add_widget(Home(name="Home"))
sm.add_widget(CalendarPage(name="CalendarPage"))
sm.add_widget(ProfilePage(name="ProfilePage"))
sm.add_widget(SettingsPage(name="SettingsPage"))
sm.add_widget(TaskScreen(name="TaskScreen"))
sm.add_widget(EventScreen(name="EventScreen"))

