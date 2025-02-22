import validators
from . import crud, models, schemas
from .config import get_settings
from .database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL
import qrcode
from io import BytesIO
from . import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(redoc_url=None)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    qr_endpoint = app.url_path_for("generate_qr_code", url_key=db_url.key)
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    db_url.qr_url = str(base_url.replace(path=qr_endpoint))
    return db_url

@app.get("/")
def read_root():
    return "This is the URL shortener API"

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):  # pyright: ignore
        raise_bad_request(message="The provided URL is invalid")

    if url.target_key:
        url.target_key = "".join(
            [c for c in url.target_key if c.isalnum() or c in ["-", "_"]]
        )

    if url.expiration_days and url.expiration_days < 1:
        raise_bad_request(message="Expiration days must be set to at least 1 day")

    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url, status_code=301)
    else:
        raise_not_found(request)

@app.get("/qr/{url_key}")
def generate_qr_code(url_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_db_url_by_key(db=db, url_key=url_key)
    if db_url:
        qr = qrcode.make(db_url.target_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="image/png")
    else:
        raise_not_found()

@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)


@app.delete("/admin/{secret_key}")
def delete_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'!"
        return {"detail": message}
    else:
        raise_not_found(request)
