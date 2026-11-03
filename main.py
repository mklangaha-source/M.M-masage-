from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text='M.M Massage App', font_size=30))
        layout.add_widget(Button(text='Book Now', size_hint_y=None, height=50))
        return layout

MyApp().run()
