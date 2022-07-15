from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivymd.toast import toast
from libs.screens.root import Root

def emulate_android_device(pixels_horizontal = 1080, pixels_vertical = 2240, android_dpi = 394, monitor_dpi = 157):
    scale_factor = monitor_dpi / android_dpi
    Window.size = (scale_factor * pixels_horizontal, scale_factor * pixels_vertical)

if platform != "android":
    emulate_android_device()
    LIVE_UI = 0
else:
    LIVE_UI = 0

Window.softinput_mode = "below_target"

KV = """
#: import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer
HotReloadViewer:
    path: app.PATH
    
"""


class MyApp(MDApp):
    PATH = "main.kv"
    user_name = StringProperty()
    user_mail = StringProperty()

    def build(self):
        Builder.load_file("libs/classes.kv")
        self.root = Root()
        self.theme_cls.primary_palette = "Red"
        self.root.set_current("OnBoarding")
        if platform == "android":
            initialize_google(self.successful_login, self.error_listener)
        # if LIVE_UI:
        #     return Builder.load_string(KV)

    def on_stop(self):
        ...
        # self.root.ids.box.export_to_png("assets/gradient.png")
        # self.root.ids.on_boarding_2.export_to_png("screenshots/on_boarding_2.png")
        # self.root.ids.on_boarding_3.export_to_png("screenshots/on_boarding_3.png")
        # self.root.ids.register_screen.export_to_png("screenshots/Signup.png")

    def login(self):
        """
        Login with Google
        """
        if platform == "android":
            login_google()
        else:
            self.successful_login("demo_name", "demo_email", "demo_photo_uri")

    def successful_login(self, name, email, photo_uri):
        toast(f"Logged in {name} with email {email}")
        self.user_name = name
        self.user_mail = email
        self.root.set_current("CreateAccount")

    def error_listener(self):
        toast("Some error occured.")


if __name__ == "__main__":
    MyApp().run()
