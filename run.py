import webview
from threading import Thread, Event
import uvicorn
from app import app  # Assuming app.py is your FastAPI application

# This event will be set when we need to stop the FastAPI server
stop_event = Event()

app_title = "App"
host = "127.0.0.1"
port = 8000


def run():
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    while not stop_event.is_set():
        server.run()


if __name__ == "__main__":
    t = Thread(target=run)
    t.daemon = True  # This ensures the thread will exit when the main program exits
    t.start()

    webview.create_window(
        app_title,
        f"http://{host}:{port}",
        resizable=False,
        height=720,
        width=1080,
        frameless=True,
        easy_drag=True,
        on_top=False,
    )

    webview.start()

    stop_event.set()  # Signal the FastAPI server to shut down
