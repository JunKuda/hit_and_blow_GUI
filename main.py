from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
import random

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '300')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('modules', 'inspector', '')

sm = ScreenManager()


# 受け取った数字が重複のない４桁か？
# 不正な値ならFalseを返す
def number_input_check(input_num):
    if len(set(input_num)) != 4:
        return False

    else:
        return True


# 防御の数字，攻撃の数字を受け取りヒット数とブロー数を返す
def hit_and_blow(defense_num, attack_num):
    i = hit = blow = 0
    for num in attack_num:
        if defense_num[i] == num:
            hit += 1
        elif num in defense_num:
            blow += 1
        i += 1

    return hit, blow


# 最初に表示されるメニュー画面
class Menu(Screen):
    def choose_mode(self, mode):
        if mode == 'practice':
            sm.transition.direction = 'left'
            # 一度メニューにもどって，またモードを切り替えたときに最初期化
            sm.get_screen('practice_mode').__init__()
            sm.current = 'practice_mode'
            # 確認開始画面をポップアップ
            readyView = ReadyView()
            readyView.open()

        if mode == 'vs_com_mode':
            sm.transition.direction = 'left'
            sm.get_screen('vs_com_mode').__init__()
            sm.current = 'vs_com_mode'


class ReadyView(ModalView):
    def yesButton(self):
        self.dismiss()

    def backButton(self):
        sm.transition.direction = 'right'
        sm.current = 'menu'
        self.dismiss()


class YouWin(ModalView):
    def backButton(self):
        sm.transition.direction = 'right'
        sm.current = 'menu'
        self.dismiss()


# Practiceモード
class Practice(Screen):
    # ListPropertyにリストを渡すとunexpectedになる？
    user_attack = ListProperty([1, 2, 3, 4])
    #    com_defense = ListProperty([1, 2, 3, 4])
    com_defense = ListProperty(random.sample([i for i in range(1, 10)], 4))
    # 複数のプロパティをつなげて宣言するとなんか変な挙動をする（ハマってしまった）
    digit_num = NumericProperty(0)
    hit = NumericProperty(0)
    blow = NumericProperty(0)
    msg = StringProperty('')

    # メニューに戻った後，またPracticeモードに来たときに前のやつが残らないように
    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        self.digit_num = 0
        self.digit_num = 0
        self.hit = 0
        self.blow = 0
        self.msg = ''

    def input_pressed(self, input, digit_num=0):
        if input == 'back':
            sm.transition.direction = 'right'
            sm.current = 'menu'

        if input == 'C':
            # 初めListProperty([1,2...])とやったらうまく行かなかった．よくわからないがListPropertyにするのは最初だけでいいみたい
            self.user_attack = [1, 2, 3, 4]

        if type(input) == int:
            self.user_attack[digit_num] = input

    def attack(self):
        if not number_input_check(self.user_attack):
            # 先頭に追加．ちょっとみっともないが，=+という演算子はないっぽい？
            self.msg = 'Duplication of number is forbidden.\n' + self.msg
            return

        self.hit, self.blow = hit_and_blow(self.com_defense, self.user_attack)
        self.msg = str(self.user_attack) + str(self.hit) + 'HIT!' + str(self.blow) + 'BLOW!\n' + self.msg

        if self.hit == 4:
            youwin = YouWin()
            youwin.open()


# VsComモードの準備（防衛番号設定）画面
class VsComMode(Screen):
    user_defense = ListProperty([1, 2, 3, 4])
    digit_num = NumericProperty(0)
    hit = NumericProperty(0)
    blow = NumericProperty(0)
    msg = StringProperty('Please input your defense number')

    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        self.digit_num = 0
        self.digit_num = 0
        self.hit = 0
        self.blow = 0
        self.msg = 'Please input your defense number'

    def input_pressed(self, input, digit_num=0):
        if input == 'back':
            sm.transition.direction = 'right'
            sm.current = 'menu'

        if input == 'C':
            self.user_defense = [1, 2, 3, 4]

        if type(input) == int:
            self.user_defense[digit_num] = input

    def decide_my_defense(self):
        if not number_input_check(self.user_defense):
            self.msg = 'Duplication of number is forbidden.\n' + self.msg
        else:
            # スクリーン間で値を受け渡す方法がこれしかわからない
            sm.get_screen('vs_com_mode_battle').user_defense = self.user_defense
            sm.current = 'vs_com_mode_battle'


# VsComモードのバトル画面
# Practiceモードを継承してUI等使い回す
class VsComModeBattle(Practice):
    # コンピュータの初期攻撃値などPracticeモードにないパラメータ
    user_defense = ListProperty([1, 2, 3, 4])
    com_attack = ListProperty(random.sample([i for i in range(1, 10)], 4))
    com_hit = NumericProperty(0)
    com_blow = NumericProperty(0)

    def attack(self):
        if not number_input_check(self.user_attack):
            self.msg = 'Duplication of number is forbidden.\n' + self.msg
            return

        self.hit, self.blow = hit_and_blow(self.com_defense, self.user_attack)
        self.msg = 'You:' + str(self.user_attack) + ' ' + str(self.hit) + 'HIT!' + str(self.blow) + 'BLOW!\n' + self.msg

        if self.hit == 4:
            youwin = YouWin()
            youwin.open()

        # コンピュータの思考ルーチンがここに入る

        self.com_hit, self.com_blow = hit_and_blow(self.user_defense, self.com_attack)
        self.msg = 'Com:' + str(self.com_attack) + str(self.com_hit) + ' ' + 'HIT!' + str(self.com_blow) + 'BLOW!\n' + self.msg

        if self.com_hit == 4:
            # ここあとで直す
            youlose = YouWin()
            youlose.open()


class HitBlowApp(App):
    def build(self):
        sm.add_widget(Menu(name='menu'))
        sm.add_widget(Practice(name='practice_mode'))
        sm.add_widget(VsComMode(name='vs_com_mode'))
        sm.add_widget(VsComModeBattle(name='vs_com_mode_battle'))
        return sm


if __name__ == '__main__':
    HitBlowApp().run()
