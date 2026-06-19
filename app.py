import asyncio
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import edge_tts

# VOICE_MAPPING (Fixed typos to match UX buttons perfectly)
VOICE_MAPPING = {
    "English": {
        "Female Voice": "en-US-AvaNeural",
        "Male Voice": "en-US-AndrewNeural",  # Fixed typo: Vocie -> Voice
    },
    "Malay": {
        "Female Voice": "ms-MY-YasminNeural",
        "Male Voice": "ms-MY-OsmanNeural",  # Fixed typo: Vocie -> Voice
    },
    "Chinese": {
        "Female Voice": "zh-CN-XiaoxiaoNeural",
        "Male Voice": "zh-CN-YunjianNeural",  # Fixed typo: Vocie -> Voice
    },
}


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class TTSApp:

    def __init__(self, root):
        self.root = root
        self.root.title("AnderOng TTS")
        self.root.geometry("600x520")
        self.root.resizable(False, False)

        # [CRITICAL FIX]: Apply icon to both Window and Taskbar
        ico_path = get_resource_path(os.path.join("resources", "app.ico"))
        if os.path.exists(ico_path):
            try:
                self.root.iconbitmap(ico_path)
            except Exception:
                pass

        # UI Styling
        style = ttk.Style()
        style.theme_use("clam")

        # 1. Text Input Region
        label_text = ttk.Label(
            root, text="Please Provide Your Script:", font=("Helvetica", 11)
        )
        label_text.pack(anchor="w", padx=20, pady=(15, 5))

        self.text_input = tk.Text(
            root, height=8, wrap="word", font=("Helvetica", 10), bd=1, relief="solid"
        )
        self.text_input.pack(fill="x", padx=20, pady=5)
        self.text_input.insert(
            "1.0",
            "Terima kasih kerana menghubungi Boustead Heavy Industries Corporation Berhad.",
        )

        # 2. Parameters Configuration Region
        config_frame = ttk.LabelFrame(
            root, text=" Voice Parameter Configuration ", padding=15
        )
        config_frame.pack(fill="x", padx=20, pady=15)
        config_frame.columnconfigure(1, weight=1)

        # 2.1 Choose Language
        ttk.Label(config_frame, text="Choose Language:", font=("Helvetica", 10)).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.lang_var = tk.StringVar(value="Malay")

        lang_frame = ttk.Frame(config_frame)
        lang_frame.grid(row=0, column=1, sticky="w", pady=5, padx=10)
        for lang in VOICE_MAPPING.keys():
            rb = ttk.Radiobutton(
                lang_frame, text=lang, value=lang, variable=self.lang_var
            )
            rb.pack(side="left", padx=10)

        # 2.2 Choose Gender
        ttk.Label(config_frame, text="Choose Gender:", font=("Helvetica", 10)).grid(
            row=1, column=0, sticky="w", pady=10
        )
        self.gender_var = tk.StringVar(value="Female Voice")

        gender_frame = ttk.Frame(config_frame)
        gender_frame.grid(row=1, column=1, sticky="w", pady=10, padx=10)
        for gender in ["Female Voice", "Male Voice"]:
            rb = ttk.Radiobutton(
                gender_frame, text=gender, value=gender, variable=self.gender_var
            )
            rb.pack(side="left", padx=10)

        # 2.3 Speech Speed Adjust
        ttk.Label(
            config_frame, text="Speech Speed Adjust:", font=("Helvetica", 10)
        ).grid(row=2, column=0, sticky="w", pady=5)

        speed_frame = ttk.Frame(config_frame)
        speed_frame.grid(row=2, column=1, sticky="ew", pady=5, padx=10)

        self.speed_slider = ttk.Scale(
            speed_frame, from_=-50, to=50, orient="horizontal"
        )
        self.speed_slider.set(10)
        self.speed_slider.pack(side="left", fill="x", expand=True)

        self.speed_label = ttk.Label(speed_frame, text="+10%", width=6, anchor="e")
        self.speed_label.pack(side="right", padx=(5, 0))
        self.speed_slider.configure(command=self.update_speed_label)

        # 3. Status and Convert Button
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            root, textvariable=self.status_var, font=("Helvetica", 10), foreground="gray"
        )
        status_label.pack(anchor="w", padx=20, pady=5)

        self.btn_convert = ttk.Button(
            root, text="Click to Generate MP3", command=self.start_conversion_thread
        )
        self.btn_convert.pack(fill="x", padx=20, pady=(5, 20), ipady=8)

    def update_speed_label(self, val):
        value = int(float(val))
        sign = "+" if value >= 0 else ""
        self.speed_label.config(text=f"{sign}{value}%")

    def start_conversion_thread(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Prompt", "Please Provide Script!")
            return

        self.btn_convert.config(state="disabled")
        self.status_var.set("Generating MP3, Please Wait...")
        threading.Thread(target=self.run_async_tts, args=(text,), daemon=True).start()

    def run_async_tts(self, text):
        lang = self.lang_var.get()
        gender = self.gender_var.get()
        voice = VOICE_MAPPING[lang][gender]

        speed_val = int(self.speed_slider.get())
        rate_str = f"+{speed_val}%" if speed_val >= 0 else f"{speed_val}%"

        filename = "AnderOng_output.mp3"

        try:
            asyncio.run(self.async_tts_task(text, voice, rate_str, filename))
            self.root.after(
                0,
                lambda: self.on_success(
                    f"Generate Successful!\n\nDocument Saved as:\n{os.path.abspath(filename)}"
                ),
            )
        except Exception as e:
            self.root.after(0, lambda: self.on_error(str(e)))

    async def async_tts_task(self, text, voice, rate_str, filename):
        communicate = edge_tts.Communicate(text, voice, rate=rate_str)
        await communicate.save(filename)

    def on_success(self, msg):
        self.status_var.set("Generated Successful!")
        self.btn_convert.config(state="normal")
        messagebox.showinfo("Successful!", msg)

    def on_error(self, err_msg):
        self.status_var.set("Generate Failed")
        self.btn_convert.config(state="normal")
        messagebox.showerror("Error", f"Error Occurred:\n{err_msg}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TTSApp(root)
    root.mainloop()
