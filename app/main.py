import os
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.store_config import (
    APP_LIST,
    App as AppBase,
    SPECIAL_STORE_TYPE_APPS
)


class AppInstallInfo(AppBase):
    install_app_id: str
    thumbnail_url: str
    store_type: str


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
IMAGES_DIR = os.path.join(STATIC_DIR, "images")
DEFAULT_ICON_NAME = "placeholder.png"

# URL for icons
ICON_BASE_URL = "https://egorchadov.github.io/Another-Hisense-App-Store/app/static/images"

app = FastAPI(
    title="Another Hisense TV App Store",
    description="A custom app store for Hisense Vidaa OS",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/apps", response_model=List[AppInstallInfo], summary="Get all apps", tags=["Apps"])
async def get_all_apps():
    apps = []

    for app_data in APP_LIST:
        install_app_id = f"{app_data.name}"
        icon_file_name = f"{app_data.appid}.png"
        thumbnail_path = os.path.join(IMAGES_DIR, icon_file_name)

        if ICON_BASE_URL:
            if os.path.exists(thumbnail_path):
                thumbnail_url_str = f"{ICON_BASE_URL}/{icon_file_name}"
            else:
                thumbnail_url_str = f"{ICON_BASE_URL}/{DEFAULT_ICON_NAME}"
        else:
            if os.path.exists(thumbnail_path):
                thumbnail_url_str = f"/static/images/{icon_file_name}"
            else:
                thumbnail_url_str = f"/static/images/{DEFAULT_ICON_NAME}"

        store_type = "sraf_ext" if app_data.name in SPECIAL_STORE_TYPE_APPS else "store"

        app_install_info = AppInstallInfo(
            **app_data.model_dump(),
            install_app_id=install_app_id,
            thumbnail_url=thumbnail_url_str,
            store_type=store_type,
        )

        apps.append(app_install_info)

    return apps


@app.get("/", response_class=HTMLResponse)
async def read_index_page():
    index_html_path = os.path.join(TEMPLATE_DIR, "index.html")
    try:
        with open(index_html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: index.html not found.</h1>", status_code=500)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Server error</h1><p>{e}</p>", status_code=500)


@app.post("/log")
async def receive_log(request: Request):
    """Receive debug logs from TV client."""
    try:
        data = await request.json()
        print(f"[TV LOG] {data.get('message', data)}")
        return {"status": "ok"}
    except Exception as e:
        print(f"[TV LOG ERROR] {e}")
        return {"status": "error"}