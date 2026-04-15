import threading
import webview
from main import app

def start_server():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    webview.create_window(
        "LoL Overlay",
        "http://127.0.0.1:5000/",
        width=436,
        height=289,
        on_top=True,
        frameless=True,
        transparent=True
    )
    webview.start()