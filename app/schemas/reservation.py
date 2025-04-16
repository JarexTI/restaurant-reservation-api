from datetime import datetime, timezone

from pydantic import BaseModel, Field, validator


class ReservationCreate(BaseModel):
    customer_name: str = Field(
        min_length=1,
        max_length=40,
        description='Character limit violated'
    )
    table_id: int = Field(
        ge=1,
        le=10,
        description='The wrong table is selected'
    )
    reservation_time: datetime
    duration_minutes: int = Field(
        ge=1,
        le=120,
        description='The visit can be anywhere from 1 to 120 minutes.'
    )

    @validator('reservation_time')
    def reservation_time_must_be_in_future(cls, value):
        if value < datetime.now(timezone.utc):
            raise ValueError('Reservation time must be in the future')
        return value


class ReservationRead(BaseModel):
    id: int
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    class Config:
        from_attributes = True
