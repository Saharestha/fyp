from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.textfield import MDTextField
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivymd.uix.button import MDFlatButton
from kivy.factory import Factory
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
from kivymd.uix.bottomsheet import MDCustomBottomSheet
import sqlite3 as sql
import calendar
import datetime
import re
from pages import *
from kivy.core.window import Window
Window.size = (450, 680)


db = sql.connect('D:\Documents\MIU\SPSDScheduler_FYP\scheduler.db')
cur = db.cursor()
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July',
                  'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
query_select = "SELECT * from user_info"
query_select_info = "SELECT * from student_uni_info"

cur_date = datetime.datetime.now()
cur_month = cur_date.strftime("%b")
cur_year = cur_date.strftime("%Y")
cur_month_num = cur_date.month
check_change_date = False
ch_date = ""
ch_month = ""
stu_id = ""
user_name_signup = ""
no_subjects = ""
course_code_ = ""
course_name_ = ""
course_credit_ = ""
student_semester = ""


class MyMDTextField(MDTextField):
    password_mode = BooleanProperty(True)


class Content(BoxLayout):
    course_code = ObjectProperty(None)
    course_name = ObjectProperty(None)
    course_credit = ObjectProperty(None)

    def course_details(self, instance):
        global course_code_, course_credit_, course_name_
        course_name_ = self.course_name.text
        course_code_ = self.course_code.text
        course_credit_ = self.course_credit.text
        self.add_subject(instance)

    def add_subject(self, instance):

        insert_subject = "INSERT INTO student_subjects(sub_cou_code, sub_name, sub_cre_hrs," \
                         "stu_sem, user_id) VALUES" \
                         "('"+course_code_+"', '" + course_name_+"','"+course_credit_+"','"+student_semester+"','"+stu_id+"')"
        cur.execute(insert_subject)
        db.commit()
        if instance.text == "Add_next":
            self.course_name.text = ""
            self.course_credit.text = ""
            self.course_code.text = ""







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




class Dates(GridLayout):
    now = datetime.datetime.now()

    def __init__(self, **kwargs):
        super(Dates, self).__init__(**kwargs)
        self.cols = 7
        self.c = calendar.monthcalendar(int(cur_year), int(cur_month_num))
        for i in self.c:
            for j in i:
                if j == 0:
                    self.add_widget(Button(on_release=self.on_release, text='{j}'.format(j='')))
                else:
                    self.add_widget(Button(on_release=self.on_release, text='{j}'.format(j=j)))

    def on_release(self, instance):
        print(instance.text)
        print("Presses")



class Scheduler(MDApp):
    dialog = None
    global check_change_date

    def build(self):
        self.strng = Builder.load_file("sch_kv.kv")
        return self.strng

    def check_login_username(self):
        self.user_name_login = self.strng.get_screen('LoginPage').ids.user_name.text
        self.user_pass_login = self.strng.get_screen('LoginPage').ids.user_pass.text
        cur.execute(query_select)
        login_data = cur.fetchall()

        if self.user_name_login != '' or self.user_pass_login != '':
            if self.user_name_login.isdigit() or ' ' in self.user_name_login or len(self.user_name_login) < 3:
                close_btn = MDFlatButton(text='Close', on_release = self.close_username_dialog)
                self.dialog = MDDialog(title="Invalid Username", text="Enter valid username",
                                       size_hint=(0.7, 0.2), buttons=[close_btn])
                self.dialog.open()
            else:
                for user_info in login_data:
                    if user_info[1] == self.user_name_login and user_info[3] == self.user_pass_login:
                        self.strng.get_screen('Home').manager.current = 'Home'
                        break

                    if not user_info[1] == self.user_name_login:
                        self.strng.get_screen('LoginPage').ids.error_text.text = "User Doesn't exist"
                        self.strng.get_screen('LoginPage').ids.error_text.height = "3dp"
                        break

                    elif not user_info[3] == self.user_pass_login:
                        self.strng.get_screen('LoginPage').ids.error_text.text = "Incorrect email or password"
                        self.strng.get_screen('LoginPage').ids.error_text.height = "3dp"
                        break


    def check_signup_page(self):
        global user_name_signup
        user_name_signup = self.strng.get_screen('SignUpPage').ids.sign_username.text
        self.user_email_signup = self.strng.get_screen('SignUpPage').ids.sign_useremail.text
        self.user_password_signup = self.strng.get_screen('SignUpPage').ids.sign_userpass.text
        self.user_conpass_signup = self.strng.get_screen('SignUpPage').ids.sign_con_userpass.text
        cur.execute(query_select)
        self.signup_user_check = cur.fetchall()
        if user_name_signup != '' or self.user_password_signup != '' or self.user_email_signup != '' or self.user_conpass_signup != '':
            self.signup_check = True

            for user in self.signup_user_check:
                if user[1] == user_name_signup or user[2] == self.user_email_signup:
                    self.strng.get_screen('SignUpPage').ids.error_text_signup.text = "User already exits"
                    self.strng.get_screen('SignUpPage').ids.error_text_signup.height = "3dp"
                    self.signup_check = False
                    break


            if user_name_signup.isdigit() or ' ' in user_name_signup:
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title="Invalid Username", text="Enter valid username", size_hint=(0.7, 0.2),
                                       buttons=[close_btn])
                self.dialog.open()
                self.signup_check = False

            elif not (re.search(regex, self.user_email_signup)):
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title="Invalid Email", text="Enter valid email", size_hint=(0.7, 0.2),
                                       buttons=[close_btn])
                self.dialog.open()
                self.signup_check = False

            elif not len(self.user_password_signup) >= 8:
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title="Invalid Password", text="Password should be at least 8 characters", size_hint=(0.7, 0.2),
                                       buttons=[close_btn])
                self.dialog.open()
                self.signup_check = False

            elif self.user_password_signup != self.user_conpass_signup:
                self.strng.get_screen('SignUpPage').ids.error_text_signup.text = "Confirmation password donot match"
                self.strng.get_screen('SignUpPage').ids.error_text_signup.height = "3dp"
                self.signup_check = False

            if self.signup_check:
                insert_user_sql = "INSERT INTO user_info(user_name, user_email, user_password) VALUES ('" + user_name_signup + "', '" + self.user_email_signup + "', '" + self.user_password_signup + "')"
                cur.execute(insert_user_sql)
                print("okay")
                db.commit()
                self.strng.get_screen('SignUpPage2').ids.pass_id.text = user_name_signup
                self.strng.get_screen('SignUpPage2').manager.current = 'SignUpPage2'



    def check_signup2(self):
        global student_semester
        self.student_prog = self.strng.get_screen('SignUpPage2').ids.stu_prog.text
        self.student_cgpa = self.strng.get_screen('SignUpPage2').ids.stu_cgpa.text
        student_semester = self.strng.get_screen('SignUpPage2').ids.stu_sem.text
        self.student_subject = self.strng.get_screen('SignUpPage2').ids.stu_subs.text
        cur.execute(query_select)
        self.signup2_user_check = cur.fetchall()
        if self.student_prog != '' or self.student_cgpa != '' or student_semester != '' or self.student_subject != '':
            self.signup2_check = True
            try:
                # Convert it into float
                self.st = float(self.student_cgpa)
            except ValueError:
                self.signup2_check = False

            if not self.signup_check or self.st > 4 or self.st < 0:
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title="Invalid CGPA", text="Enter valid CGPA (eg. 3.50)", size_hint=(0.7, 0.2),
                                       buttons=[close_btn])
                self.dialog.open()
                self.signup2_check = False

            if not student_semester.isdigit() or int(student_semester) < 0:
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title="Invalid Semester", text="Enter valid semester", size_hint=(0.7, 0.2),
                                       buttons=[close_btn])
                self.dialog.open()
                self.signup2_check = False



            elif not self.student_subject.isdigit() or int(self.student_subject) < 0:
                close_btn = MDFlatButton(text='Close', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title="Invalid number of Subjects", text="Enter valid number", size_hint=(0.7, 0.2),
                                       buttons=[close_btn])
                self.dialog.open()
                self.signup2_check = False

            if self.signup2_check:

                global no_subjects, stu_id
                no_subjects = int(self.student_subject)
                print(user_name_signup)
                for user in self.signup2_user_check:
                    if user[1] == user_name_signup:
                        stu_id = str(user[0])
                        break
                insert_user_sql = "INSERT INTO student_uni_info(stu_program, stu_CGPA, stu_sem, stu_no_subjects, user_id) VALUES('" + self.student_prog + "'," + self.student_cgpa + ", " + student_semester + "," + self.student_subject + "," + stu_id + ")"
                cur.execute(insert_user_sql)
                db.commit()
                self.strng.get_screen('SignUpPage3').manager.current = 'SignUpPage3'

    def close_username_dialog(self, obj):
        self.dialog.dismiss()

    def close_page(self):
        self.strng.get_screen('Home').manager.current = "Home"

    def calendarPage_title(self):
        global check_change_date
        self.cal_cur_title = cur_month + " " + cur_year
        check_change_date = False
        self.strng.get_screen('CalendarPage').ids.cal_tool.title = self.cal_cur_title
        self.strng.get_screen('CalendarPage').manager.current = 'CalendarPage'


    def go_back(self, instance):
        global ch_month
        global check_change_date
        ch_month = instance.text
        self.cal_sel_title = ch_month + " " + ContentCustomSheet().bottom_date.text
        self.strng.get_screen('CalendarPage').ids.cal_tool.title = self.cal_sel_title
        self.custom_sheet.dismiss()
        #self.strng.get_screen('CalendarPage').manager.current = 'CalendarPage'

    def show_example_custom_bottom_sheet(self):
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.ContentCustomSheet())
        self.custom_sheet.open()


    def calendarPicker(self):
        date_dialog = MDDatePicker(callback=self.got_date)
        date_dialog.open()

    def got_date(self, the_date):
        print(the_date)





    def add_subject_dialog(self):

        if not self.dialog:
            self.dialog = MDDialog(
                title="Add Subject:",
                type="custom",
                size_hint_x= None,
                width="300dp",
                content_cls=Content(),

            )
        self.dialog.open()

    def close_dialog(self):
        self.dialog.dismiss()


Scheduler().run()
