from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.modalview import ModalView
from kivy.properties import ListProperty, NumericProperty
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '300')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

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
    user_attack = ListProperty([1, 2, 3, 4])
    com_defense = ListProperty([1, 2, 3, 4])
    digit_num = NumericProperty(0)

    def input_pressed(self, input, digit_num=0):
        if input == 'back':
            sm.transition.direction = 'right'
            sm.current = 'menu'

        if input == 'C':
            # 初めListProperty([1,2...])とやったらうまく行かなかった．よくわからないがListPropertyにするのは最初だけでいいみたい
            self.user_attack = [1, 2, 3, 4]

        if type(input) == int:
            self.user_attack[digit_num] = input


class HitBlowApp(App):
    def build(self):
        sm.add_widget(Menu(name='menu'))
        sm.add_widget(Practice(name='practice_mode'))
        return sm


if __name__ == '__main__':
    HitBlowApp().run()
