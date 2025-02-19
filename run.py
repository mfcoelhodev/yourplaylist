import webview
from threading import Thread, Event
from app import create_app

stop_event = Event()
app = create_app()
app_title = "YourPlaylist"
host = "http://127.0.0.1"
port = 5000

def run():
    while not stop_event.is_set():
        app.run(port=port, use_reloader=False, threaded=True, debug=False)

if __name__ == '__main__':
    t = Thread(target=run)
    t.daemon = True
    t.start()

    webview.create_window(
        app_title,
        f"{host}:{port}",
        resizable=True,
        height=700,
        width=500,
        frameless=False,
    )

    webview.start()

    stop_event.set()