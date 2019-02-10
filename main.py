from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '300')

sm = ScreenManager()


class Menu(Screen):
    def choose_mode(self, mode):
        if mode == 'practice':
            sm.transition.direction = 'left'
            sm.current = 'practice_mode'
            readyView = ReadyView()
            readyView.open()


class ReadyView(ModalView):
    def yesButton(self):
        self.dismiss()

    def backButton(self):
        sm.transition.direction = 'right'
        sm.current = 'menu'
        self.dismiss()


class Practice(Screen):
    pass


class HitBlowApp(App):
    def build(self):
        sm.add_widget(Menu(name='menu'))
        sm.add_widget(Practice(name='practice_mode'))
        return sm


if __name__ == '__main__':
    HitBlowApp().run()
