import sys
from PIL import Image
from pystray import Icon, Menu, MenuItem
import webview
import uvicorn
from threading import Thread, Event
from app import app  # Assuming app.py is your FastAPI application
from pathlib import Path

app_title = "App"
host = "127.0.0.1"
port = 8000
stop_event = Event()


def run_fastapi():
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()


def start_fastapi():
    fastapi_thread = Thread(target=run_fastapi)
    fastapi_thread.daemon = True  # Ensure the thread exits when the main program exits
    fastapi_thread.start()
    return fastapi_thread


def create_tray_icon(fastapi_thread):
    script_dir = Path(__file__).resolve().parent
    tray_icon_path = script_dir / "templates" / "tray.png"

    if not tray_icon_path.exists():
        print(f"Tray icon not found at {tray_icon_path}")
        sys.exit(1)

    image = Image.open(tray_icon_path)

    def on_open(icon, item):
        webview.create_window(
            app_title,
            f"http://{host}:{port}",
            resizable=True,
            height=720,
            width=1080,
            frameless=False,
            easy_drag=True,
            on_top=False,
            confirm_close=True,
        )
        webview.start()

    def on_exit(icon, item):
        icon.stop()
        stop_event.set()  # Signal the FastAPI server to shut down
        if fastapi_thread.is_alive():
            fastapi_thread.join(timeout=2)
        sys.exit(0)

    menu = Menu(MenuItem("Open", on_open), MenuItem("Exit", on_exit))
    icon = Icon("App", image, menu=menu)
    icon.run()


if __name__ == "__main__":
    fastapi_thread = start_fastapi()
    create_tray_icon(fastapi_thread)
