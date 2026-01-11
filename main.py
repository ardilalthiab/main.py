import cv2
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from plyer import filechooser, notification

# --- 1. محرك المنطق العاطفي والمحاكاة ---
class PersonaEngine:
    def __init__(self):
        self.context = []
        self.identity = {"name": "", "image": "", "voice": ""}
        self.sensitivity = 50

    def analyze_emotion(self, text):
        sad_words = ["حزين", "ضيق", "تعب", "فشل"]
        happy_words = ["سعيد", "فرح", "نجاح", "ممتاز"]
        if any(w in text for w in sad_words): return "SAD"
        if any(w in text for w in happy_words): return "HAPPY"
        return "NEUTRAL"

    def get_response(self, text):
        emotion = self.analyze_emotion(text)
        responses = {
            "SAD": f"أنا أشعر بك يا صديقي.. {self.identity['name']} هنا لتسمعك.",
            "HAPPY": f"هذا رائع! حماسي كـ {self.identity['name']} لا يوصف بخبرك!",
            "NEUTRAL": "أنا أصغي إليك بكل اهتمام، واصل.."
        }
        return responses[emotion], emotion

# --- 2. شاشة الخصوصية ---
class PrivacyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)
        layout.add_widget(Label(text="تعهد الخصوصية الرقمي\nبياناتك مشفرة ولا يتم مشاركتها.", halign="center"))
        btn = Button(text="أوافق وأتعهد", size_hint_y=0.2)
        btn.bind(on_press=self.accept)
        layout.add_widget(btn)

    def accept(self, instance):
        self.manager.current = 'identity_screen'

# --- 3. شاشة بناء الهوية ---
class IdentityScreen(Screen):
    def finalize(self, instance):
        app = App.get_running_app()
        app.engine.identity['name'] = self.name_in.text
        self.manager.current = 'chat_screen'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.name_in = TextInput(hint_text="اسم الشخصية الرقمية", halign="right")
        btn_img = Button(text="رفع صورة من الجهاز")
        btn_voice = Button(text="رفع مقطع صوتي")
        btn_go = Button(text="تفعيل الشخصية", background_color=(0, 0.7, 0.3, 1))
        btn_go.bind(on_press=self.finalize)
        
        self.layout.add_widget(self.name_in)
        self.layout.add_widget(btn_img); self.layout.add_widget(btn_voice)
        self.layout.add_widget(btn_go)
        self.add_widget(self.layout)

# --- 4. شاشة الحوار والتحريك ---
class ChatScreen(Screen):
    def send(self, instance):
        text = self.input.text
        if text:
            app = App.get_running_app()
            reply, emotion = app.engine.get_response(text)
            self.logs.text += f"\nأنت: {text}\n{app.engine.identity['name']}: {reply}\n"
            self.input.text = ""
            # محاكاة التنبيه العاطفي
            if emotion == "SAD":
                notification.notify(title="اهتمام", message="هل أنت بخير الآن؟")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        self.logs = Label(text="ابدأ الحوار الآن...\n", halign="right", valign="top")
        self.input = TextInput(size_hint_y=0.1, multiline=False)
        btn = Button(text="إرسال", size_hint_y=0.1)
        btn.bind(on_press=self.send)
        
        layout.add_widget(self.logs)
        layout.add_widget(self.input)
        layout.add_widget(btn)
        self.add_widget(layout)

# --- 5. تشغيل التطبيق المتكامل ---
class PersonaApp(App):
    def build(self):
        self.engine = PersonaEngine()
        sm = ScreenManager()
        sm.add_widget(PrivacyScreen(name='privacy_screen'))
        sm.add_widget(IdentityScreen(name='identity_screen'))
        sm.add_widget(ChatScreen(name='chat_screen'))
        return sm

if __name__ == '__main__':
    PersonaApp().run()
