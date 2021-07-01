from kivy.uix.screenmanager import Screen, ScreenManager


class LoginPage(Screen):
    pass


class SignUpPage(Screen):
    pass


class SignUpPage2(Screen):
    pass


class SignUpPage3(Screen):
    pass


class Home(Screen):
    pass


class CalendarPage(Screen):
    pass


class ProfilePage(Screen):
    pass


class TaskScreen(Screen):
    pass


class EventScreen(Screen):
    pass


class CgpaPage(Screen):
    pass


class DetailsPage(Screen):
    pass


class AllTasksPage(Screen):
    pass


class Store(Screen):
    pass


# Create screen Manager object
sm = ScreenManager()
# Add page to screen manager
sm.add_widget(LoginPage(name="LoginPage"))
sm.add_widget(SignUpPage(name="SignUpPage"))
sm.add_widget(SignUpPage2(name="SignUpPage2"))
sm.add_widget(SignUpPage3(name="SignUpPage3"))
sm.add_widget(Home(name="Home"))
sm.add_widget(CalendarPage(name="CalendarPage"))
sm.add_widget(ProfilePage(name="ProfilePage"))
sm.add_widget(TaskScreen(name="TaskScreen"))
sm.add_widget(EventScreen(name="EventScreen"))
sm.add_widget(CgpaPage(name="CgpaPage"))
sm.add_widget(DetailsPage(name="DetailsPage"))
sm.add_widget(AllTasksPage(name="AllTasksPage"))
sm.add_widget(Store(name="Store"))
