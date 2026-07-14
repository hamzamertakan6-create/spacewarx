# -*- coding: utf-8 -*-
"""
SpaceWarx - 2D Pixel Art Space Shooter
Faz 1: Splash -> Loading+Language -> Tutorial -> (Menu placeholder)
"""
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Rotate
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
FONTS = os.path.join(BASE, "fonts")

LabelBase.register(name="Pixel", fn_regular=os.path.join(FONTS, "PixelifySans-Medium.ttf"))
LabelBase.register(name="CJK", fn_regular=os.path.join(FONTS, "NotoSansCJK-SC.ttf"))
LabelBase.register(name="Cyrillic", fn_regular=os.path.join(FONTS, "arial.ttf"))


def font_for(text):
    """Pick a registered font that actually has glyphs for this string.
    PixelifySans only covers Latin, so Cyrillic/CJK text needs a fallback
    font or it renders as blank boxes."""
    for ch in text:
        code = ord(ch)
        if 0x3040 <= code <= 0x30FF or 0x4E00 <= code <= 0x9FFF or 0x3400 <= code <= 0x4DBF:
            return "CJK"
        if 0x0400 <= code <= 0x04FF:
            return "Cyrillic"
    return "Pixel"

Window.clearcolor = (0.02, 0.02, 0.05, 1)

# ---------------------------------------------------------------
# Basic i18n
# ---------------------------------------------------------------
LANGS = ["tr", "en", "fr", "pt", "ru", "jp", "cn"]

TEXTS = {
    "loading": {
        "tr": "YÜKLENİYOR", "en": "LOADING", "fr": "CHARGEMENT",
        "pt": "CARREGANDO", "ru": "ЗАГРУЗКА", "jp": "ロード中", "cn": "加载中",
    },
    "select_lang": {
        "tr": "DİL SEÇ", "en": "SELECT LANGUAGE", "fr": "CHOISIR LANGUE",
        "pt": "ESCOLHER IDIOMA", "ru": "ЯЗЫК", "jp": "言語選択", "cn": "选择语言",
    },
    "drag_up": {
        "tr": "YUKARI SÜRÜKLE", "en": "DRAG UP", "fr": "GLISSE VERS HAUT",
        "pt": "ARRASTE PARA CIMA", "ru": "ТЯНИ ВВЕРХ", "jp": "上にドラッグ", "cn": "向上拖动",
    },
    "drag_right": {
        "tr": "SAĞA SÜRÜKLE", "en": "DRAG RIGHT", "fr": "GLISSE À DROITE",
        "pt": "ARRASTE À DIREITA", "ru": "ТЯНИ ВПРАВО", "jp": "右にドラッグ", "cn": "向右拖动",
    },
    "drag_left": {
        "tr": "SOLA SÜRÜKLE", "en": "DRAG LEFT", "fr": "GLISSE À GAUCHE",
        "pt": "ARRASTE À ESQUERDA", "ru": "ТЯНИ ВЛЕВО", "jp": "左にドラッグ", "cn": "向左拖动",
    },
    "success": {
        "tr": "BAŞARILI!", "en": "SUCCESS!", "fr": "SUCCÈS!",
        "pt": "SUCESSO!", "ru": "УСПЕХ!", "jp": "成功!", "cn": "成功!",
    },
    "tap_continue": {
        "tr": "DEVAM ETMEK İÇİN DOKUN", "en": "TAP TO CONTINUE", "fr": "TOUCHEZ POUR CONTINUER",
        "pt": "TOQUE PARA CONTINUAR", "ru": "НАЖМИТЕ ДЛЯ ПРОДОЛЖЕНИЯ", "jp": "タップして続行", "cn": "点击继续",
    },
    "level_complete": {
        "tr": "BÖLÜM TAMAMLANDI!", "en": "LEVEL COMPLETE!", "fr": "NIVEAU TERMINÉ!",
        "pt": "NÍVEL COMPLETO!", "ru": "УРОВЕНЬ ПРОЙДЕН!", "jp": "レベルクリア!", "cn": "关卡完成!",
    },
    "game_over": {
        "tr": "OYUN BİTTİ", "en": "GAME OVER", "fr": "PARTIE TERMINÉE",
        "pt": "FIM DE JOGO", "ru": "ИГРА ОКОНЧЕНА", "jp": "ゲームオーバー", "cn": "游戏结束",
    },
}


def tr_text(key, lang):
    return TEXTS.get(key, {}).get(lang, TEXTS.get(key, {}).get("en", key))


# ---------------------------------------------------------------
# Space background widget (tiled pixel starfield, slowly scrolls)
# ---------------------------------------------------------------
class SpaceBackground(Widget):
    scroll_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tex = Image(source=os.path.join(ASSETS, "space_bg.png")).texture
        self.tex.wrap = "repeat"
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(texture=self.tex, pos=self.pos, size=(self.width, self.height * 2))
        self.bind(pos=self._update, size=self._update)
        Clock.schedule_interval(self._scroll, 1 / 30)

        # Distant planets - slow parallax drift for a "deep space" creative touch
        self.mars = Image(source=os.path.join(ASSETS, "mars.png"), size_hint=(None, None),
                           size=(70, 70), opacity=0.9)
        self.add_widget(self.mars)
        self.earth = Image(source=os.path.join(ASSETS, "earth.png"), size_hint=(None, None),
                            size=(38, 38), opacity=0.85)
        self.add_widget(self.earth)
        self._planet_t = 0
        self.bind(pos=self._place_planets, size=self._place_planets)
        Clock.schedule_interval(self._drift_planets, 1 / 30)

    def _place_planets(self, *a):
        self.mars.pos = (self.x + self.width * 0.62, self.y + self.height * 0.8)
        self.earth.pos = (self.x + self.width * 0.12, self.y + self.height * 0.35)

    def _drift_planets(self, dt):
        self._planet_t += dt
        self.mars.y -= 6 * dt
        self.earth.y -= 3 * dt
        if self.mars.y < self.y - 80:
            self.mars.y = self.y + self.height + 40
        if self.earth.y < self.y - 50:
            self.earth.y = self.y + self.height + 30

    def _update(self, *a):
        self.rect.pos = (self.x, self.y - self.scroll_y)
        self.rect.size = (self.width, self.height * 2)
        self._set_uv()

    def _set_uv(self):
        # repeat texture vertically for endless scroll illusion
        tw, th = self.tex.size
        rep_y = max(1.0, self.height * 2 / th)
        self.tex.uvsize = (1, rep_y)
        self.tex.uvpos = (0, 0)

    def _scroll(self, dt):
        self.scroll_y = (self.scroll_y + 20 * dt) % (self.tex.height or 1)
        self.rect.pos = (self.x, self.y - self.scroll_y)


# ---------------------------------------------------------------
# LANGUAGE SCREEN: pure black, asked ONCE before splash, stays forever
# ---------------------------------------------------------------
LANG_NAMES = {
    "tr": "Türkçe", "en": "English", "fr": "Français",
    "pt": "Português", "ru": "Русский", "jp": "日本語", "cn": "中文",
}


class LanguageScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        root = FloatLayout()
        with root.canvas.before:
            Color(0, 0, 0, 1)
            self._bgr = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bgr, "pos", root.pos),
                  size=lambda *a: setattr(self._bgr, "size", root.size))

        # a few faint stars for atmosphere, but background stays essentially black
        title = Label(text="SELECT LANGUAGE / DİL SEÇ", font_name="Pixel", font_size=16,
                       color=(0.9, 0.9, 0.9, 1), size_hint=(None, None), size=(360, 40),
                       pos_hint={"center_x": 0.5, "top": 0.62})
        root.add_widget(title)

        grid_top = 0.52
        cols = 2
        cell_w, cell_h = 170, 64
        gap_x, gap_y = 16, 14
        total_w = cols * cell_w + gap_x
        start_x = 0.5 - (total_w / 2) / 400  # approximation, refined via pos below

        container = FloatLayout(size_hint=(None, None), size=(360, 320),
                                 pos_hint={"center_x": 0.5, "top": grid_top})
        for i, code in enumerate(LANGS):
            col = i % cols
            row = i // cols
            btn = Button(text=LANG_NAMES[code], font_name=font_for(LANG_NAMES[code]), font_size=13,
                         size_hint=(None, None), size=(cell_w, cell_h),
                         pos=(col * (cell_w + gap_x), 320 - (row + 1) * (cell_h + gap_y)),
                         background_normal="", background_down="",
                         background_color=(0.1, 0.1, 0.16, 1), color=(1, 1, 1, 1))
            flag = Image(source=os.path.join(ASSETS, f"flag_{code}.png"),
                         size_hint=(None, None), size=(34, 24),
                         pos=(btn.x + 8, btn.y + cell_h / 2 - 12))
            btn.bind(on_release=lambda inst, c=code: self._pick(c))
            container.add_widget(btn)
            container.add_widget(flag)
        root.add_widget(container)
        self.add_widget(root)

    def _pick(self, code):
        app = App.get_running_app()
        app.lang = code
        app.save_data["lang"] = code
        app.save()
        self.manager.current = "splash"


# ---------------------------------------------------------------
# SPLASH SCREEN: black square shrinks & fades to reveal space bg
# ---------------------------------------------------------------
class SplashScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        root = FloatLayout()
        bg = SpaceBackground(size_hint=(1, 1))
        root.add_widget(bg)

        logo = Image(source=os.path.join(ASSETS, "icon.png"),
                      size_hint=(None, None), size=(140, 140),
                      pos_hint={"center_x": 0.5, "center_y": 0.5}, opacity=0)
        root.add_widget(logo)

        black = Widget(size_hint=(1, 1))
        with black.canvas:
            Color(0, 0, 0, 1)
            self._brect = Rectangle(pos=self.pos, size=self.size)
        black.bind(pos=lambda *a: setattr(self._brect, "pos", black.pos))
        black.bind(size=lambda *a: setattr(self._brect, "size", black.size))
        root.add_widget(black)

        self.add_widget(root)

        Animation(opacity=1, d=0.6).start(logo)

        self._splash_event = Clock.schedule_once(lambda dt: self._start_fade(black), 0.8)

    def _start_fade(self, black):
        self._t = 0

        def upd(dt):
            if self.manager.current != self.name:
                return False  # navigated away, stop touching this screen
            self._t += dt
            a = max(0, 1 - self._t / 0.9)
            black.canvas.clear()
            with black.canvas:
                Color(0, 0, 0, a)
                Rectangle(pos=black.pos, size=black.size)
            if a <= 0:
                self.manager.current = "loading"
                return False
            return True

        self._splash_event = Clock.schedule_interval(upd, 1 / 60)

    def on_leave(self):
        if getattr(self, "_splash_event", None):
            Clock.unschedule(self._splash_event)


# ---------------------------------------------------------------
# LOADING + LANGUAGE SCREEN
# ---------------------------------------------------------------
class LoadingScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self.lang = App.get_running_app().lang
        self.progress = 0
        self.loaded = False
        App.get_running_app().play_music("menu")

        root = FloatLayout()
        root.add_widget(SpaceBackground(size_hint=(1, 1)))

        self.logo = Image(source=os.path.join(ASSETS, "icon.png"),
                           size_hint=(None, None), size=(110, 110),
                           pos_hint={"center_x": 0.5, "center_y": 0.58})
        root.add_widget(self.logo)

        _loading_txt = tr_text("loading", self.lang)
        self.status_label = Label(text=_loading_txt, font_name=font_for(_loading_txt),
                                   font_size=22, color=(1, 1, 1, 1),
                                   size_hint=(None, None), size=(300, 40),
                                   pos_hint={"center_x": 0.5, "center_y": 0.42})
        root.add_widget(self.status_label)

        bar_bg = Widget(size_hint=(None, None), size=(280, 22),
                         pos_hint={"center_x": 0.5, "center_y": 0.36})
        with bar_bg.canvas:
            Color(0.15, 0.15, 0.2, 1)
            Rectangle(pos=bar_bg.pos, size=bar_bg.size)
        root.add_widget(bar_bg)

        self.bar_fill = Widget(size_hint=(None, None), size=(0, 18),
                                pos=(bar_bg.x + 2, bar_bg.y + 2))
        with self.bar_fill.canvas:
            Color(1, 0.82, 0.15, 1)
            self._fill_rect = Rectangle(pos=self.bar_fill.pos, size=self.bar_fill.size)
        root.add_widget(self.bar_fill)
        self._bar_bg = bar_bg

        self.pct_label = Label(text="0%", font_name="Pixel", font_size=14,
                                color=(1, 1, 1, 1), size_hint=(None, None), size=(100, 20),
                                pos_hint={"center_x": 0.5, "center_y": 0.31})
        root.add_widget(self.pct_label)

        self.add_widget(root)
        self._loading_event = Clock.schedule_interval(self._tick, 1 / 30)

    def _tick(self, dt):
        if self.manager.current != self.name:
            return False  # navigated away, stop
        if self.loaded:
            return False
        self.progress += 55 * dt
        if self.progress >= 100:
            self.progress = 100
            self.loaded = True
            Clock.schedule_once(self._go_tutorial, 0.4)
        w = self._bar_bg.width - 4
        self.bar_fill.width = w * (self.progress / 100)
        self._fill_rect.size = self.bar_fill.size
        self._fill_rect.pos = self.bar_fill.pos
        self.pct_label.text = f"{int(self.progress)}%"
        return True

    def _go_tutorial(self, dt):
        if self.manager.current == self.name:
            self.manager.current = "tutorial"

    def on_leave(self):
        if getattr(self, "_loading_event", None):
            Clock.unschedule(self._loading_event)

# ---------------------------------------------------------------
# TUTORIAL SCREEN: arrow up / right / left, then SUCCESS
# ---------------------------------------------------------------
class TutorialScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        self.lang = App.get_running_app().lang
        self.step = 0
        self.steps = ["drag_up", "drag_right", "drag_left"]

        root = FloatLayout()
        root.add_widget(SpaceBackground(size_hint=(1, 1)))

        self.plane = Image(source=os.path.join(ASSETS, "player.png"),
                            size_hint=(None, None), size=(64, 64),
                            pos_hint={"center_x": 0.5, "center_y": 0.45})
        root.add_widget(self.plane)

        self.arrow = Image(source=os.path.join(ASSETS, "arrow.png"),
                            size_hint=(None, None), size=(48, 48),
                            pos_hint={"center_x": 0.5, "center_y": 0.62})
        with self.arrow.canvas.before:
            PushMatrix()
            self._arrow_rotate = Rotate(angle=0, origin=self.arrow.center)
        with self.arrow.canvas.after:
            PopMatrix()
        self.arrow.bind(center=lambda *a: setattr(self._arrow_rotate, "origin", self.arrow.center))
        root.add_widget(self.arrow)

        self.instr = Label(text="", font_name="Pixel", font_size=20,
                            color=(1, 1, 1, 1), size_hint=(None, None), size=(320, 40),
                            pos_hint={"center_x": 0.5, "center_y": 0.78})
        root.add_widget(self.instr)

        self.success_label = Label(text="", font_name="Pixel", font_size=30,
                                    color=(1, 0.85, 0.2, 0), size_hint=(None, None),
                                    size=(320, 50), pos_hint={"center_x": 0.5, "center_y": 0.55})
        root.add_widget(self.success_label)

        self.add_widget(root)
        self._show_step()
        self._bob_arrow()

    def _bob_arrow(self):
        rot_map = {"drag_up": 0, "drag_right": -90, "drag_left": 90}
        key = self.steps[self.step] if self.step < len(self.steps) else "drag_up"
        self._arrow_rotate.angle = rot_map.get(key, 0)

    def _show_step(self):
        if self.step >= len(self.steps):
            self._finish()
            return
        key = self.steps[self.step]
        self.instr.text = tr_text(key, self.lang)
        self.instr.font_name = font_for(self.instr.text)
        self._bob_arrow()

        plane_targets = {
            "drag_up": {"center_x": 0.5, "center_y": 0.58},
            "drag_right": {"center_x": 0.68, "center_y": 0.45},
            "drag_left": {"center_x": 0.32, "center_y": 0.45},
        }
        arrow_bob = {
            "drag_up": [(0.5, 0.66), (0.5, 0.60)],
            "drag_right": [(0.62, 0.62), (0.56, 0.62)],
            "drag_left": [(0.38, 0.62), (0.44, 0.62)],
        }
        Animation.cancel_all(self.arrow)
        Animation.cancel_all(self.plane)
        b1, b2 = arrow_bob[key]
        anim = Animation(pos_hint={"center_x": b1[0], "center_y": b1[1]}, d=0.4, t="in_out_sine") + \
               Animation(pos_hint={"center_x": b2[0], "center_y": b2[1]}, d=0.4, t="in_out_sine")
        anim.repeat = True
        anim.start(self.arrow)
        Animation(pos_hint=plane_targets[key], d=0.8, t="out_quad").start(self.plane)
        Clock.schedule_once(lambda dt: self._advance(), 1.6)

    def _advance(self):
        Animation.cancel_all(self.arrow)
        self.step += 1
        self._show_step()

    def _finish(self):
        self.arrow.opacity = 0
        self.instr.text = ""
        self.success_label.text = tr_text("success", self.lang)
        self.success_label.font_name = font_for(self.success_label.text)
        Animation(color=(1, 0.85, 0.2, 1), font_size=34, d=0.5).start(self.success_label)
        _tap_txt = tr_text("tap_continue", self.lang)
        tap = Label(text=_tap_txt, font_name=font_for(_tap_txt),
                    font_size=14, color=(1, 1, 1, 0), size_hint=(None, None), size=(320, 30),
                    pos_hint={"center_x": 0.5, "center_y": 0.35})
        self.add_widget(tap)
        Animation(color=(1, 1, 1, 1), d=1.0).start(tap)
        Clock.schedule_once(lambda dt: self._enable_tap(), 1.0)

    def _enable_tap(self):
        self._can_continue = True

    def on_touch_down(self, touch):
        if getattr(self, "_can_continue", False):
            self.manager.current = "menu"
        return super().on_touch_down(touch)


# ---------------------------------------------------------------
# MENU SCREEN placeholder (Faz 2'de dolacak)
# ---------------------------------------------------------------
class UsernamePopup(FloatLayout):
    def __init__(self, on_submit, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 0.75)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *a: setattr(self._bg, "pos", self.pos),
                  size=lambda *a: setattr(self._bg, "size", self.size))

        panel = Widget(size_hint=(None, None), size=(300, 180),
                        pos_hint={"center_x": 0.5, "center_y": 0.5})
        with panel.canvas:
            Color(0.08, 0.08, 0.14, 1)
            Rectangle(pos=panel.pos, size=panel.size)
        self.add_widget(panel)

        title = Label(text="PILOT ADIN?", font_name="Pixel", font_size=18,
                       color=(1, 1, 1, 1), size_hint=(None, None), size=(260, 30),
                       pos_hint={"center_x": 0.5, "center_y": 0.63})
        self.add_widget(title)

        from kivy.uix.textinput import TextInput
        self.input = TextInput(text="Pilot", multiline=False, font_size=18,
                                size_hint=(None, None), size=(240, 44),
                                pos_hint={"center_x": 0.5, "center_y": 0.5},
                                background_color=(0.15, 0.15, 0.22, 1),
                                foreground_color=(1, 1, 1, 1), cursor_color=(1, 1, 1, 1),
                                padding=(10, 10))
        self.add_widget(self.input)

        ok_btn = Button(text="BASLA", font_name="Pixel", font_size=16,
                         size_hint=(None, None), size=(140, 44),
                         pos_hint={"center_x": 0.5, "center_y": 0.35},
                         background_color=(1, 0.82, 0.15, 1), color=(0.1, 0.1, 0.1, 1))

        def submit(*a):
            name = self.input.text.strip() or "Pilot"
            on_submit(name)

        ok_btn.bind(on_release=submit)
        self.add_widget(ok_btn)


class MenuScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        app.play_music("menu")
        self.gold = app.save_data.get("gold", 0)
        self.diamonds = app.save_data.get("diamonds", 5)

        root = FloatLayout()
        self.bg = SpaceBackground(size_hint=(1, 1))
        root.add_widget(self.bg)
        self._add_drifting_ships(root)

        # top currency bar
        bar = Widget(size_hint=(None, None), size=(170, 40), pos=(10, self.height - 50 if self.height else 680))
        with bar.canvas:
            Color(0.05, 0.05, 0.1, 0.75)
            Rectangle(pos=bar.pos, size=bar.size)
        root.add_widget(bar)
        bar.pos_hint = {"x": 0.03, "top": 0.98}

        coin_img = Image(source=os.path.join(ASSETS, "coin.png"), size_hint=(None, None),
                          size=(28, 28), pos_hint={"x": 0.05, "top": 0.965})
        root.add_widget(coin_img)
        self.gold_label = Label(text=str(self.gold), font_name="Pixel", font_size=16,
                                 color=(1, 1, 1, 1), size_hint=(None, None), size=(60, 28),
                                 pos_hint={"x": 0.135, "top": 0.975})
        root.add_widget(self.gold_label)

        dia_img = Image(source=os.path.join(ASSETS, "diamond.png"), size_hint=(None, None),
                         size=(26, 26), pos_hint={"x": 0.24, "top": 0.965})
        root.add_widget(dia_img)
        self.dia_label = Label(text=str(self.diamonds), font_name="Pixel", font_size=16,
                                color=(1, 1, 1, 1), size_hint=(None, None), size=(60, 28),
                                pos_hint={"x": 0.325, "top": 0.975})
        root.add_widget(self.dia_label)

        # title/logo
        title = Label(text="SPACEWARX", font_name="Pixel", font_size=34,
                       color=(1, 0.85, 0.2, 1), size_hint=(None, None), size=(320, 60),
                       pos_hint={"center_x": 0.5, "center_y": 0.78})
        root.add_widget(title)

        # bottom row: chest (left) - play (center) - map (right), ALL equal square buttons
        BTN_SIZE = 76
        chest_btn = Button(background_normal=os.path.join(ASSETS, "chest.png"),
                            background_down=os.path.join(ASSETS, "chest.png"),
                            size_hint=(None, None), size=(BTN_SIZE, BTN_SIZE),
                            pos_hint={"x": 0.08, "center_y": 0.16})
        chest_btn.bind(on_release=lambda *a: self._open_shop())
        root.add_widget(chest_btn)

        map_btn = Button(background_normal=os.path.join(ASSETS, "map_icon.png"),
                          background_down=os.path.join(ASSETS, "map_icon.png"),
                          size_hint=(None, None), size=(BTN_SIZE, BTN_SIZE),
                          pos_hint={"right": 0.92, "center_y": 0.16})
        map_btn.bind(on_release=lambda *a: self._open_map())
        root.add_widget(map_btn)

        play_btn = Button(background_normal=os.path.join(ASSETS, "play_button.png"),
                           background_down=os.path.join(ASSETS, "play_button.png"),
                           size_hint=(None, None), size=(BTN_SIZE, BTN_SIZE),
                           pos_hint={"center_x": 0.5, "center_y": 0.16})
        play_btn.bind(on_release=lambda *a: self._start_game())
        root.add_widget(play_btn)

        # bottom-right upgrade button
        upg_btn = Button(background_normal=os.path.join(ASSETS, "upgrade_icon.png"),
                          background_down=os.path.join(ASSETS, "upgrade_icon.png"),
                          size_hint=(None, None), size=(52, 52),
                          pos_hint={"right": 0.97, "y": 0.03})
        upg_btn.bind(on_release=lambda *a: self._open_upgrade())
        root.add_widget(upg_btn)

        self.add_widget(root)
        self._root_layout = root

        if not app.save_data.get("username"):
            popup = UsernamePopup(on_submit=self._set_username, size_hint=(1, 1))
            self.add_widget(popup)

    def _set_username(self, name):
        app = App.get_running_app()
        app.save_data["username"] = name
        app.save()
        for w in list(self.children):
            if isinstance(w, UsernamePopup):
                self.remove_widget(w)

    def _add_drifting_ships(self, root):
        import random
        for i in range(3):
            sprite = random.choice(["cloud", "bird"])
            img = Image(source=os.path.join(ASSETS, f"{sprite}.png"), size_hint=(None, None),
                        size=(40, 30), opacity=0.5,
                        pos=(-60, 100 + i * 180))
            root.add_widget(img)
            anim = Animation(x=460, d=6 + i * 2, t="linear")
            anim.repeat = True
            Clock.schedule_once(lambda dt, im=img, an=anim: an.start(im), i * 1.5)

    def _open_shop(self):
        self.manager.current = "shop"

    def _open_map(self):
        self.manager.current = "campaign"

    def _start_game(self):
        self.manager.current = "game"

    def _open_upgrade(self):
        self.manager.current = "upgrade"


class GameScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        app.play_music("game")
        self.max_health = 100
        self.health = 100
        self.score = 0
        self.gold_collected = 0
        self.diamonds_collected = 0
        self.playing = False
        self.entrance_done = False
        self.shield_active = False
        self.shield_timer = 0
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.pickups = []
        self.touch_active = False
        self.wave_num = 1
        self.boss = None

        self.shield_count = app.save_data.get("ability_shield", 1)
        self.heal_count = app.save_data.get("ability_heal", 1)
        self.laser_count = app.save_data.get("ability_laser", 1)

        root = FloatLayout()
        self.bg = SpaceBackground(size_hint=(1, 1))
        root.add_widget(self.bg)
        self.root_layout = root

        # player starts below the screen, flies up (entrance animation)
        self.player = Image(source=os.path.join(ASSETS, "player.png"),
                             size_hint=(None, None), size=(56, 56),
                             pos=(400 / 2 - 28, -70))
        root.add_widget(self.player)

        self.flame = Image(source=os.path.join(ASSETS, "flame.png"),
                            size_hint=(None, None), size=(26, 26))
        root.add_widget(self.flame)

        # top-left health bar
        self.hp_bg = Widget(size_hint=(None, None), size=(160, 18), pos=(12, 690))
        with self.hp_bg.canvas:
            Color(0.15, 0.15, 0.2, 1)
            Rectangle(pos=self.hp_bg.pos, size=self.hp_bg.size)
        root.add_widget(self.hp_bg)
        self.hp_fill = Widget(size_hint=(None, None), size=(156, 14), pos=(14, 692))
        with self.hp_fill.canvas:
            Color(0.25, 0.85, 0.35, 1)
            self._hp_rect = Rectangle(pos=self.hp_fill.pos, size=self.hp_fill.size)
        root.add_widget(self.hp_fill)

        # score label top-right
        self.score_label = Label(text="0", font_name="Pixel", font_size=18,
                                  color=(1, 1, 1, 1), size_hint=(None, None), size=(100, 30),
                                  pos_hint={"right": 0.95, "top": 0.99})
        root.add_widget(self.score_label)

        # bottom-left ability circles: shield / heal / laser
        self.ability_widgets = {}
        names = [("shield", "shield_icon"), ("heal", "heart_icon"), ("laser", "laser_icon")]
        for i, (key, icon) in enumerate(names):
            circle = Widget(size_hint=(None, None), size=(50, 50), pos=(12 + i * 60, 14))
            count = getattr(self, f"{key}_count")
            with circle.canvas:
                Color(0.9, 0.75, 0.15, 1) if count > 0 else Color(0.3, 0.3, 0.35, 1)
                Rectangle(pos=circle.pos, size=circle.size)
            root.add_widget(circle)
            icon_img = Image(source=os.path.join(ASSETS, icon), size_hint=(None, None),
                              size=(28, 28), pos=(circle.x + 11, circle.y + 14))
            root.add_widget(icon_img)
            count_lbl = Label(text=str(count), font_name="Pixel", font_size=12,
                               color=(1, 1, 1, 1), size_hint=(None, None), size=(24, 18),
                               pos=(circle.x + 34, circle.y + 32))
            root.add_widget(count_lbl)
            btn = Button(size_hint=(None, None), size=circle.size, pos=circle.pos,
                         background_color=(0, 0, 0, 0))
            btn.bind(on_release=lambda inst, k=key: self._use_ability(k))
            root.add_widget(btn)
            self.ability_widgets[key] = {"circle": circle, "count_lbl": count_lbl, "btn": btn}

        self.add_widget(root)
        Animation(pos=(400 / 2 - 28, 130), d=1.0, t="out_quad").start(self.player)
        Clock.schedule_once(self._begin_play, 1.1)
        Clock.schedule_interval(self._update, 1 / 45)

    # ---------------- setup wave ----------------
    def _begin_play(self, dt):
        self.entrance_done = True
        self.playing = True
        self._spawn_wave()

    def _spawn_wave(self):
        import random
        xs = [50, 120, 190, 260, 330]
        random.shuffle(xs)
        types = ["fighter", "fighter", "fighter", "drone", "drone"]
        for i in range(5):
            kind = types[i]
            sprite = "enemy_red.png" if kind == "fighter" else "enemy_drone.png"
            img = Image(source=os.path.join(ASSETS, sprite), size_hint=(None, None),
                        size=(46, 46), pos=(xs[i] - 23, 760 + i * 40))
            self.root_layout.add_widget(img)
            enemy = {
                "kind": kind,
                "widget": img,
                "base_y": 560 - (i % 3) * 40,
                "phase": random.uniform(0, 6.28),
                "fire_cd": random.uniform(0.5, 1.5),
                "hp": 2 if kind == "fighter" else 1,
                "dodge_cd": 0,
                "vx": random.choice([-1, 1]) * (30 if kind == "fighter" else 70),
            }
            self.enemies.append(enemy)

    def _spawn_boss(self):
        app = App.get_running_app()
        app.play_sfx("boss_alarm")
        app.play_music("boss")
        warn = Label(text="BOSS!", font_name="Pixel", font_size=32,
                     color=(1, 0.2, 0.2, 0), size_hint=(None, None), size=(200, 50),
                     pos_hint={"center_x": 0.5, "center_y": 0.6})
        self.root_layout.add_widget(warn)
        anim = Animation(color=(1, 0.2, 0.2, 1), d=0.3) + Animation(color=(1, 0.2, 0.2, 0), d=0.3)
        anim.repeat = True
        anim.start(warn)
        Clock.schedule_once(lambda dt: (Animation.cancel_all(warn), self.root_layout.remove_widget(warn)), 1.8)

        img = Image(source=os.path.join(ASSETS, "ufo_boss.png"), size_hint=(None, None),
                    size=(140, 100), pos=(400 / 2 - 70, 800))
        self.root_layout.add_widget(img)
        self.boss = {
            "kind": "boss",
            "widget": img,
            "hp": 40, "max_hp": 40,
            "phase": 0,
            "attack_cd": 3.0,
            "vx": 55,
            "entered": False,
        }
        Animation(y=590, d=1.4, t="out_quad").start(img)
        Clock.schedule_once(lambda dt: self.boss.__setitem__("entered", True), 1.5)

        # boss health bar (top center)
        self.boss_hp_bg = Widget(size_hint=(None, None), size=(220, 16), pos=(90, 662))
        with self.boss_hp_bg.canvas:
            Color(0.15, 0.05, 0.05, 1)
            Rectangle(pos=self.boss_hp_bg.pos, size=self.boss_hp_bg.size)
        self.root_layout.add_widget(self.boss_hp_bg)
        self.boss_hp_fill = Widget(size_hint=(None, None), size=(216, 12), pos=(92, 664))
        with self.boss_hp_fill.canvas:
            Color(0.85, 0.15, 0.2, 1)
            self._boss_hp_rect = Rectangle(pos=self.boss_hp_fill.pos, size=self.boss_hp_fill.size)
        self.root_layout.add_widget(self.boss_hp_fill)

    # ---------------- input ----------------
    def on_touch_down(self, touch):
        if self.playing:
            self.touch_active = True
            self._move_player_to(touch.x, touch.y)
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.playing and self.touch_active:
            self._move_player_to(touch.x, touch.y)
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        self.touch_active = False
        return super().on_touch_up(touch)

    def _move_player_to(self, x, y):
        hw = self.player.width / 2
        hh = self.player.height / 2
        nx = max(hw, min(400 - hw, x))
        ny = max(hh + 20, min(680, y))
        self.player.center = (nx, ny)

    # ---------------- abilities ----------------
    def _use_ability(self, key):
        count = getattr(self, f"{key}_count")
        if count <= 0 or not self.playing:
            return
        App.get_running_app().play_sfx("ability")
        setattr(self, f"{key}_count", count - 1)
        self.ability_widgets[key]["count_lbl"].text = str(count - 1)
        circle = self.ability_widgets[key]["circle"]
        if count - 1 == 0:
            circle.canvas.clear()
            with circle.canvas:
                Color(0.3, 0.3, 0.35, 1)
                Rectangle(pos=circle.pos, size=circle.size)

        if key == "shield":
            self.shield_active = True
            self.shield_timer = 5.0
        elif key == "heal":
            self.health = min(self.max_health, self.health + 35)
        elif key == "laser":
            for enemy in list(self.enemies):
                self._kill_enemy(enemy)

    # ---------------- main loop ----------------
    def _update(self, dt):
        if not self.playing:
            return True
        import math, random
        app = App.get_running_app()

        # player bullets auto-fire
        self._player_fire_timer = getattr(self, "_player_fire_timer", 0) + dt
        if self._player_fire_timer >= 0.35:
            self._player_fire_timer = 0
            b = Image(source=os.path.join(ASSETS, "bullet_player.png"), size_hint=(None, None),
                      size=(18, 18), pos=(self.player.center_x - 9, self.player.top - 6))
            self.root_layout.add_widget(b)
            self.player_bullets.append(b)
            app.play_sfx("shoot")

        for b in list(self.player_bullets):
            b.y += 420 * dt
            if b.y > 740:
                self.root_layout.remove_widget(b)
                self.player_bullets.remove(b)

        # enemies: bob forward/back + dodge incoming player bullets + fire
        for e in list(self.enemies):
            e["phase"] += dt * (2.4 if e["kind"] == "drone" else 1.6)
            w = e["widget"]
            w.y = e["base_y"] + math.sin(e["phase"]) * (18 if e["kind"] == "drone" else 26)
            w.x += e["vx"] * dt
            if w.x < 10 or w.x > 400 - w.width - 10:
                e["vx"] *= -1

            e["dodge_cd"] = max(0, e["dodge_cd"] - dt)
            if e["dodge_cd"] == 0:
                for b in self.player_bullets:
                    if abs(b.center_x - w.center_x) < 26 and 0 < (w.y - b.y) < 90:
                        w.x += 46 if random.random() < 0.5 else -46
                        w.x = max(10, min(400 - w.width - 10, w.x))
                        e["dodge_cd"] = 0.8
                        break

            fire_interval = 0.7 if e["kind"] == "drone" else 1.1
            e["fire_cd"] -= dt
            if e["fire_cd"] <= 0:
                e["fire_cd"] = fire_interval + random.uniform(-0.2, 0.2)
                eb = Image(source=os.path.join(ASSETS, "bullet_enemy.png"), size_hint=(None, None),
                           size=(16, 16), pos=(w.center_x - 8, w.y - 10))
                self.root_layout.add_widget(eb)
                self.enemy_bullets.append(eb)

        # boss AI
        if self.boss:
            b = self.boss
            bw = b["widget"]
            if b["entered"]:
                b["phase"] += dt * 0.6
                bw.x = 400 / 2 - bw.width / 2 + math.sin(b["phase"]) * 130
                b["attack_cd"] -= dt
                if b["attack_cd"] <= 0:
                    b["attack_cd"] = 2.6
                    self._boss_attack(b)
            ratio = max(0, b["hp"] / b["max_hp"])
            self.boss_hp_fill.width = 216 * ratio
            self._boss_hp_rect.size = self.boss_hp_fill.size

        for b in list(self.enemy_bullets):
            b.y -= 260 * dt
            if b.y < -20:
                self.root_layout.remove_widget(b)
                self.enemy_bullets.remove(b)

        # pickups (gold/diamond) drift down
        for p in list(self.pickups):
            p["widget"].y -= 90 * dt
            if p["widget"].y < -20:
                self.root_layout.remove_widget(p["widget"])
                self.pickups.remove(p)

        self._check_collisions()

        # shield timer
        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False

        # flame follows player
        self.flame.pos = (self.player.center_x - 13, self.player.y - 18)

        # health bar update
        ratio = max(0, self.health / self.max_health)
        self.hp_fill.width = 156 * ratio
        self._hp_rect.size = self.hp_fill.size
        if self.health <= 0:
            self._game_over()

        # wave cleared -> next wave or boss or level complete
        if self.playing and self.entrance_done and len(self.enemies) == 0 and self.boss is None:
            if self.wave_num == 1:
                self.wave_num = 2
                self._spawn_boss()
            elif getattr(self, "_boss_defeated", False):
                self._level_complete()

        return True

    def _boss_attack(self, b):
        app = App.get_running_app()
        app.play_sfx("boss_attack")
        bw = b["widget"]
        import math
        n = 8
        for i in range(n):
            ang = (2 * math.pi / n) * i
            eb = Image(source=os.path.join(ASSETS, "bullet_ufo.png"), size_hint=(None, None),
                       size=(18, 18), pos=(bw.center_x - 9, bw.center_y - 9))
            eb.vx = math.cos(ang) * 140
            eb.vy = math.sin(ang) * 140
            self.root_layout.add_widget(eb)
            self.enemy_bullets.append(eb)

    def _check_collisions(self):
        app = App.get_running_app()
        # player bullets vs enemies
        for b in list(self.player_bullets):
            hit_something = False
            for e in list(self.enemies):
                w = e["widget"]
                if self._overlap(b, w):
                    e["hp"] -= 1
                    hit_something = True
                    if e["hp"] <= 0:
                        self._kill_enemy(e)
                    break
            if not hit_something and self.boss:
                bw = self.boss["widget"]
                if self._overlap(b, bw):
                    self.boss["hp"] -= 1
                    hit_something = True
                    if self.boss["hp"] <= 0:
                        self._kill_boss()
            if hit_something and b in self.player_bullets:
                self.root_layout.remove_widget(b)
                self.player_bullets.remove(b)

        # enemy bullets vs player
        if not self.shield_active:
            for b in list(self.enemy_bullets):
                # radial boss bullets carry their own velocity
                if hasattr(b, "vx"):
                    continue
                if self._overlap(b, self.player):
                    self.root_layout.remove_widget(b)
                    self.enemy_bullets.remove(b)
                    self.health -= 8
                    app.play_sfx("hit")
        else:
            pass

        # radial (boss) bullets move + collide separately since they have vx/vy
        for b in list(self.enemy_bullets):
            if hasattr(b, "vx"):
                if not self.shield_active and self._overlap(b, self.player):
                    self.root_layout.remove_widget(b)
                    self.enemy_bullets.remove(b)
                    self.health -= 12
                    app.play_sfx("hit")

        # player vs pickups
        for p in list(self.pickups):
            if self._overlap(p["widget"], self.player):
                if p["kind"] == "gold":
                    self.gold_collected += 1
                else:
                    self.diamonds_collected += 1
                self.root_layout.remove_widget(p["widget"])
                self.pickups.remove(p)
                self.score += 5
                app.play_sfx("pickup")

    def _overlap(self, a, b):
        return (a.x < b.x + b.width and a.x + a.width > b.x and
                a.y < b.y + b.height and a.y + a.height > b.y)

    def _kill_enemy(self, e):
        import random
        App.get_running_app().play_sfx("explosion")
        w = e["widget"]
        boom = Image(source=os.path.join(ASSETS, "explosion.png"), size_hint=(None, None),
                     size=(50, 50), pos=(w.center_x - 25, w.center_y - 25))
        self.root_layout.add_widget(boom)
        anim = Animation(opacity=0, size=(70, 70), d=0.35)
        anim.bind(on_complete=lambda *a: self.root_layout.remove_widget(boom))
        anim.start(boom)

        if w in self.root_layout.children:
            self.root_layout.remove_widget(w)
        if e in self.enemies:
            self.enemies.remove(e)
        self.score += 20

        if random.random() < 0.7:
            self._spawn_pickup(w.center_x, w.center_y, "gold")
        if random.random() < 0.15:
            self._spawn_pickup(w.center_x, w.center_y, "diamond")
        self.score_label.text = str(self.score)

    def _kill_boss(self):
        import random
        app = App.get_running_app()
        app.play_sfx("explosion")
        b = self.boss
        w = b["widget"]
        # bigger multi-burst explosion for a boss kill
        for i in range(4):
            ox = random.uniform(-30, 30)
            oy = random.uniform(-20, 20)
            boom = Image(source=os.path.join(ASSETS, "explosion.png"), size_hint=(None, None),
                         size=(60, 60), pos=(w.center_x - 30 + ox, w.center_y - 30 + oy))
            self.root_layout.add_widget(boom)
            anim = Animation(opacity=0, size=(90, 90), d=0.45)
            anim.bind(on_complete=lambda *a, bm=boom: self.root_layout.remove_widget(bm))
            Clock.schedule_once(lambda dt, a=anim, bm=boom: a.start(bm), i * 0.12)

        if w in self.root_layout.children:
            self.root_layout.remove_widget(w)
        if self.boss_hp_bg in self.root_layout.children:
            self.root_layout.remove_widget(self.boss_hp_bg)
        if self.boss_hp_fill in self.root_layout.children:
            self.root_layout.remove_widget(self.boss_hp_fill)

        self.score += 200
        self.score_label.text = str(self.score)
        for _ in range(4):
            self._spawn_pickup(w.center_x + random.uniform(-30, 30),
                                w.center_y + random.uniform(-20, 20), "gold")
        self._spawn_pickup(w.center_x, w.center_y, "diamond")

        self.boss = None
        self._boss_defeated = True
        app.play_music("game")

    def _spawn_pickup(self, x, y, kind):
        icon = "coin.png" if kind == "gold" else "diamond.png"
        img = Image(source=os.path.join(ASSETS, icon), size_hint=(None, None),
                    size=(22, 22), pos=(x - 11, y - 11))
        self.root_layout.add_widget(img)
        self.pickups.append({"widget": img, "kind": kind})

    def _level_complete(self):
        self.playing = False
        app = App.get_running_app()
        app.play_sfx("level_complete")
        app.save_data["gold"] = app.save_data.get("gold", 0) + self.gold_collected
        app.save_data["diamonds"] = app.save_data.get("diamonds", 0) + self.diamonds_collected
        app.save()
        for lst in (self.player_bullets, self.enemy_bullets):
            for b in lst:
                if b in self.root_layout.children:
                    self.root_layout.remove_widget(b)
            lst.clear()

        _lc_txt = tr_text("level_complete", app.lang)
        lbl = Label(text=_lc_txt, font_name=font_for(_lc_txt), font_size=26,
                    color=(1, 0.85, 0.2, 1), size_hint=(None, None), size=(320, 50),
                    pos_hint={"center_x": 0.5, "center_y": 0.6})
        self.root_layout.add_widget(lbl)
        Animation(pos=(self.player.x, 760), d=1.2, t="in_quad").start(self.player)
        Clock.schedule_once(self._return_to_menu, 2.0)

    def _game_over(self):
        self.playing = False
        app = App.get_running_app()
        app.play_sfx("game_over")
        app.save_data["gold"] = app.save_data.get("gold", 0) + self.gold_collected
        app.save_data["diamonds"] = app.save_data.get("diamonds", 0) + self.diamonds_collected
        app.save()
        _go_txt = tr_text("game_over", app.lang)
        lbl = Label(text=_go_txt, font_name=font_for(_go_txt), font_size=26,
                    color=(1, 0.3, 0.3, 1), size_hint=(None, None), size=(320, 50),
                    pos_hint={"center_x": 0.5, "center_y": 0.6})
        self.root_layout.add_widget(lbl)
        Clock.schedule_once(self._return_to_menu, 2.0)

    def _return_to_menu(self, dt):
        if self.manager.current == self.name:
            self.manager.current = "menu"

    def on_leave(self):
        Clock.unschedule(self._update)


class PlaceholderScreen(Screen):
    text_key = "SCREEN"

    def on_enter(self):
        self.clear_widgets()
        App.get_running_app().play_music("menu")
        root = FloatLayout()
        root.add_widget(SpaceBackground(size_hint=(1, 1)))
        lbl = Label(text=f"{self.text_key}\n(bir sonraki fazda)", font_name="Pixel",
                    font_size=20, color=(1, 1, 1, 1), halign="center",
                    pos_hint={"center_x": 0.5, "center_y": 0.55})
        root.add_widget(lbl)
        back = Button(text="< GERI", font_name="Pixel", font_size=16,
                      size_hint=(None, None), size=(120, 44),
                      pos_hint={"x": 0.05, "top": 0.97},
                      background_color=(0.2, 0.2, 0.3, 1))
        back.bind(on_release=lambda *a: setattr(self.manager, "current", "menu"))
        root.add_widget(back)
        self.add_widget(root)


class SpaceWarxApp(App):
    lang = StringProperty("en")

    def build(self):
        Window.size = (400, 720)
        self.save_path = os.path.join(self.user_data_dir, "save.json")
        self.save_data = self._load_save()
        if self.save_data.get("lang"):
            self.lang = self.save_data["lang"]
        self._music_cache = {}
        self._current_music_key = None
        self._current_music_category = None
        self._sfx_cache = {}
        sm = ScreenManager(transition=FadeTransition(duration=0.35))
        sm.add_widget(LanguageScreen(name="language"))
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LoadingScreen(name="loading"))
        sm.add_widget(TutorialScreen(name="tutorial"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        shop = PlaceholderScreen(name="shop"); shop.text_key = "SANDIK / MAGAZA"
        campaign = PlaceholderScreen(name="campaign"); campaign.text_key = "UZAY HARITASI"
        upgrade = PlaceholderScreen(name="upgrade"); upgrade.text_key = "UCAK YUKSELTME"
        sm.add_widget(shop)
        sm.add_widget(campaign)
        sm.add_widget(upgrade)
        sm.current = "splash" if self.save_data.get("lang") else "language"
        return sm

    def _load_save(self):
        import json
        try:
            with open(self.save_path, "r") as f:
                return json.load(f)
        except Exception:
            return {"gold": 0, "diamonds": 5, "username": ""}

    def save(self):
        import json
        try:
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            with open(self.save_path, "w") as f:
                json.dump(self.save_data, f)
        except Exception as e:
            print("save error", e)

    def play_music(self, key):
        """key: 'menu', 'game', or 'boss'. Menu/game rotate between variants
        so it's not the exact same loop every time; won't restart if the
        same resolved track is already playing."""
        import random
        variants = {
            "menu": ["music_menu.wav", "music_menu2.wav", "music_menu3.wav"],
            "game": ["music_game.wav", "music_game2.wav", "music_game3.wav"],
            "boss": ["music_boss.wav"],
        }
        if key == self._current_music_category:
            return  # already playing this category, don't restart/reshuffle
        if self._current_music_key is not None:
            old = self._music_cache.get(self._current_music_key)
            if old:
                old.stop()
        fname = random.choice(variants[key])
        if fname not in self._music_cache:
            snd = SoundLoader.load(os.path.join(ASSETS, fname))
            if snd:
                snd.loop = True
                snd.volume = 0.5 if key != "boss" else 0.6
            self._music_cache[fname] = snd
        snd = self._music_cache.get(fname)
        if snd:
            snd.play()
        self._current_music_key = fname
        self._current_music_category = key

    def stop_music(self):
        if self._current_music_key is not None:
            snd = self._music_cache.get(self._current_music_key)
            if snd:
                snd.stop()
        self._current_music_key = None
        self._current_music_category = None

    def play_sfx(self, key):
        fname = f"sfx_{key}.wav"
        if fname not in self._sfx_cache:
            snd = SoundLoader.load(os.path.join(ASSETS, fname))
            self._sfx_cache[fname] = snd
        snd = self._sfx_cache.get(fname)
        if snd:
            snd.volume = 0.5
            snd.play()


if __name__ == "__main__":
    SpaceWarxApp().run()
