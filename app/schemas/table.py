from pydantic import BaseModel, Field


class TableCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=40,
        description='Character limit violated'
    )
    seats: int = Field(
        ge=1,
        le=10,
        description='Incorrect number of seats'
    )
    location: str = Field(
        min_length=1,
        max_length=40,
        description='Character limit violated'
    )


class TableRead(BaseModel):
    id: int
    name: str
    seats: int
    location: str

    class Config:
        from_attributes = True
