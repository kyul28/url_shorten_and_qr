from . import keygen, models, schemas
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    if url.target_key:
        key = url.target_key
    else:
        key = keygen.create_unique_random_key(db)

    secret_key = f"{key}_{keygen.create_random_key(length=8)}"

    expiration_date = None
    if url.expiration_days:
        expiration_date = datetime.utcnow() + timedelta(days=url.expiration_days)

    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key, expiration_date=expiration_date
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_by_key(db: Session, url_key: str):
    db_url = (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )
    if db_url and db_url.expiration_date and db_url.expiration_date < datetime.utcnow():
        db_url.is_active = False
        db.commit()
        return None
    return db_url


def get_db_url_by_secret_key(db: Session, secret_key: str):
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL):
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def deactivate_db_url_by_secret_key(db: Session, secret_key: str):
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url
