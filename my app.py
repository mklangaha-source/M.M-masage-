from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
import socket
import threading

class RoundButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.font_size = 16
        self.bold = True
        with self.canvas.before:
            Color(0.2, 0.6, 1, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[22])
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    def set_color(self, r, g, b):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(r, g, b, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[22])

class ChatBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 12
        self.conn = None

        self.history = Label(text='Private Chat App\n\nServer IP + Room Code likho\nSirf same code waly baat kar sakengy', size_hint=(1, 0.6), halign='left', valign='top', color=(0,0,0,1))
        self.history.bind(size=self.history.setter('text_size'))
        self.add_widget(self.history)

        # Server IP
        self.server_ip = TextInput(hint_text='Server IP - e.g 192.168.1.5', size_hint=(1, 0.08), multiline=False, background_color=(0.95,0.95,0.95,1), foreground_color=(0,0,0,1), padding=[12,8])
        self.add_widget(self.server_ip)

        # Room Code - Yahi aap ka private lock hai
        self.room_code = TextInput(hint_text='Private Code - e.g ALI-786', size_hint=(1, 0.08), multiline=False, background_color=(0.95,0.95,0.95,1), foreground_color=(0,0,0,1), padding=[12,8])
        self.add_widget(self.room_code)
        
        # Name
        self.my_name = TextInput(hint_text='Your Name', size_hint=(1, 0.08), multiline=False, background_color=(0.95,0.95,0.95,1), foreground_color=(0,0,0,1), padding=[12,8])
        self.add_widget(self.my_name)

        self.connect_btn = RoundButton(text='CONNECT', size_hint=(1, 0.12))
        self.connect_btn.set_color(0.15, 0.68, 0.38)
        self.connect_btn.bind(on_press=self.connect_to_server)
        self.add_widget(self.connect_btn)

        send_layout = BoxLayout(size_hint=(1, 0.12), spacing=10)
        self.msg_input = TextInput(hint_text='Type message...', multiline=False, background_color=(0.95,0.95,0.95,1), foreground_color=(0,0,0,1), padding=[12,8])
        self.send_btn = RoundButton(text='SEND', size_hint=(0.35, 1))
        self.send_btn.set_color(0.1, 0.1, 0.1)
        self.send_btn.bind(on_press=self.send_message)
        send_layout.add_widget(self.msg_input)
        send_layout.add_widget(self.send_btn)
        self.add_widget(send_layout)

    def add_chat(self, text):
        def update(dt):
            self.history.text += f"\n{text}"
        Clock.schedule_once(update)

    def connect_to_server(self, instance):
        ip = self.server_ip.text.strip()
        room = self.room_code.text.strip().upper()
        name = self.my_name.text.strip() or "User"
        if not ip or not room:
            self.add_chat("IP aur Room Code zaroori hai")
            return
        self.my_name_text = name
        self.room = room
        threading.Thread(target=self.client_thread, args=(ip, room), daemon=True).start()

    def client_thread(self, ip, room):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((ip, 5000))
            self.conn.send(f"ROOM:{room}".encode('utf-8'))
            self.add_chat(f"--- Connected to Room: {room} ---")
            while True:
                data = self.conn.recv(1024).decode('utf-8')
                if data:
                    if data.startswith("JOINED:"):
                        continue
                    self.add_chat(data)
        except Exception as e:
            self.add_chat(f"Error: {e}")

    def send_message(self, instance):
        if not self.conn or not self.msg_input.text.strip():
            return
        msg = f"{self.my_name_text}: {self.msg_input.text.strip()}"
        try:
            self.conn.send(msg.encode('utf-8'))
            self.add_chat(f"You: {self.msg_input.text.strip()}")
            self.msg_input.text = ""
        except:
            self.add_chat("Send failed")

class ChatApp(App):
    def build(self):
        return ChatBox()

ChatApp().run()