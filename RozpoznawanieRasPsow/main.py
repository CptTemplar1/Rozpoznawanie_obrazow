from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex


class HelloWorldApp(App):
    def build(self):
        self.colors = [
            '#FF5733',  # Czerwony
            '#33FF57',  # Zielony
            '#3377FF',  # Niebieski
        ]
        self.current_color_index = 0

        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Hello, World!", font_size='30sp', color=get_color_from_hex(self.colors[0]))
        self.button = Button(text="Zmień kolor", on_press=self.change_color)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
        return self.layout

    def change_color(self, instance):
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        self.label.color = get_color_from_hex(self.colors[self.current_color_index])


if __name__ == '__main__':
    HelloWorldApp().run()
