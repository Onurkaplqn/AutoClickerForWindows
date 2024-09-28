import tkinter as tk
from tkinter import ttk, messagebox
import pygetwindow as gw
import threading
import keyboard
import time
import ctypes
import os
import webbrowser


class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("720x480")  # Pencere boyutunu 720x480 olarak ayarlama
        self.root.configure(bg='black')  # Arka plan rengini siyah yapma

        # Simgeyi ayarlama
        icon_path = 'your_icon.ico'
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        else:
            print("Simge dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")

        self.running = False
        self.paused = False
        self.clicker_position = None
        self.active_window = None

        # Animasyon için
        self.border_color = "#8A2BE2"  # Mor renk
        self.alpha = 0.3
        self.direction = 1

        self.create_widgets()
        self.animate_border()

    def create_widgets(self):
        # Language Buttons
        lang_frame = tk.Frame(self.root, bg='black')
        lang_frame.pack(pady=10)

        self.create_lang_button(lang_frame, "TR")
        self.create_lang_button(lang_frame, "ENG")
        self.create_lang_button(lang_frame, "ZH")
        self.create_lang_button(lang_frame, "RU")

        # Interval
        interval_frame = tk.Frame(self.root, bg='black')
        interval_frame.pack(pady=10)

        self.interval_label = ttk.Label(interval_frame, text="Click Interval (ms):", background="black",
                                        foreground="white")
        self.interval_label.grid(row=0, column=0, sticky='w')
        self.interval_entry = ttk.Entry(interval_frame)
        self.interval_entry.grid(row=0, column=1, padx=5)

        # App Selection
        app_frame = tk.Frame(self.root, bg='black')
        app_frame.pack(pady=10)

        self.app_label = ttk.Label(app_frame, text="Select Application:", background="black", foreground="white")
        self.app_label.grid(row=0, column=0, sticky='w')
        self.app_combobox = ttk.Combobox(app_frame, values=self.get_open_windows())
        self.app_combobox.grid(row=0, column=1, padx=5)

        # Set Click Position Button
        self.set_position_button = tk.Button(self.root, text="Set Click Position", command=self.set_click_position,
                                             bg="#4B0082", fg="white", bd=0, highlightthickness=0)
        self.set_position_button.pack(pady=10)

        # Start Button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_clicking, bg="#4B0082", fg="white",
                                      bd=0, highlightthickness=0)
        self.start_button.pack(pady=10)

        # Pause Button
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_clicking, bg="#4B0082", fg="white",
                                      bd=0, highlightthickness=0)
        self.pause_button.pack(pady=10)

        # Stop Button
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_clicking, bg="#4B0082", fg="white", bd=0,
                                     highlightthickness=0)
        self.stop_button.pack(pady=10)

        # Add Buy Me a Coffee Button with Border Frame
        self.bmc_button_border = tk.Frame(self.root, highlightbackground="white", highlightthickness=2, bd=0)
        self.bmc_button_border.pack(pady=10)

        self.bmc_button = tk.Button(self.bmc_button_border, text="Buy me a coffee ☕", command=self.open_bmc_page,
                                    bg="#474747", fg="white", bd=0, highlightthickness=0)
        self.bmc_button.pack(padx=2, pady=2)  # Slight padding to make the border visible

        self.animate_bmc_button_border()

        # Bind keyboard shortcuts
        keyboard.add_hotkey('ctrl+shift+s', self.start_clicking)
        keyboard.add_hotkey('ctrl+shift+p', self.pause_clicking)
        keyboard.add_hotkey('ctrl+shift+q', self.stop_clicking)
        keyboard.add_hotkey('s', self.pause_clicking)

    def open_bmc_page(self):
        webbrowser.open("https://www.buymeacoffee.com/LestAim")

    def create_lang_button(self, parent, text):
        button = tk.Button(parent, text=text, command=lambda: self.change_language(text), bg="#4B0082", fg="white",
                           bd=0, highlightthickness=0)
        button.pack(side=tk.LEFT, padx=5)

    def change_language(self, lang):
        translations = {
            "TR": {
                "Click Interval (ms):": "Tıklama Aralığı (ms):",
                "Select Application:": "Uygulama Seç:",
                "Set Click Position": "Tıklama Konumunu Ayarla",
                "Start": "Başlat",
                "Pause": "Duraklat",
                "Stop": "Durdur"
            },
            "ENG": {
                "Click Interval (ms):": "Click Interval (ms):",
                "Select Application:": "Select Application:",
                "Set Click Position": "Set Click Position",
                "Start": "Start",
                "Pause": "Pause",
                "Stop": "Stop"
            },
            "ZH": {
                "Click Interval (ms):": "点击间隔 (ms):",
                "Select Application:": "选择应用程序:",
                "Set Click Position": "设置点击位置",
                "Start": "开始",
                "Pause": "暂停",
                "Stop": "停止"
            },
            "RU": {
                "Click Interval (ms):": "Интервал кликов (мс):",
                "Select Application:": "Выберите приложение:",
                "Set Click Position": "Установить положение клика",
                "Start": "Старт",
                "Pause": "Пауза",
                "Stop": "Стоп"
            }
        }

        if lang in translations:
            translation = translations[lang]
            self.update_labels(translation)

    def update_labels(self, translation):
        self.interval_label.config(text=translation["Click Interval (ms):"])
        self.app_label.config(text=translation["Select Application:"])
        self.set_position_button.config(text=translation["Set Click Position"])
        self.start_button.config(text=translation["Start"])
        self.pause_button.config(text=translation["Pause"])
        self.stop_button.config(text=translation["Stop"])

    def animate_border(self):
        new_alpha = self.alpha + 0.02 * self.direction
        if new_alpha >= 1 or new_alpha <= 0.3:
            self.direction *= -1
        self.alpha = new_alpha

        color = self._blend_color("#000000", self.border_color, self.alpha)
        self.root.configure(highlightbackground=color, highlightcolor=color, highlightthickness=2)
        self.root.after(50, self.animate_border)

    def animate_bmc_button_border(self):
        new_alpha = self.alpha + 0.02 * self.direction
        if new_alpha >= 1 or new_alpha <= 0.3:
            self.direction *= -1
        self.alpha = new_alpha

        color = self._blend_color("black", "white", self.alpha)
        self.bmc_button_border.config(highlightbackground=color)
        self.root.after(50, self.animate_bmc_button_border)

    def _blend_color(self, color1, color2, alpha):
        rgb1 = self.root.winfo_rgb(color1)
        rgb2 = self.root.winfo_rgb(color2)
        r = int(rgb1[0] * (1 - alpha) + rgb2[0] * alpha) // 256
        g = int(rgb1[1] * (1 - alpha) + rgb2[1] * alpha) // 256
        b = int(rgb1[2] * (1 - alpha) + rgb2[2] * alpha) // 256
        return f"#{r:02x}{g:02x}{b:02x}"

    def get_open_windows(self):
        windows = gw.getAllTitles()
        return [win for win in windows if win]

    def set_click_position(self):
        app_name = self.app_combobox.get()
        window = gw.getWindowsWithTitle(app_name)
        if not window:
            messagebox.showerror("Error", "Selected application not found.")
            return

        self.active_window = window[0]
        self.active_window.activate()
        messagebox.showinfo("Info", "Hover over the desired position and press 'P'.")

        keyboard.wait('p')
        self.clicker_position = self.get_mouse_position_relative_to_window()
        print(f"Click position set to: {self.clicker_position}")

    def get_mouse_position_relative_to_window(self):
        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))

        # Pencere koordinatlarını al
        window_rect = self.active_window
        window_x, window_y = window_rect.left, window_rect.top

        # Fare pozisyonunu pencereye göre ayarla
        relative_x = pt.x - window_x
        relative_y = pt.y - window_y

        return (relative_x, relative_y)

    def start_clicking(self):
        try:
            interval = int(self.interval_entry.get())
            if not self.clicker_position:
                messagebox.showerror("Error", "Click position not set.")
                return

            self.app_name = self.app_combobox.get()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the interval.")
            return

        if not self.running:
            self.running = True
            self.paused = False
            self.click_thread = threading.Thread(target=self.click_loop, args=(interval,))
            self.click_thread.start()

    def pause_clicking(self):
        self.paused = not self.paused
        if self.paused:
            print("Paused")
        else:
            print("Resumed")

    def stop_clicking(self):
        self.running = False
        self.root.quit()

    def click_loop(self, interval):
        while self.running:
            if self.paused:
                time.sleep(0.1)
                continue

            try:
                window = gw.getWindowsWithTitle(self.app_name)
                if window:
                    window = window[0]

                    click_x, click_y = self.clicker_position

                    # Fareyi hareket ettirmeden tıklama işlemi
                    self.send_click_to_window(window, click_x, click_y)
                    time.sleep(interval / 1000.0)
                else:
                    print(f"Window with title '{self.app_name}' not found.")
                    self.running = False
            except Exception as e:
                print(f"An error occurred: {e}")
                self.running = False

    def send_click_to_window(self, window, x, y):
        # Pencere içi tıklama konumunu hesaplayın
        lParam = (y << 16) | x
        hwnd = window._hWnd
        ctypes.windll.user32.SendMessageW(hwnd, 0x0201, 0x0001, lParam)  # WM_LBUTTONDOWN
        ctypes.windll.user32.SendMessageW(hwnd, 0x0202, 0x0001, lParam)  # WM_LBUTTONUP


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
