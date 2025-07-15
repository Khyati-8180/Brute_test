# main.py

import customtkinter as ctk
from PIL import Image, ImageTk
import database # type: ignore

# App theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# App window
app = ctk.CTk()
app.geometry("600x600")
app.title("Login App 🌸")

# ========== Background ==========
bg_image = Image.open("assets/background.jpg")
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = ctk.CTkLabel(app, image=bg_image, text="")
bg_label.place(relwidth=1, relheight=1)

# ========== Logo ==========
# Load logo once globally (shared by both frames)
logo_image = Image.open("assets/logo.png").resize((80, 80))
logo_image = ImageTk.PhotoImage(logo_image)

# ========== Globals ==========
failed_attempts = 0
is_locked_out = False
lockout_seconds = 60

# ========== Frames ==========
login_frame = ctk.CTkFrame(app, width=450, height=550, fg_color="#069ba2", corner_radius=20, border_width=6, border_color="#024852")
signup_frame = ctk.CTkFrame(app, width=450, height=550, fg_color="#069ba2", corner_radius=20, border_width=6, border_color="#024852")

for frame in (login_frame, signup_frame):
    frame.place(relx=0.5, rely=0., anchor="center")

# ========== Frame Switching ==========
def fade_in(target_frame):
    for frame in (login_frame, signup_frame):
        frame.place_forget()
    target_frame.place(relx=0.5, rely=0.48, anchor="center")

# ========== Countdown for lockout ==========
def countdown(seconds):
    if seconds > 0:
        login_result_label.configure(text=f"⏳ Try again in {seconds}s", text_color="orange")
        app.after(1000, countdown, seconds - 1)
    else:
        global is_locked_out, failed_attempts
        is_locked_out = False
        failed_attempts = 0
        login_button.configure(state="normal")
        login_result_label.configure(text="🔓 Try again now!", text_color="green")

# ========== Login Function ==========
def login():
    global failed_attempts, is_locked_out

    if is_locked_out:
        login_result_label.configure(text="⛔ Locked out! Wait...", text_color="red")
        return

    user = login_username.get()
    pwd = login_password.get()

    if database.verify_user(user, pwd):
        login_result_label.configure(text="✅ Login Successful!", text_color="green")
        failed_attempts = 0
    else:
        failed_attempts += 1
        if failed_attempts >= 3:
            is_locked_out = True
            login_button.configure(state="disabled")
            countdown(lockout_seconds)
        else:
            left = 3 - failed_attempts
            login_result_label.configure(text=f"❌ Wrong! {left} left", text_color="red")

# ========== Signup Function ==========
def signup():
    user = signup_username.get()
    pwd = signup_password.get()

    if not user or not pwd:
        signup_result_label.configure(text="⚠️ Fill all fields", text_color="orange")
        return

    success = database.add_user(user, pwd)
    if success:
        signup_result_label.configure(text="✅ Signup Successful!", text_color="green")
    else:
        signup_result_label.configure(text="❌ Username exists", text_color="red")

# ========== Login UI ==========
ctk.CTkLabel(login_frame, image=logo_image, text="").pack(pady=(30, 10))

ctk.CTkLabel(login_frame, text="Welcome Back 👋", font=("Poppins", 18, "bold"), text_color="white").pack(pady=(0, 10))

login_username = ctk.CTkEntry(login_frame, placeholder_text="Username", width=240, corner_radius=12)
login_username.pack(pady=10, padx=20)

login_password = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=240, corner_radius=12)
login_password.pack(pady=10, padx=20)

login_result_label = ctk.CTkLabel(login_frame, text="", font=("Arial", 12))
login_result_label.pack(pady=5)

login_button = ctk.CTkButton(login_frame, text="Login", command=login, width=200, corner_radius=10)
login_button.pack(pady=(10, 10))

ctk.CTkButton(login_frame, text="No account? Signup", command=lambda: fade_in(signup_frame), width=160, corner_radius=10, fg_color="#4266b9").pack(pady=15)

# ========== Signup UI ==========
ctk.CTkLabel(signup_frame, image=logo_image, text="").pack(pady=(30, 10))

ctk.CTkLabel(signup_frame, text="Create New Account ✨", font=("Poppins", 18, "bold"), text_color="white").pack(pady=(0, 10))

signup_username = ctk.CTkEntry(signup_frame, placeholder_text="Choose a Username", width=240, corner_radius=12)
signup_username.pack(pady=10, padx=20)

signup_password = ctk.CTkEntry(signup_frame, placeholder_text="Create a Password", show="*", width=240, corner_radius=12)
signup_password.pack(pady=10, padx=20)

signup_result_label = ctk.CTkLabel(signup_frame, text="", font=("Arial", 12))
signup_result_label.pack(pady=5)

ctk.CTkButton(signup_frame, text="Signup", command=signup, width=200, corner_radius=10).pack(pady=10)

ctk.CTkButton(signup_frame, text="← Back to Login", command=lambda: fade_in(login_frame), width=160, corner_radius=10, fg_color="#346beb").pack(pady=15)

# Start with Login
fade_in(login_frame)

# Launch app
app.mainloop()
