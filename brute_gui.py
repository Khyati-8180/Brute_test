import sqlite3
import hashlib
import itertools
import string
import threading
import customtkinter as ctk

DB_FILE = "login_app.db"
CHARSET = string.ascii_lowercase + string.digits
MAX_LENGTH = 4

def get_hash(username):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def start_attack(username, output_box, result_label):
    target_hash = get_hash(username)
    if not target_hash:
        result_label.configure(text="❌ User not found!", text_color="red")
        return

    attempts = 0
    for length in range(1, MAX_LENGTH + 1):
        for attempt in itertools.product(CHARSET, repeat=length):
            guess = ''.join(attempt)
            guess_hash = hash_password(guess)
            attempts += 1
            output_box.configure(state="normal")
            output_box.insert("end", f"Trying: {guess}\n")
            output_box.yview("end")
            output_box.configure(state="disabled")
            if guess_hash == target_hash:
                result_label.configure(
                    text=f"✅ Cracked: {guess} in {attempts} tries", text_color="green"
                )
                return
    result_label.configure(text="❌ Could not crack password.", text_color="red")

# GUI App
app = ctk.CTk()
app.geometry("600x500")
app.title("💣 Brute Force Attack Simulator")

ctk.CTkLabel(app, text="👤 Username to Attack:", font=("Poppins", 16)).pack(pady=(20, 5))
user_entry = ctk.CTkEntry(app, width=250)
user_entry.pack(pady=10)

output_box = ctk.CTkTextbox(app, width=450, height=300)
output_box.pack(pady=10)
output_box.configure(state="disabled")

result_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
result_label.pack(pady=10)

def on_start():
    output_box.configure(state="normal")
    output_box.delete("1.0", "end")
    output_box.configure(state="disabled")
    result_label.configure(text="")
    username = user_entry.get()
    threading.Thread(target=start_attack, args=(username, output_box, result_label)).start()

start_btn = ctk.CTkButton(app, text="💥 Start Attack", command=on_start)
start_btn.pack(pady=15)

app.mainloop()
