username_helper = """
Screen:
    MDTextField:
        hint_text: "Enter username"
        helper_text: "or click on forgot username"
        helper_text_mode: "on_focus"
        icon_right_color: app.theme_cls.primary_color
        icon_right: "android"
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint_x: None
        width: 300
        
    MDTextField:
        hint_text: "Enter Password"
        helper_text: "or click on forgot password"
        helper_text_mode: "on_focus"
        icon_right_color: app.theme_cls.primary_color
        icon_right: "android"
        pos_hint: {'center_x':0.5,'center_y':0.5}
        size_hint_x: None
        width: 300
"""