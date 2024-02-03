from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        layout.add_widget(Label(text="Login Screen"))
        layout.add_widget(Button(text="Login", on_press=self.login))
        layout.add_widget(Button(text="Signup", on_press=self.signup))

    def login(self, instance):
        # Here you would implement the login functionality
        print("Login clicked")

    def signup(self, instance):
        self.manager.current = 'signup'

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super(SignupScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        layout.add_widget(Label(text="Signup Screen"))
        layout.add_widget(Button(text="Signup", on_press=self.signup))
        layout.add_widget(Button(text="Back to Login", on_press=self.back_to_login))

    def signup(self, instance):
        # Here you would implement the signup functionality
        print("Signup clicked")

    def back_to_login(self, instance):
        self.manager.current = 'login'

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        layout.add_widget(Label(text="Main Menu Screen"))
        layout.add_widget(Button(text="Dashboard"))

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        return sm

if __name__ == '__main__':
    MyApp().run()
