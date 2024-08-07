from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# from config import config

app = FastAPI()

# Get the absolute path to the current script
current_file_path = Path(__file__).resolve()
current_dir = current_file_path.parent

# Ensure that the 'templates' directory path is absolute
templates_dir = current_dir / "templates"

# Serve static files
app.mount("/static", StaticFiles(directory=templates_dir), name="static")

# Jinja2 template configuration
templates = Jinja2Templates(directory=str(templates_dir))


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    # Render the main index.html page
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/get_data")
async def get_data():
    # Provide a simple JSON response
    data = {"message": "Hello from FastAPI!"}
    return data


if __name__ == "__main__":
    import uvicorn

    # Ensure the server runs with proper configuration directly from app.py when not imported
    uvicorn.run(app, host="0.0.0.0", port=8000)
