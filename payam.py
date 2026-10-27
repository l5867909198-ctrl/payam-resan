

import asyncio
import threading
import websockets

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

SERVER = "ws://127.0.0.1:8765"

class PayamApp(App):
    def build(self):
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

        root = BoxLayout(orientation="vertical", padding=10, spacing=8)
        self.chat = Label(text="در حال اتصال...", halign="left", valign="top")
        self.chat.bind(size=lambda obj, size: setattr(obj, "text_size", size))
        root.add_widget(self.chat)

        row = BoxLayout(size_hint_y=None, height=48, spacing=5)
        self.entry = TextInput(hint_text="پیام بنویس", multiline=False)
        row.add_widget(self.entry)

        send = Button(text="ارسال", size_hint_x=None, width=80)
        send.bind(on_press=self.send_message)
        row.add_widget(send)
        root.add_widget(row)

        asyncio.run_coroutine_threadsafe(self.receive(), self.loop)
        return root

    async def receive(self):
        while True:
            try:
                async with websockets.connect(SERVER) as ws:
                    Clock.schedule_once(
                        lambda dt: setattr(self.chat, "text", "متصل شدی!")
                    )
                    while True:
                        msg = await ws.recv()
                        Clock.schedule_once(
                            lambda dt, m=msg: setattr(
                                self.chat, "text", self.chat.text + "\n" + m
                            )
                        )
            except Exception:
                Clock.schedule_once(
                    lambda dt: setattr(self.chat, "text", "اتصال برقرار نشد.")
                )
                await asyncio.sleep(3)

    def send_message(self, *_):
        msg = self.entry.text.strip()
        if msg:
            asyncio.run_coroutine_threadsafe(self.send(msg), self.loop)
            self.entry.text = ""

    async def send(self, msg):
        try:
            async with websockets.connect(SERVER) as ws:
                await ws.send(msg)
        except Exception:
            Clock.schedule_once(
                lambda dt: setattr(self.chat, "text", self.chat.text + "\nارسال ناموفق بود.")
            )

PayamApp().run()
