from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.uix.button import Button
from kivymd.uix.button import MDFlatButton
from kivy.uix.screenmanager import NoTransition, SlideTransition
from kivy.factory import Factory
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
from kivymd.uix.bottomsheet import MDCustomBottomSheet
import os
import sqlite3 as sql
import calendar
from datetime import timedelta
import datetime
import re

from pages import *
from kivy.core.window import Window

Window.size = (400, 650)

db = sql.connect('D:\Documents\MIU\SPSDScheduler_FYP\scheduler.db')
cur = db.cursor()

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July',
          'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"]
cur_date = datetime.datetime.now()
cur_month = cur_date.strftime("%b")
cur_year = cur_date.strftime("%Y")
cur_month_num = cur_date.month
ch_date = cur_year
stu_id = ""
stu_sem = ""

check_change_date = False


class CourseGra(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CourseCreHrs(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CurrentGp(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Content(BoxLayout):
    course_code = ObjectProperty(None)
    course_name = ObjectProperty(None)
    course_credit = ObjectProperty(None)
    global stu_sem
    global stu_id

    def course_details(self, instance):

        self.add_subject(instance)

    def add_subject(self, instance):

        if self.course_name.text != "" and self.course_code.text != "" and self.course_credit.text != "":
            insert_subject = "INSERT INTO student_subjects(sub_cou_code, sub_name, sub_cre_hrs,stu_sem, user_id) VALUES" \
                             "('" + self.course_code.text + "', '" + self.course_name.text + "', " + self.course_credit.text + " , " + stu_sem + ", " + stu_id + ")"
            cur.execute(insert_subject)
            db.commit()
            if os.path.isdir("D:\Documents\MIU\{}".format(stu_id)):
                self.create_dir(stu_id, self.course_name.text)

            else:
                os.mkdir("D:\Documents\MIU\{}".format(stu_id))
                self.create_dir(stu_id, self.course_name.text)



        if instance.text == "Add_next":
            self.course_name.text = ""
            self.course_credit.text = ""
            self.course_code.text = ""
        else:
            self.dialog.dismiss()

    def create_dir(self, s_id, course_name):
        os.mkdir("D:\Documents\MIU\{}\{}".format(s_id, course_name))
        os.mkdir("D:\Documents\MIU\{}\{}\Assignment".format(s_id, course_name))
        os.mkdir("D:\Documents\MIU\{}\{}\ClassNotes".format(s_id, course_name))
        os.mkdir("D:\Documents\MIU\{}\{}\Reference".format(s_id, course_name))


class ContentCustomSheet(BoxLayout):
    prev_b = ObjectProperty(None)
    bottom_date = ObjectProperty(None)
    next_b = ObjectProperty(None)

    def change_date_prev(self):
        global check_change_date
        global ch_date
        check_change_date = True
        ch_date = int(self.bottom_date.text) - 1
        self.bottom_date.text = str(ch_date)
        return ch_date

    def change_date_next(self):
        global check_change_date
        global ch_date
        check_change_date = True
        ch_date = int(self.bottom_date.text) + 1
        self.bottom_date.text = str(ch_date)
        return ch_date

    def date_c(self):
        if check_change_date:
            date = ch_date
        else:
            date = cur_year
        return str(date)


class Scheduler(MDApp):
    dialog = None
    dialog2 = None
    taskeve_dialog = None
    error_dialog = None
    global check_change_date

    # Button Values/Icon for Floating ActionButton
    data = {
        "Add Task": "calendar-check",
        "Add Event": "calendar-range"
    }

    # instantiate Scheduler class
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.path = "/storage/emulated/0/SPSDSchedular"
        # self.path = "D:\Documents\MIU\SPSDSchedular"

        # self.access = 0o755
        # os.mkdir(self.path, self.access)

    # build method to load kv file
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Indigo"
        self.strng = Builder.load_file("sch_kv.kv")
        return self.strng

    # check login details
    def check_login_username(self):
        self.query_select = "SELECT * from user_info"
        self.regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        self.user_email_login = self.strng.get_screen('LoginPage').ids.user_email.text
        self.user_pass_login = self.strng.get_screen('LoginPage').ids.user_pass.text
        self.strng.get_screen('LoginPage').ids.error_text.text = ""
        self.strng.get_screen('LoginPage').ids.error_text.height = "0dp"
        cur.execute(self.query_select)
        login_data = cur.fetchall()

        if self.user_email_login != '' or self.user_pass_login != '':
            if not re.search(self.regex, self.user_email_login):
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.error_dialog = MDDialog(title="Invalid Email", text="Enter valid email",
                                             size_hint=(0.7, 0.2), buttons=[close_btn])
                self.error_dialog.open()
            else:
                for user_info in login_data:
                    if user_info[2] == self.user_email_login and user_info[3] == self.user_pass_login:
                        self.strng.get_screen('Store').ids.user_id.text = str(user_info[0])
                        self.strng.get_screen('ProfilePage').ids.ch_user_name.text = str(user_info[1])
                        self.strng.get_screen('ProfilePage').ids.ch_user_email.text = str(user_info[2])
                        self.strng.get_screen('ProfilePage').ids.ch_user_pass.text = str(user_info[3])
                        self.home_view()
                        self.strng.get_screen('Home').manager.current = 'Home'
                        break

                    elif user_info[2] != self.user_email_login:
                        self.strng.get_screen('LoginPage').ids.error_text.text = "User Doesn't exist"
                        self.strng.get_screen('LoginPage').ids.error_text.height = "3dp"

                    elif not user_info[3] != self.user_pass_login:
                        self.strng.get_screen('LoginPage').ids.error_text.text = "Incorrect email or password"
                        self.strng.get_screen('LoginPage').ids.error_text.height = "3dp"

    # check signup details
    def check_signup_page(self):
        self.query_select = "SELECT * from user_info"
        self.regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        self.user_name_signup = self.strng.get_screen('SignUpPage').ids.sign_username.text
        self.user_email_signup = self.strng.get_screen('SignUpPage').ids.sign_useremail.text
        self.user_password_signup = self.strng.get_screen('SignUpPage').ids.sign_userpass.text
        self.user_conpass_signup = self.strng.get_screen('SignUpPage').ids.sign_con_userpass.text
        self.strng.get_screen('SignUpPage').ids.error_text_signup.text = ""
        self.strng.get_screen('SignUpPage').ids.error_text_signup.height = "0dp"
        cur.execute(self.query_select)
        self.signup_user_check = cur.fetchall()
        if self.user_name_signup != '' or self.user_password_signup != '' or self.user_email_signup != '' or self.user_conpass_signup != '':
            self.signup_check = True

            for user in self.signup_user_check:
                if user[2] == self.user_email_signup:
                    self.strng.get_screen('SignUpPage').ids.error_text_signup.text = "User already exits"
                    self.strng.get_screen('SignUpPage').ids.error_text_signup.height = "3dp"
                    self.signup_check = False
                    break

            if self.user_name_signup.isdigit() or ' ' in self.user_name_signup:
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.error_dialog = MDDialog(title="Invalid Username", text="Enter valid username",
                                             size_hint=(0.7, 0.2),
                                             buttons=[close_btn])
                self.error_dialog.open()
                self.signup_check = False

            elif not (re.search(self.regex, self.user_email_signup)):
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.error_dialog = MDDialog(title="Invalid Email", text="Enter valid email", size_hint=(0.7, 0.2),
                                             buttons=[close_btn])
                self.error_dialog.open()
                self.signup_check = False

            elif not len(self.user_password_signup) >= 8:
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.error_dialog = MDDialog(title="Invalid Password", text="Password should be at least 8 characters",
                                             size_hint=(0.7, 0.2), buttons=[close_btn])
                self.error_dialog.open()
                self.signup_check = False

            elif self.user_password_signup != self.user_conpass_signup:
                self.strng.get_screen('SignUpPage').ids.error_text_signup.text = "Confirmation password donot match"
                self.strng.get_screen('SignUpPage').ids.error_text_signup.height = "3dp"
                self.signup_check = False

            if self.signup_check:
                self.strng.get_screen('SignUpPage2').manager.transition = NoTransition()
                self.strng.get_screen('SignUpPage2').manager.current = 'SignUpPage2'

    # check signup details Page2
    def check_signup2(self):
        global stu_id, stu_sem
        self.student_prog = self.strng.get_screen('SignUpPage2').ids.stu_prog.text
        self.student_cgpa = self.strng.get_screen('SignUpPage2').ids.stu_cgpa.text
        self.student_semester = self.strng.get_screen('SignUpPage2').ids.stu_sem.text
        self.study_time_s = self.strng.get_screen('SignUpPage2').ids.study_time_start.text
        self.no_of_tasks = self.strng.get_screen('SignUpPage2').ids.no_of_tasks.text
        cur.execute(self.query_select)
        self.signup2_user_check = cur.fetchall()
        if self.student_prog != '' and self.student_cgpa != '' and self.student_semester != '' and self.study_time_s != '' and self.no_of_tasks != '':
            self.signup2_check = True
            try:
                # Convert it into float
                self.st = float(self.student_cgpa)
            except ValueError:
                self.signup2_check = False

            if not self.signup_check or self.st > 4.0 or self.st < 0.0:
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.error_dialog = MDDialog(title="Invalid CGPA", text="Enter valid CGPA (eg. 3.50)",
                                             size_hint=(0.7, 0.2),
                                             buttons=[close_btn])
                self.error_dialog.open()
                self.signup2_check = False

            if not self.student_semester.isdigit() or int(self.student_semester) < 0:
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.error_dialog = MDDialog(title="Invalid Semester", text="Enter valid semester",
                                             size_hint=(0.7, 0.2),
                                             buttons=[close_btn])
                self.error_dialog.open()
                self.signup2_check = False

            if self.signup2_check:
                insert_query = "INSERT INTO user_info(user_name, user_email, user_password) " \
                               "VALUES('" + self.user_name_signup + "', '" + self.user_email_signup + "', '" + self.user_password_signup + "')"
                cur.execute(insert_query)
                db.commit()
                cur.execute(self.query_select)
                user_details = cur.fetchall()
                for u_id in user_details:
                    if u_id[2] == self.user_email_signup:
                        self.id = str(u_id[0])
                        self.strng.get_screen('Store').ids.user_id.text = self.id

                insert_query2 = "INSERT INTO student_uni_info(stu_program, stu_CGPA, stu_sem, study_start, no_of_tasks, user_id) " \
                                "VALUES('" + self.student_prog + "', '" + self.student_cgpa + "', " + self.student_semester + ", '" + self.study_time_s + "', '" + self.no_of_tasks + "', " + self.id + ")"
                cur.execute(insert_query2)
                db.commit()

                self.strng.get_screen('Store').ids.user_sem.text = str(self.student_semester)
                self.strng.get_screen('ProfilePage').ids.ch_user_name.text = self.user_name_signup
                self.strng.get_screen('ProfilePage').ids.ch_user_email.text = self.user_email_signup
                self.strng.get_screen('ProfilePage').ids.ch_user_pass.text = self.user_password_signup
                stu_id = self.id
                stu_sem = self.student_semester
                self.strng.get_screen('SignUpPage2').manager.transition = NoTransition()
                self.strng.get_screen('SignUpPage3').manager.current = 'SignUpPage3'

    # close error dialog box for SignUpPage
    def close_username_dialog(self, obj):
        self.error_dialog.dismiss()

    # SignupPAge 3 add subjects
    def add_subject_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add Subject:",
                type="custom",
                size_hint_x=None,
                width="300dp",
                content_cls=Content(),

            )
        self.dialog.open()

    def close_dialog(self):
        self.dialog.dismiss()

    # Show all pending task in Home page of the User
    def home_view(self):
        self.u_id = self.strng.get_screen('Store').ids.user_id.text

        self.query_select_events = "SELECT task_name, task_type, task_due_date from students_task " \
                                   "INNER JOIN student_subjects ON student_subjects.stu_sub_id = students_task.stu_sub_id " \
                                   "where student_subjects.user_id = " + self.u_id + " ORDER BY priority ASC"
        cur.execute(self.query_select_events)
        self.strng.get_screen('Home').ids.view_all.clear_widgets()
        all_events = cur.fetchall()
        for all_eve in all_events:
            self.strng.get_screen('Home').ids.view_all.add_widget(
                ThreeLineListItem(text=all_eve[0], secondary_text=all_eve[2]))

    # Set the date for calenderPage title bar to current Date
    def calendarPage_title(self):
        global check_change_date
        self.cal_cur_title = cur_month + " " + cur_year
        check_change_date = False
        self.strng.get_screen('CalendarPage').ids.cal_tool.title = self.cal_cur_title
        self.strng.get_screen('CalendarPage').manager.current = 'CalendarPage'

    # To create calendar in Calendar Page
    def create_calendar(self, instance):
        self.date = ""
        if instance.text == "Calendar":
            self.c = calendar.monthcalendar(int(cur_year), int(cur_month_num))
        else:
            for m in months:
                if instance.text == m:
                    self.date = months.index(m) + 1
            self.c = calendar.monthcalendar(int(ch_date), self.date)
        self.strng.get_screen('CalendarPage').ids.calendar_space.clear_widgets()
        for i in self.c:
            for j in i:
                if j == 0:
                    self.strng.get_screen("CalendarPage").ids.calendar_space.add_widget(
                        Button(on_release=self.on_release,
                               text='{j}'.format(j='')))
                else:
                    self.strng.get_screen("CalendarPage").ids.calendar_space.add_widget(
                        Button(on_release=self.on_release,
                               text='{j}'.format(j=j)))

    # Go from calender page to Home Screen
    def close_page(self):
        self.strng.get_screen('Home').manager.current = "Home"

    # To open an overlay to view the events/tasks for the day
    def on_release(self, obj):
        pass

    #    if not self.dialog2:
    #        self.dialog2 = MDDialog(
    #            title="Events for the Day:",
    #            type="custom",
    #            size_hint_x=None,
    #            width="300dp",
    #            content_cls= SeeEvents(),
    #        )
    #    self.dialog2.open()
    #    SeeEvents().show_all()

    # Show bottom nav in Calendar page
    def select_calendar(self):
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.ContentCustomSheet())
        self.custom_sheet.open()

    # Change the date for calendarPage title bar after Selecting Date from bottom nav bar
    def go_back(self, instance):
        global ch_month
        global check_change_date
        ch_month = instance.text
        self.create_calendar(instance)
        self.cal_sel_title = ch_month + " " + ContentCustomSheet().bottom_date.text
        self.strng.get_screen('CalendarPage').ids.cal_tool.title = self.cal_sel_title
        self.custom_sheet.dismiss()

    # To open Floating ActionButton
    def callback(self, instance):
        if instance.icon == "calendar-check":
            self.strng.get_screen('TaskScreen').manager.transition = SlideTransition(direction="down")
            self.strng.get_screen('TaskScreen').manager.current = 'TaskScreen'
        else:
            self.strng.get_screen('EventScreen').manager.transition = SlideTransition(direction="down")
            self.strng.get_screen('EventScreen').manager.current = 'EventScreen'

    # datePicker for task/event
    def date_picker(self, instance):
        self.x = datetime.datetime.now()
        self.date_dialog = MDDatePicker(year=int(self.x.strftime("%Y")),
                                        month=int(self.x.strftime("%m")), day=int(self.x.strftime("%d")))
        if instance.icon == "calendar-month":
            self.date_dialog.bind(on_save=self.on_task_save, on_cancel=self.on_cancel)
        else:
            self.date_dialog.bind(on_save=self.on_event_save, on_cancel=self.on_cancel)
        self.date_dialog.open()

    # Selected date for task
    def on_task_save(self, instance, value, date_range):
        self.strng.get_screen('TaskScreen').ids.due_date.text = f'{value}'

    # Selected date for event
    def on_event_save(self, instance, value, date_range):
        self.strng.get_screen('EventScreen').ids.eve_date.text = f'{value}'

    # To close the calender dialog box
    def on_cancel(self, instance, value):
        self.date_dialog.dismiss()

    # dropdown menu to show subjects
    def drop_subs(self):
        self.query_select_sub = "SELECT * from student_subjects"
        cur.execute(self.query_select_sub)
        all_sub = cur.fetchall()

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "icon": "git",
                "height": dp(56),
                "text": f"{i[2]}",
                "on_release": lambda x=f"{i[2]}": self.set_item(x),
            } for i in all_sub if i[5] == int(self.strng.get_screen('Store').ids.user_id.text)]
        self.menu = MDDropdownMenu(
            caller=self.strng.get_screen('TaskScreen').ids.task_sub,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.menu.open()

    # Put selected subject in the textbox
    def set_item(self, text__item):
        self.strng.get_screen('TaskScreen').ids.task_sub.text = text__item
        self.menu.dismiss()

    # add task to the database
    def add_task(self):
        self.type_task = ""
        self.task_name = self.strng.get_screen('TaskScreen').ids.task_name.text
        if self.strng.get_screen('TaskScreen').ids.exam.state == "down":
            self.type_task = "Exam"
        else:
            self.type_task = "Assignment"
        self.due_date = self.strng.get_screen('TaskScreen').ids.due_date.text
        self.marks_per = self.strng.get_screen('TaskScreen').ids.percent.text
        self.subject = self.strng.get_screen('TaskScreen').ids.task_sub.text
        self.id = self.strng.get_screen('Store').ids.user_id.text

        if self.task_name != "" and self.type_task != "" and self.due_date != "" and self.marks_per != "" and self.subject != "":
            select_sub = "SELECT stu_sub_id, user_id FROM student_subjects where sub_name = '" + self.subject + "'"
            cur.execute(select_sub)
            sub = cur.fetchall()
            for all in sub:
                if all[1] == int(self.id):
                    self.sub_code = str(all[0])


            self.insert_task = "INSERT INTO students_task(task_type, task_name, " \
                               "task_due_date, marks_percentage,stu_sub_id) VALUES('" + self.type_task + "', '" + self.task_name + "', '" + self.due_date + "', " + self.marks_per + ", " + self.sub_code + ")"
            cur.execute(self.insert_task)
            db.commit()
            self.set_priority()
            self.home_view()
            self.strng.get_screen('Home').manager.current = 'Home'

        else:
            close_btn = MDFlatButton(text='Close', on_release=self.close_taskeve)
            self.taskeve_dialog = MDDialog(title="Empty inputs", text="All info are required", size_hint=(0.7, 0.2),
                                           buttons=[close_btn])
            self.taskeve_dialog.open()

    # add event to the database
    def add_event(self):
        self.event_name = self.strng.get_screen('EventScreen').ids.event_name.text
        self.eve_date = self.strng.get_screen('EventScreen').ids.eve_date.text
        self.eve_time_start = self.strng.get_screen('EventScreen').ids.eve_time_start.text
        self.eve_time_end = self.strng.get_screen('EventScreen').ids.eve_time_end.text
        self.id = self.strng.get_screen('Store').ids.user_id.text

        if self.event_name != "" and self.eve_date != "" and self.eve_time_start != "" and self.eve_time_end != "":
            self.insert_event = "INSERT INTO student_events(event_name, event_date, event_start_time,event_end, user_id) " \
                                "VALUES('" + self.event_name + "', '" + self.eve_date + "','" + self.eve_time_start + "', '" + self.eve_time_end + "', " + self.id + ")"
            cur.execute(self.insert_event)
            db.commit()
            self.home_view()
            self.strng.get_screen('Home').manager.current = 'Home'

        else:
            close_btn = MDFlatButton(text='Close', on_release=self.close_taskeve)
            self.taskeve_dialog = MDDialog(title="Empty inputs", text="All info are required", size_hint=(0.7, 0.2),
                                           buttons=[close_btn])
            self.taskeve_dialog.open()

    # Close error dialog box on task/eve page
    def close_taskeve(self, obj):
        self.taskeve_dialog.dismiss()

    # To pick time for Event
    def timePicker_start(self):
        self.time_dialog = MDTimePicker()
        self.time_dialog.bind(on_cancel=self.on_can, time=self.on_ok)
        self.time_dialog.open()

    # to save the time for the event
    def on_ok(self, instance, time):
        self.strng.get_screen('EventScreen').ids.eve_time_start.text = str(time)

    # To pick time for Event
    def timePicker_end(self):
        self.time_dialog = MDTimePicker()
        self.time_dialog.bind(on_cancel=self.on_can, time=self.on_okay)
        self.time_dialog.open()

    # to save the time for the event
    def on_okay(self, instance, time):
        self.strng.get_screen('EventScreen').ids.eve_time_end.text = str(time)

        # To pick time for Event

    def study_start(self):
        self.time_dialog = MDTimePicker()
        self.time_dialog.bind(on_cancel=self.on_can, time=self.on_s)
        self.time_dialog.open()

        # to save the time for the event

    def on_s(self, instance, time):
        self.strng.get_screen('SignUpPage2').ids.study_time_start.text = str(time)

        # To pick time for Event

    def study_end(self):
        self.time_dialog = MDTimePicker()
        self.time_dialog.bind(on_cancel=self.on_can, time=self.on_sa)
        self.time_dialog.open()

        # to save the time for the event

    def on_sa(self, instance, time):
        self.strng.get_screen('SignUpPage2').ids.study_time_end.text = str(time)

    # to close the time dialog box
    def on_can(self, instance, time):
        self.time_dialog.dismiss()

    def calculate_gpa(self):
        self.cre_hrs = []
        self.gra = []
        self.multi = 1
        self.sum = 0
        self.cre_hrs.append(self.strng.get_screen('CgpaPage').ids.cre_1.text)
        self.cre_hrs.append(self.strng.get_screen('CgpaPage').ids.cre_2.text)
        self.cre_hrs.append(self.strng.get_screen('CgpaPage').ids.cre_3.text)
        self.cre_hrs.append(self.strng.get_screen('CgpaPage').ids.cre_4.text)
        self.cre_hrs.append(self.strng.get_screen('CgpaPage').ids.cre_5.text)
        self.gra.append(self.ch_gra(self.strng.get_screen('CgpaPage').ids.gra_1.text))
        self.gra.append(self.ch_gra(self.strng.get_screen('CgpaPage').ids.gra_2.text))
        self.gra.append(self.ch_gra(self.strng.get_screen('CgpaPage').ids.gra_3.text))
        self.gra.append(self.ch_gra(self.strng.get_screen('CgpaPage').ids.gra_4.text))
        self.gra.append(self.ch_gra(self.strng.get_screen('CgpaPage').ids.gra_5.text))
        for (i, j) in zip(self.cre_hrs, self.gra):
            if i != "" and int(i) <= 4 and j is not None:
                self.multi += int(i) * j
                self.sum += int(i)
            elif i != "" or j is not None:
                break
            else:
                close_btn = MDFlatButton(text='Close', on_release=self.close_cgpa_dialog)
                self.err_cgpa_dialog = MDDialog(title="Invalid Credit hrs", text="Enter valid Credit hours",
                                                size_hint=(0.7, 0.2),
                                                buttons=[close_btn])
                self.err_cgpa_dialog.open()
                break

        self.result = round(self.multi / self.sum, 2)
        self.strng.get_screen('CgpaPage').ids.result.text = f"CGPA is: {self.result}"

    def close_cgpa_dialog(self, obj):
        self.err_cgpa_dialog.dismiss()

    # dropdown menu to show subjects
    def drop_gra(self, instance):
        gra_items = [
            {
                "viewclass": "OneLineListItem",
                "icon": "git",
                "height": dp(56),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_gra(x, instance),
            } for i in grades]
        self.gra_menu = MDDropdownMenu(
            caller=instance,
            items=gra_items,
            position="bottom",
            width_mult=4,
        )
        self.gra_menu.open()

    # Put selected subject in the textbox
    def set_gra(self, text__item, instance):
        instance.text = text__item
        self.gra_menu.dismiss()

    # change grades to gpa
    def ch_gra(self, grade):
        if grade == "A+" or grade == "A":
            return 4.00
        elif grade == "A-":
            return 3.67
        elif grade == "B+":
            return 3.33
        elif grade == "B":
            return 3.00
        elif grade == "B-":
            return 2.67
        elif grade == "C+":
            return 2.33
        elif grade == "C":
            return 2.00
        elif grade == "D":
            return 1.67
        elif grade == "F":
            return 0.00

    # After Logout
    def clear_all(self):
        self.strng.get_screen('LoginPage').ids.user_pass.text = ""
        self.strng.get_screen('Store').ids.user_sem.text = ""
        self.strng.get_screen('Store').ids.user_id.text = ""

    def set_priority(self):
        self.id = self.strng.get_screen('Store').ids.user_id.text
        select_state = "Select task_id, sub_cre_hrs, task_due_date, marks_percentage FROM students_task " \
                       "INNER JOIN student_subjects ON student_subjects.stu_sub_id = students_task.stu_sub_id and student_subjects.user_id=" + self.id + ""
        cur.execute(select_state)
        er = cur.fetchall()

        for i in er:
            x = i[2].split("-")
            my_datetime = datetime.datetime(int(x[0]), int(x[1]), int(x[2]))
            now = datetime.datetime.now()
            diff = now - my_datetime
            diff = diff.total_seconds()
            m, s = divmod(diff, 60)
            h, m = divmod(m, 60)
            priority = (- h + (i[1] + i[3])) / 100

            insert_state = "UPDATE students_task SET priority = " + str(priority) + " where task_id =" + str(i[0]) + ""
            cur.execute(insert_state)
            db.commit()

        self.allot_time(self.id)

    def allot_time(self, s_id):
        select_uni = "SELECT study_start, no_of_tasks FROM student_uni_info WHERE user_id =" + s_id + " "
        cur.execute(select_uni)
        task_data = cur.fetchall()
        self.study_start_time = task_data[0][0]
        self.no_of_tasks = str(task_data[0][1])
        self.data_ch = False
        select_pri = "Select task_id, priority, marks_percentage FROM students_task " \
                     "INNER JOIN student_subjects ON student_subjects.stu_sub_id = students_task.stu_sub_id and " \
                     "student_subjects.user_id="+s_id+" ORDER BY priority ASC LIMIT "+self.no_of_tasks+""
        cur.execute(select_pri)
        final = cur.fetchall()
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")

        select_all = "SELECT * from task_time_allocation"
        cur.execute(select_all)
        final2 = cur.fetchall()


        for fi in final:
            time_allot = (fi[2] / 10) * 2.0
            print(self.data_ch)
            insert_task_hrs = "INSERT INTO task_time_allocation(task_hrs, task_id) VALUES(" + str(
                time_allot) + ", " + str(fi[0]) + ")"
            print("yup")
            cur.execute(insert_task_hrs)
            db.commit()

            self.task_start = datetime.datetime.strptime(self.study_start_time, '%H:%M:%S')
            self.task_end = self.task_start + timedelta(hours=time_allot)
            self.study_start_time = datetime.datetime.strftime(self.task_end, '%H:%M:%S')

            insert_task_time = "UPDATE task_time_allocation set task_start = '"+str(self.task_start.time())+"', task_end = '"+str(self.task_end.time())+"' where task_id = "+str(fi[0])+""
            print(insert_task_time)
            cur.execute(insert_task_time)
            db.commit()









Scheduler().run()
