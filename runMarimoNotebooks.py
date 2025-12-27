# Basic usage:
# sudo systemctl restart marimo-python-server.service
# accessable at python.ju.se/marimo
# Edit /etc/systemd/system/marimo-server.service
# Nginx config: /etc/nginx/sites-available/python.conf

from typing import Annotated, Callable, Coroutine
from fastapi.responses import HTMLResponse, RedirectResponse
import marimo
from fastapi import FastAPI, Form, Request, Response, APIRouter
from pathlib import Path
import argparse

# Build the initial Marimo Builder
server = marimo.create_asgi_app(include_code=True)
app_names: list[str] = []

# Parse CLI arg for folder
parser = argparse.ArgumentParser()
parser.add_argument("--folder", type=str)
args = parser.parse_args()

notebooks_dir = Path(args.folder)

# Register all notebooks with builder
for filename in sorted(notebooks_dir.iterdir()):
    if filename.suffix == ".py":
        app_name = filename.stem
        server = server.with_app(path=f"/{app_name}", root=str(filename.resolve()))
        app_names.append(app_name)
        print(f"Registered: {app_name} -> {filename}")

# FastAPI app
app  = FastAPI()
router = APIRouter()

@router.get("/marimo/", response_class=HTMLResponse)
async def index():
    links = "\n".join(
        f'<p><a href="/marimo/{name}">{name.replace("_", " ")}</a></p>'
        for name in app_names
    )
    return f"""
    <html>
        <head>
            <title>Marimo Notebooks</title>
            <style>
                 body {{
                    background-color: #222222;
                    font-family: sans-serif; /* Replace with the font family from mechanics.ju.se */
                    margin: 0;
                    padding: 20px;
                    color: #c4c4c4;
                    display: flex; /* Enable flexbox */
                    flex-direction: column; /* Stack elements vertically */
                    align-items: center; /* Center horizontally */
                    
                 }}
                .marimo-links {{
                     margin-top: 20px;
                 }}
                a {{
                    color: hsl(110, 100%, 87%);;
                    text-decoration: none;
                    transition: color 0.3s ease; /* Add smooth transition */
                }}
                a:hover {{
                    filter: brightness(60%);
                    text-decoration: underline;
                }}
                h1 {{
                    text-align: center;
                }}
                 
            </style>        
        </head>
        <body>
            <h1>Marimo Notebooks</h1>
            <div class="marimo-links">
                {links}
                </div>
        </body>
    </html>
    """

app.include_router(router)
app.mount("/marimo/", server.build())


# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=3100)