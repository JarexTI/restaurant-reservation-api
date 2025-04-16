from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationCreate, ReservationRead
from app.services.reservation_service import is_reservation_conflicting

router = APIRouter()


@router.get('/', response_model=list[ReservationRead])
async def get_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()


@router.get('/{reservation_id}', response_model=ReservationRead)
async def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail='Reservation not found')
    return reservation


@router.post('/', response_model=ReservationRead)
async def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db)
):
    table = db.get(Table, reservation.table_id)
    if not table:
        raise HTTPException(
            status_code=404,
            detail=f'Table with ID {reservation.table_id} not found'
        )

    # check res conf
    if is_reservation_conflicting(
        db=db,
        table_id=reservation.table_id,
        reservation_time=reservation.reservation_time,
        duration_minutes=reservation.duration_minutes
    ):
        raise HTTPException(
            status_code=404,
            detail='The selected time has already been booked.'
        )

    new_reservation = Reservation(
        customer_name=reservation.customer_name,
        table_id=reservation.table_id,
        reservation_time=reservation.reservation_time,
        duration_minutes=reservation.duration_minutes
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation


@router.delete('/{reservation_id}', response_model=ReservationRead)
async def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    reservation = db.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail='Reservation not found')
    db.delete(reservation)
    db.commit()
    return reservation
