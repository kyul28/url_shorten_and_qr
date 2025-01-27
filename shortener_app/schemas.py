from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class URLBase(BaseModel):
    target_url: str
    target_key: Optional[str] = None
    expiration_days: Optional[int] = None

class URL(URLBase):
    is_active: bool
    clicks: int
    expiration_date: Optional[datetime]

    class Config:
        from_attributes = True

class URLInfo(URL):
    url: str
    admin_url: str
    qr_url: str | None = None
